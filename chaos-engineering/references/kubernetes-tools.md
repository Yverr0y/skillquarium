# Kubernetes execution with LitmusChaos and Chaos Mesh

Load this reference after the experiment contract is complete. These commands are patterns,
not authorization to change a cluster. Replace every placeholder and inspect the resulting
target set before running a mutating command.

## Discover the installed control plane

Use the live cluster and installed CRDs as the schema source:

```bash
kubectl config current-context
kubectl cluster-info
kubectl api-resources | rg 'chaos|litmus'
kubectl get crd | rg 'chaos-mesh|litmuschaos'
kubectl get pods -A | rg 'chaos-mesh|litmus'
kubectl auth can-i --list -n <chaos-namespace>
```

That last command checks the current kubeconfig identity. When the controller or fault
runner uses a different service account, also check the identity that will execute the
fault:

```bash
kubectl auth can-i --list \
  --as=system:serviceaccount:<execution-namespace>:<execution-service-account> \
  -n <target-namespace>
```

Inspect the exact resource before authoring YAML:

```bash
kubectl explain podchaos.spec --api-version=chaos-mesh.org/v1alpha1 --recursive
kubectl explain workflow.spec --api-version=chaos-mesh.org/v1alpha1 --recursive
kubectl explain chaosengine.spec --api-version=litmuschaos.io/v1alpha1 --recursive
kubectl explain chaosresult --api-version=litmuschaos.io/v1alpha1
```

Record controller images as an additional version check:

```bash
kubectl get deploy,daemonset -A \
  -l 'app.kubernetes.io/part-of in (chaos-mesh,litmus)' \
  -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{range .spec.template.spec.containers[*]}{.image}{" "}{end}{"\n"}{end}'
```

If labels differ, list candidate controller workloads first and query their images directly.
Do not install or upgrade a chaos platform as an incidental step in an experiment.

## Resolve and bound targets

Preview the selector with ordinary Kubernetes resources:

```bash
kubectl get pods -n <target-namespace> -l '<key>=<value>' -o wide
kubectl get pods -n <target-namespace> -l '<key>=<value>' -o name
kubectl get deploy,statefulset,daemonset,pdb -n <target-namespace> -o wide
kubectl get events -n <target-namespace> --sort-by=.lastTimestamp
```

Require at least one target, fail on unexpected targets, and record the exact names. Check
that an owning controller can replace a killed pod and that disruption budgets, replicas,
zones, and readiness probes match the recovery hypothesis. Avoid system namespaces,
control-plane components, chaos controllers, backup systems, and shared state stores unless
they are explicitly in scope.

Validate a completed manifest against the server without applying it:

```bash
kubectl apply --server-side --dry-run=server -f <experiment.yaml>
kubectl diff -f <experiment.yaml>
```

Review every object shown by `diff`, including service accounts, roles, bindings, schedules,
and helper workloads.

## Chaos Mesh: start with one time-bounded pod fault

This minimal pattern follows the official `PodChaos` schema. Resolve the label selector to
the exact pod approved for the run, record that name, and refuse to continue unless a second
resolution immediately before creation returns the same set. Choose a per-run resource name
and an approved chaos-resource namespace, then verify that identity is unused:

```bash
kubectl get pods -n <target-namespace> -l '<key>=<value>' -o name
# Record the reviewed result as <reviewed-pod-name>, then repeat the query and compare.
kubectl get podchaos -n <approved-chaos-resource-namespace> \
  <unique-experiment-name> >/dev/null 2>&1 && {
    echo "refusing to reuse an existing PodChaos resource" >&2
    exit 1
  }
```

Render the exact reviewed pod into the final manifest. The explicit pod-list selector keeps
the controller from randomly choosing a different member of the original label-selected set.
Use `kubectl create`, not `apply`, so a race cannot update an existing resource.

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: <unique-experiment-name>
  namespace: <approved-chaos-resource-namespace>
  labels:
    chaos.skillquarium.dev/run-id: <run-id>
spec:
  action: pod-failure
  mode: one
  duration: "30s"
  selector:
    pods:
      <target-namespace>:
        - <reviewed-pod-name>
```

Do not copy placeholders into the cluster. Confirm the installed schema, render the final
YAML, repeat the selector preview, compare it with the recorded set, and validate server-side.
For `pod-failure`, require a validated health signal; working liveness/readiness probes are
the recommended implementation because the pause image can otherwise leave the pod looking
`Running` and `Ready`, but they are not a CRD validation requirement. `pod-kill` requires an
owning controller or another proven restart mechanism.

Create, observe, and stop with the exact resource name. After creation, record its UID. Before
cleanup, require both the recorded UID and run label to match the live object; refuse deletion
if either identity check fails.

```bash
kubectl create -f <rendered-experiment.yaml>
kubectl get podchaos -n <approved-chaos-resource-namespace> \
  <unique-experiment-name> -o jsonpath='{.metadata.uid}{"\t"}{.metadata.labels.chaos\\.skillquarium\\.dev/run-id}{"\n"}'
kubectl get pod -n <target-namespace> <reviewed-pod-name> -w
kubectl describe podchaos -n <approved-chaos-resource-namespace> <unique-experiment-name>
live_uid=$(kubectl get podchaos -n <approved-chaos-resource-namespace> \
  <unique-experiment-name> \
  -o jsonpath='{.metadata.uid}')
live_run_id=$(kubectl get podchaos -n <approved-chaos-resource-namespace> \
  <unique-experiment-name> \
  -o jsonpath='{.metadata.labels.chaos\\.skillquarium\\.dev/run-id}')
test "$live_uid" = "<recorded-uid>" && test "$live_run_id" = "<run-id>" || {
  echo "refusing cleanup: PodChaos identity changed" >&2
  exit 1
}
kubectl delete podchaos -n <approved-chaos-resource-namespace> \
  <unique-experiment-name> --wait=true
```

Use `Workflow` only after a single fault is proven. Give every fault node a `deadline`, use
serial composition before parallel composition, and place a `StatusCheck` before expansion.
Set `abortWithStatusCheck` when the installed version supports it and the status check is a
valid abort signal.

Chaos Mesh commonly uses a node-level daemon with elevated privileges to implement network,
process, kernel, and resource faults. Inspect its security context, host mounts, and RBAC;
do not widen them simply to make an experiment run.

## LitmusChaos: inspect the selected fault before creating an engine

Litmus faults are represented by `ChaosExperiment` resources and commonly invoked through a
`ChaosEngine` or a Chaos Center workflow. Source the fault from the current installed or
official ChaosHub catalog, then inspect its definition:

```bash
kubectl get chaosexperiment -n <litmus-resource-namespace> <fault-name> -o yaml
kubectl get chaosexperiment -n <litmus-resource-namespace> <fault-name> \
  -o jsonpath='{.spec.definition.permissions}'
kubectl get serviceaccount,role,rolebinding -n <litmus-resource-namespace>
```

The Litmus resource namespace and application target namespace can be the same in a given
installation, but resolve and record each role explicitly instead of assuming they coincide.

Do not treat `.spec.definition.permissions` as effective policy: it declares the fault's
required permissions but does not create or constrain RBAC. Resolve the `ChaosEngine`
`chaosServiceAccount`, inspect every associated `Role`, `ClusterRole`, `RoleBinding`, and
`ClusterRoleBinding`, and impersonate that identity before approving the run:

```bash
kubectl get chaosengine -n <litmus-resource-namespace> <engine-name> \
  -o jsonpath='{.spec.chaosServiceAccount}{"\n"}'
kubectl get role,rolebinding -n <litmus-resource-namespace> -o yaml
kubectl get clusterrole,clusterrolebinding -o yaml
kubectl auth can-i --list \
  --as=system:serviceaccount:<litmus-resource-namespace>:<chaos-service-account> \
  -n <target-namespace>
```

The actual bindings on that service account, including cluster-scoped grants, determine its
effective permissions. Require least privilege even when the declared minimum is narrower.

For a first experiment:

- Populate the application's namespace, kind, and labels or the fault's explicit target
  fields; never leave selection fields blank.
- Use one target or the smallest supported affected percentage and serial execution.
- Set the fault duration, interval, ramp time, and helper timeout explicitly.
- Add a command, HTTP, Kubernetes, or Prometheus probe that implements the steady-state
  check. Confirm whether it runs before, during, after, or continuously.
- Bind the engine to a dedicated service account containing only the permissions declared
  by the chosen fault.
- Preview the generated workflow and all fault environment variables before execution.

Monitor the engine, runner/helper pods, events, and result separately from application SLIs:

```bash
kubectl get chaosengine,chaosresult -n <litmus-resource-namespace> -w
kubectl get pods -n <litmus-resource-namespace> -l app.kubernetes.io/part-of=litmus -o wide
kubectl get events -n <target-namespace> --sort-by=.lastTimestamp
```

Use the Chaos Center stop control when it started the run. For a directly managed engine,
confirm the installed schema before changing `spec.engineState` to `stop`. Verify helper
termination, result state, target recovery, and steady-state recovery; a `ChaosResult`
verdict alone does not prove user-visible resilience.

## Agent and MCP guardrails

Treat control surfaces by effect:

- Read-only: list platforms, experiments, targets, runs, probes, and results.
- Drafting: prepare a contract or manifest without applying it.
- Mutating: install, register infrastructure, create, run, schedule, stop, or delete an
  experiment; these require the same explicit scope and execution gate as direct CLI use.

Keep platform endpoints and tokens out of committed files. Use a project and environment
with the narrowest feasible permissions. Require a human-readable target preview before a
mutating tool call, and never let an agent schedule or execute production chaos unattended.

## Evidence and cleanup checklist

Capture:

- Kubernetes context, controller images, CRD versions, manifest digest, and applied object.
- Resolved target names, experiment start/stop timestamps, events, and controller logs.
- Baseline, fault-window, and recovery-window metric snapshots using the same queries.
- Abort action and timestamp, recovery completion, data-integrity result, and orphan check.

After the run, verify that no experiment, schedule, workflow, runner/helper pod, or fault
side effect remains. Keep result resources only when required for audit history.

## Official sources

- [Principles of Chaos Engineering](https://principlesofchaos.org/)
- [Chaos Mesh: simulate pod faults](https://chaos-mesh.org/docs/simulate-pod-chaos-on-kubernetes/)
- [Chaos Mesh: create a workflow](https://chaos-mesh.org/docs/create-chaos-mesh-workflow/)
- [Chaos Mesh architecture](https://chaos-mesh.org/docs/)
- [LitmusChaos repository](https://github.com/litmuschaos/litmus)
- [LitmusChaos fault catalog](https://github.com/litmuschaos/chaos-charts)

The patterns above were checked on 2026-08-01 against Chaos Mesh tag
[`v2.8.3`](https://github.com/chaos-mesh/chaos-mesh/tree/v2.8.3) at commit
`60ec97f1fd5d5edb2fb5c722c8888e18b618d1a0` (`api/v1alpha1/podchaos_types.go`,
`api/v1alpha1/workflow_types.go`, and `config/crd/bases/chaos-mesh.org_podchaos.yaml`)
and LitmusChaos tag [`3.31.0`](https://github.com/litmuschaos/litmus/tree/3.31.0) at
commit `5d37ea84a96a1653a13781fad6f3d7ffcde7f660` (the ChaosExperiment scope and
configuration documents plus ChaosEngine RBAC guidance under
`mkdocs/docs/experiments/concepts/`). Reinspect current official sources and the installed
CRDs when versions differ.
