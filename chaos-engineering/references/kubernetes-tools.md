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

This minimal pattern follows the official `PodChaos` schema. Use a dedicated chaos resource
namespace if the installed configuration requires it, and set the selector namespace to the
approved workload namespace.

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: bounded-pod-failure
  namespace: chaos-mesh
spec:
  action: pod-failure
  mode: one
  duration: "30s"
  selector:
    namespaces:
      - <target-namespace>
    labelSelectors:
      <label-key>: <label-value>
```

Do not copy placeholders into the cluster. Confirm the installed schema, render the final
YAML, repeat the selector preview, and validate server-side. `pod-failure` requires working
liveness/readiness probes to reveal loss of functionality reliably; `pod-kill` requires an
owning controller or another proven restart mechanism.

Observe and stop with the exact resource name:

```bash
kubectl get podchaos -n chaos-mesh bounded-pod-failure -o yaml
kubectl get pods -n <target-namespace> -l '<key>=<value>' -w
kubectl describe podchaos -n chaos-mesh bounded-pod-failure
kubectl delete podchaos -n chaos-mesh bounded-pod-failure --wait=true
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
kubectl get chaosexperiment -n <chaos-namespace> <fault-name> -o yaml
kubectl get chaosexperiment -n <chaos-namespace> <fault-name> \
  -o jsonpath='{.spec.definition.permissions}'
kubectl get serviceaccount,role,rolebinding -n <chaos-namespace>
```

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
kubectl get chaosengine,chaosresult -n <chaos-namespace> -w
kubectl get pods -n <chaos-namespace> -l app.kubernetes.io/part-of=litmus -o wide
kubectl get events -n <chaos-namespace> --sort-by=.lastTimestamp
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

The patterns above were checked against Chaos Mesh 2.8.3 and LitmusChaos 3.31.0 on
2026-08-01. Reinspect current official sources and the installed CRDs when versions differ.
