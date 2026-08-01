---
name: chaos-engineering
description: Design and run bounded chaos engineering experiments that test whether a system preserves measurable steady-state behavior during realistic faults. Use for resilience hypotheses, game days, fault injection, failover and recovery validation, or LitmusChaos and Chaos Mesh experiments involving pod, node, network, latency, resource, storage, DNS, time, or cloud failures. Require explicit authorization before mutating an environment, especially production; do not use as a substitute for load testing, disaster-recovery planning, penetration testing, or incident response. Pair with kubernetes-specialist when broader cluster design or workload remediation is required.
---

# Chaos Engineering

Treat chaos as a controlled experiment against a falsifiable resilience hypothesis,
not as random breakage. Prefer the smallest fault that can reveal a meaningful weakness.

## Gate execution

Planning, manifest review, and read-only discovery can proceed without changing a system.
Before injecting a fault, establish all of the following:

- Explicit authorization for the named environment, cluster, namespace, services, and fault.
- An accountable owner, active observer, approved window, and communication channel.
- A measurable baseline, abort thresholds, a stop mechanism, and recovery steps.
- A bounded selector, target count, duration or deadline, and maximum concurrent impact.

Treat production as unauthorized unless the user explicitly names and approves it. Stop
and request direction when scope is ambiguous, a target selector is empty or broader than
intended, an abort path is untested, or the proposed fault could threaten control-plane,
security, backup, or shared data services outside the approved scope.

Do not claim that an experiment ran without execution evidence. If access is unavailable,
deliver a plan or manifest labeled **not executed**.

## Build the experiment contract

Write the contract before choosing a tool or fault:

1. **Steady state** — define user-visible and system-level indicators, their queries,
   acceptable ranges, and a baseline observation window.
2. **Hypothesis** — state what should remain true while the fault is active and how the
   experiment could disprove it.
3. **Failure mode** — select one realistic risk from incidents, architecture assumptions,
   dependency behavior, or an FMEA; do not begin with a compound scenario.
4. **Blast radius** — name the environment, region or cluster, namespace, workload,
   label selector, resolved targets, target count, concurrency, and duration.
5. **Abort criteria** — use live, quantitative thresholds such as error rate, latency,
   unavailable replicas, queue depth, data-integrity signals, or operator health.
6. **Recovery proof** — define how to stop injection, restore state if automatic recovery
   fails, and prove that service health and data correctness returned to baseline.

Use this compact contract:

```text
Experiment: <name>
Owner/window: <owner> / <start-end and timezone>
Environment and targets: <exact scope and resolved target count>
Steady state: <metric or probe, query, baseline, acceptable range>
Hypothesis: Given <fault>, <steady state> remains <range> for <duration>
Fault: <type, intensity, duration, concurrency>
Abort when: <threshold, evaluation interval, responsible observer>
Stop and recover: <command or control, rollback, recovery deadline>
Evidence: <dashboard, logs, events, traces, result object, timestamps>
```

## Inspect the real system

Ground the design in current topology and tool schemas:

- Map clients, dependencies, replicas, zones, health probes, autoscaling, disruption
  budgets, retries, timeouts, queues, and stateful boundaries.
- Confirm which component is expected to detect, contain, and recover from the fault.
- Resolve selectors with a read-only query and record every target before applying chaos.
- Inspect installed CRDs, CLI help, controller versions, and official documentation instead
  of guessing a manifest schema from memory.
- Review the fault's service account, RBAC, admission behavior, privileged components, and
  cleanup semantics. Grant only the permissions required for this experiment.
- Capture a quiet baseline with the same probes and observation interval used during chaos.

Read [kubernetes-tools.md](references/kubernetes-tools.md) when using LitmusChaos or
Chaos Mesh. Recheck upstream guidance when installed versions differ from its source basis.

## Run progressively

1. Rehearse the stop path in a disposable or non-production environment.
2. Validate the rendered configuration against the live API without applying it.
3. Begin with one recoverable target and one fault. Avoid `all`, broad percentages,
   empty selectors, unbounded schedules, and parallel faults on the first run.
4. Start synchronized evidence capture, then inject the fault for the agreed duration.
5. Watch both user-visible steady state and the recovery mechanism. Do not rely only on
   the chaos controller reporting success.
6. Abort immediately when any abort threshold fires. Stop injection first, preserve
   evidence second, and escalate through the agreed channel.
7. Remove the chaos resource or stop the experiment, then verify workload recovery,
   steady-state recovery, and data integrity.
8. Expand one dimension at a time only after a clean result: duration, target count,
   fault intensity, environment, or fault composition.

For recurring experiments, first prove the same experiment manually, then add scheduling,
concurrency control, deadlines, automated probes, and alerts for stuck or orphaned chaos.

## Choose the control surface

| Situation | Prefer | Check before use |
| --- | --- | --- |
| Kubernetes-native faults and workflow composition | Chaos Mesh | Installed CRDs, target namespace rules, daemon privileges, duration/deadline semantics |
| Litmus ChaosHub experiments, probes, and resilience results | LitmusChaos | Current fault definition, ChaosEngine schema, experiment RBAC, service account, probe behavior |
| Managed cloud or service-specific failure | Provider-native fault service | Account and region scope, IAM, stop action, quotas, data-service safeguards |
| Process or dependency behavior covered in code | Test harness or proxy fault injection | Fidelity to production, deterministic cleanup, assertion quality |

An agent or MCP interface does not relax the execution gate. Listing, describing, and
drafting are read-only; running, scheduling, stopping, or changing infrastructure are
mutations. Keep credentials scoped, require an exact target preview, and never let an
agent autonomously apply chaos to production.

## Interpret the result

Separate platform execution from resilience outcome:

- **Passed** — the intended fault was observed, steady state stayed within the contract,
  and recovery completed within the limit.
- **Failed safely** — the intended fault was observed, the hypothesis was disproved, and
  abort/recovery controls contained the impact.
- **Aborted** — a guardrail fired or an operator stopped the run; report the triggering
  signal and recovery evidence.
- **Inconclusive** — injection, observability, targeting, or baseline evidence was
  insufficient; do not treat this as a pass.

Report timestamps, exact fault parameters, resolved targets, metric traces, controller
events, stop action, time to detection, time to recovery, and any data-integrity checks.
Turn a failed hypothesis into an owned remediation and rerun only after the fix is verified.

## Quality gate

Before calling the work complete, verify that:

- The steady state and hypothesis are quantitative and falsifiable.
- Scope, selectors, target count, duration, and concurrency are explicit.
- Production authorization and the approved window are recorded when applicable.
- Abort thresholds are live, observable, and assigned to an operator or automation.
- The stop path is faster than the expected harm and does not depend on the failed service.
- The manifest or API request matches the installed tool version.
- Injection happened as intended, cleanup completed, and recovery was independently proven.
- The result is labeled passed, failed safely, aborted, or inconclusive with evidence.

## Source basis

This workflow follows the [Principles of Chaos Engineering](https://principlesofchaos.org/)
method: define steady state, form a hypothesis, introduce realistic variables, and seek
evidence that disproves the hypothesis while minimizing blast radius. Kubernetes tool
patterns were checked against official Chaos Mesh 2.8.3 and LitmusChaos 3.31.0 sources on
2026-08-01. Treat the installed CRDs and current official documentation as authoritative.
