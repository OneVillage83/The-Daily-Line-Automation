# ADR-0007 — Immutable Execution Envelope and Reconciliable Backend Dispatch

Date: 2026-09-05  
Status: **ACCEPTED**

## Context

A-10 bridges the boundary between TDLA's canonical logical execution authority and replaceable physical worker/backends.

Several failure modes make a direct `ready -> queue -> run` model unsafe:

- eligibility can become stale between A-9 evaluation and physical submission;
- backend submission acknowledgement can be lost even after a job/message is accepted;
- worker heartbeat/lease loss does not prove the submitted job or sport child stopped;
- the worker can die after sport child acceptance but before recording the child ref;
- backend-native IDs are vendor-specific and may disappear or change when runtimes are replaced;
- a process/backend can report success while the sport semantic result or required outputs are invalid;
- partial artifacts can exist without a committed semantic result;
- queue messages can remain pending long enough for plan/schedule/readiness authority to change.

A durable production architecture therefore needs an immutable physical execution request, a TDLA-owned dispatch identity, and independent reconciliation for both backend submission and nested sport child execution.

## Decision

TDLA will use the following execution-plane model:

```text
A-9 DispatchEligibilityGrant
        |
        v
current-authority verification
        |
        v
A-11 logical StageRun / RunAttempt authority
        |
        v
immutable ExecutionEnvelope
        |
        v
FINAL current-authority verification
        |
        v
durable TDLA DispatchRecord / stable BackendSubmissionKey
        |
        v
replaceable backend submission
        |
        +---- backend-native ExecutionHandle
        |
        v
worker/transport
        |
        v
A-5 Sport Automation Adapter
        |
        +---- sport child execution ref
        |
        v
semantic result + immutable output manifests
```

The architecture adopts these durable decisions:

1. **ExecutionEnvelope is immutable, versioned, and hashable.** It captures the exact StageRun/RunAttempt, A-9 grant, plan/stage/scope/schedule authority, immutable target, adapter/config/input contracts, environment/mode, A-11 idempotency reference, and expected result/output contract.
2. **Dispatch intent is durable before irreversible external submission.** Exact transaction/outbox mechanics are deferred to A-13.
3. **Backend-native job/message/pod/process IDs are provenance only.** They never replace canonical TDLA WorkflowRun/StageRun/RunAttempt identity.
4. **A stable BackendSubmissionKey exists for one RunAttempt's backend submission authority.** Safe retransmission after acknowledgement ambiguity reuses the same stable identity when the backend supports idempotent submission.
5. **Backend submission reconciliation and A-5 sport-child reconciliation are separate responsibilities.** One cannot substitute for the other.
6. **Final current-authority revalidation occurs immediately before backend submission.** A syntactically valid A-9 grant or already-created RunAttempt does not override a newly stale plan/scope/schedule/readiness/dependency/policy witness.
7. **Runtime/backend completion is not semantic completion.** A StageRun result depends on A-5/A-6 semantic result/output contracts, not Prefect Completed, process exit code, Kubernetes Job completion, or queue acknowledgement alone.
8. **Cancellation/heartbeat/lease observations are not proof of child termination.** Reconciliation establishes trustworthy terminal state.
9. **Backend replacement must preserve TDLA identity/audit semantics.** Prefect, Docker, Kubernetes, queue workers, local subprocesses, or sport-service transports may change without redefining what logical work occurred.

## Alternatives considered

### 1. Use backend-native job ID as RunAttempt identity

Rejected.

This couples TDLA business/audit identity to a physical runtime and breaks historical continuity during backend replacement or backend record expiration.

### 2. Submit external work first, then record TDLA dispatch state

Rejected.

A crash between external submission and local persistence creates an orphan with no durable TDLA intent and encourages unsafe duplicate redispatch.

### 3. Treat one backend acknowledgement as proof the child exists

Rejected.

Backend acceptance may precede worker execution or sport child creation. Conversely, a sport child can exist after the worker/backend reporting path fails.

### 4. Use A-5 child idempotency as the only duplicate-submission defense

Rejected.

A queue/container/Prefect/Kubernetes backend can duplicate physical jobs before the A-5 boundary is reached. Backend submission ambiguity therefore needs its own identity/reconciliation layer.

### 5. Trust queue age/worker claim once work has been enqueued

Rejected.

Plan, schedule, readiness, output, or policy authority may change while queued. Final current-authority validation is required close to the physical side-effect boundary.

### 6. Rely on singleton workers/schedulers to avoid duplicates

Rejected.

Production correctness must tolerate duplicate delivery, HA workers, network partitions, process restarts, and lost acknowledgements.

### 7. Treat process exit 0/backend Completed as StageRun success

Rejected.

This cannot prove required output manifests, schema/digests, semantic sport disposition, or correct provenance.

## Consequences

### Benefits

- backend/runtime can be replaced without rewriting canonical execution history;
- stale queued work fails closed before start;
- lost backend acknowledgements can be reconciled without blind duplicate submission;
- lost sport-child acknowledgements remain recoverable through A-5 independently;
- immutable envelopes provide exact attempt-level audit/reproducibility evidence;
- worker heartbeat/lease/cancellation races do not accidentally authorize duplicate side effects;
- output validation remains contract-based rather than runtime-status-based;
- supports local, Docker, Prefect, queue, Kubernetes, service, CPU, GPU, and publication workers under one logical architecture.

### Costs

- production backends need reconciliation/idempotent-submission support or a certified compensating design;
- A-13 persistence must support durable dispatch intent, handles, callbacks, reconciliation, and envelope references;
- A-11 must coordinate logical attempt authority and stable backend submission identity;
- execution startup requires current-authority revalidation and may reject stale queued work;
- result correlation requires explicit attempt/envelope/child bindings.

These costs are accepted because duplicate model runs, duplicate external side effects, or untraceable orphan jobs are more damaging.

## Compatibility / migration impact

No production TDLA worker runtime currently exists, so there is no deployed schema/runtime to migrate.

Future implementations may use Prefect 3 initially, but Prefect IDs remain runtime cross-references only.

A backend migration must preserve:

- TDLA WorkflowRun/StageRun/RunAttempt lineage;
- ExecutionEnvelope semantics;
- A-9 grant/evaluation lineage;
- A-11 logical idempotency identity;
- A-5 sport child identity;
- output/result contracts and audit evidence.

## Security / authorization impact

The ExecutionEnvelope contains stable secret/service-identity references only, never raw secret values.

Worker/backend capability does not equal production authorization. Environment, mode, plan/certification, A-19 approvals where applicable, A-20 service identity, and side-effect policies remain mandatory.

## Validation required

Implementation must prove at minimum:

- stale A-9 grant rejected immediately before submission;
- stable backend submission identity survives lost acknowledgement;
- duplicate queue/backend deliveries do not create duplicate logical work;
- ambiguous backend submission is reconciled before resubmission;
- sport child accepted before worker death can be recovered through A-5 logical idempotency;
- heartbeat/lease/cancel loss does not automatically mark child stopped;
- backend completion without valid semantic outputs does not become StageRun success;
- partial artifacts cannot satisfy terminal output contracts;
- final result is correlated to exact attempt/envelope/child authority;
- backend migration does not change canonical TDLA identities;
- all A-10 certification stress cases pass.

## Related architecture

- A-3 Run identity / execution lifecycle
- A-5 Sport Automation Adapter
- A-6 Pipeline Plan / Stage Contracts
- A-7 Trigger Architecture
- A-8 Event-Relative Scheduling Engine
- A-9 Dependency / Readiness Engine
- A-10 Worker / Execution Backend Architecture
- future A-11 Retry / Timeout / Idempotency
- future A-12 Failure / Degradation / Recovery
- future A-13 Persistence / Audit / Provenance
- future A-20 Security / Service Identity
- future A-21 Deployment / HA

## Supersession

Supersedes: none.  
Superseded by: none.