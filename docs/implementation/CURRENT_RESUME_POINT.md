# The Daily Line Automation — Current Resume Point

Last updated: 2026-09-05 (America/Los_Angeles)  
Authority: This file is the single exact continuation point for unfinished TDLA work. It does not override architecture/certification authority; it tells the next session where to resume.

## Current project state

- Repository constitution/documentation-memory policy is authoritative in `AGENTS.md`.
- A-0 through A-4 Foundation V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-5 Sport Automation Adapter V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-6 Pipeline Plan / Stage Contracts V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-7 Trigger Architecture V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-8 Event-Relative Scheduling Engine V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-9 Dependency / Readiness Engine V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-9 review evidence: `docs/implementation/A09_ARCHITECTURE_CONFORMANCE_REVIEW_20260905.md`.
- ADR-0001: TDLA canonical identity / replaceable orchestration runtime.
- ADR-0002: transport-neutral Sport Automation Adapter protocol.
- ADR-0003: immutable plan fragments / explicit composition / resolved-plan authority.
- ADR-0004: durable trigger evidence / reevaluation-only trigger authority.
- ADR-0005: stable schedule slots / immutable resolved-time authority / reevaluation-only due events.
- ADR-0006: version-bound dispatch eligibility / mandatory final current-authority revalidation.
- No production implementation milestone is certified.
- No TDLA automation is production-authoritative.
- Daily-MLB remains manual-first; later automation must prove equivalence after its final manual production pipeline is certified.

## Certified nested architecture through A-9

```text
sport-owned scope/discovery/plan fragment
        +
TDLA platform fragment(s)
        |
        v
explicit PlanAssembly + typed bindings
        |
        v
immutable ResolvedAutomationPlan
        |
        v
StageDefinition / StageMaterialization
        |
        +------------------------------+
        |                              |
        v                              v
A-6 TimingDeclaration             A-7 TriggerBinding
        |                              |
        v                              v
A-8 ScheduleResolution        TriggerDelivery/Event
        |                              |
        v                              v
A-8 ScheduleOccurrence        TriggerEvaluation
        |                              |
        +------ TIME_DUE ------------> EligibilityReevaluationRequest
                                       |
                                       v
                           A-9 EligibilityEvaluation
                              current authority
                              time/window
                              dependencies/outputs
                              A-5 readiness/freshness
                              policy/mode/applicability
                                       |
                                       v
                           DispatchEligibilityGrant
                         (version-bound, non-bearer)
                                       |
                                       v
                              A-10/A-11 NEXT:
                        revalidate + dispatch/idempotency
                                       |
                                       v
                         A-5 Sport Automation Adapter
                                       |
                                       v
                            sport child job/service
                                       |
                                       v
                         DDC/provider evidence where used
```

## Important locked A-9 rules

1. `READY` is derived immutable evidence, not a persistent mutable boolean.
2. A-5 sport `READY` is only one readiness gate and never direct TDLA execution authority.
3. A-9 checks current plan/materialization/scope/schedule/mode/policy authority before and after evidence collection.
4. A stale or superseded plan/scope/schedule/materialization cannot become current because old dependencies/readiness once passed.
5. Dependency satisfaction binds exact upstream StageRun/materialization/output manifest/schema/digest/provenance authority.
6. Same-named outputs from an old plan/scope/snapshot/replay cannot silently satisfy current work.
7. Upstream output supersession/retraction invalidates dependent current eligibility/grants before dispatch.
8. `OPTIONAL` does not mean automatically ignorable; explicit downstream dependency/output contracts decide satisfaction.
9. `NO_OP` cannot satisfy an output dependency for output it did not produce unless the exact contract permits absent output/no-op semantics.
10. `SUCCEEDED_DEGRADED` satisfies only exact validated outputs allowed by bound policy.
11. Fan-in binds exact A-6 `ScopeSetBinding` membership revision/digest; no sport-ID inference or implicit empty-set success.
12. A-5 sport reason codes stay opaque; generic TDLA never branches on pitcher/lineup/inactive/weather meaning.
13. Technical readiness timeout/schema/capability failure is not sport `WAITING`, `BLOCKED`, or `READY`.
14. Readiness cache validity is the intersection of sport validity, plan max-age, evidence freshness, schedule/window validity, and policy bound.
15. Any incompatible plan/stage/scope/schedule/readiness/evidence revision invalidates cached readiness immediately even if its wall-clock TTL has not expired.
16. Composite readiness uses explicit versioned required/optional composition; optional predicates cannot compensate for failed required predicates.
17. PIT/freshness contracts are enforced through declared generic provenance/cutoff metadata; sport-specific PIT meaning remains sport-owned.
18. A-7 reevaluation cause is distinct from A-9 evaluation result; multiple causes can map to one semantic current evaluation while every cause remains auditable.
19. Eligibility semantic digest is distinct from unique evaluation-record identity and causal trigger lineage.
20. Deterministic reason sets do not require unnecessary external readiness calls after an earlier authoritative gate already proves the stage cannot proceed.
21. `READY_FOR_DISPATCH` does not mean worker assigned, dispatch succeeded, child started, A-11 idempotency passed, or side effect occurred.
22. A-9 issues a `DispatchEligibilityGrant` only for an exact ready authority/evidence set.
23. The grant is immutable, non-transferable, environment/mode/stage/scope/revision-bound, and never a bearer token.
24. Grant validity cannot outlive the earliest applicable readiness/time/window/policy authority expiry.
25. When no safe TTL exists, dispatch requires immediate inline current-authority revalidation.
26. A-10/A-11 must verify current plan/scope/schedule/dependency/readiness/policy witnesses before using a grant.
27. Superseded/expired grants remain immutable audit evidence but cannot authorize dispatch.
28. A-9 does not create StageRun/RunAttempt child work and does not replace A-11 final logical execution idempotency.
29. Ordinary trigger/readiness changes do not replay/reprocess already-terminal stages; A-14 later owns explicit historical lineages.
30. Prefect/Celery/Redis/process-local readiness state can never become canonical eligibility authority.

## Daily-MLB / football compatibility note that must not be forgotten

Future sport integrations remain responsible for sport readiness meaning and canonical sport state.

A future adapter can provide:

```text
ReadinessResult(
    disposition = READY | WAITING | BLOCKED | NOT_APPLICABLE,
    opaque sport reason/evidence,
    scope revision,
    freshness/validity
)
```

TDLA then evaluates only generic current authority, dependencies, outputs, time/window, freshness, mode, and policy.

TDLA must never implement:

```text
if MLB probable pitcher confirmed -> READY
if lineup posted -> READY
if NFL inactives final -> READY
if weather changed enough -> rerun
```

Current Daily-MLB remains manual-first and is **not** production-ready merely because A-9 is certified.

---

# Exact next step — A-10 Worker / Execution Backend Architecture

Design the replaceable execution plane that consumes an A-9 `DispatchEligibilityGrant`, performs mandatory final current-authority verification, creates/executes one physical dispatch attempt under TDLA canonical identity, invokes the A-5 sport adapter through an immutable execution envelope, and safely reconciles worker/backend/child-job ambiguity without making Prefect/Docker/Kubernetes/queue IDs canonical TDLA identity.

The central A-10 rule should be:

> **A worker/backend is an execution mechanism, not workflow authority. TDLA canonical StageRun/RunAttempt identity, immutable execution envelope, eligibility authority, and child-operation provenance remain valid when the physical backend changes. A backend acknowledgement or process exit code is never sufficient proof of semantic success.**

A-10 should define the execution plane without prematurely freezing A-11 retry/idempotency algorithms or A-13 persistence DDL.

## A-10 must define at minimum

### 1. Execution-plane authority entities

Define clear logical identities/contracts for concepts such as:

- `ExecutionBackendDescriptor`;
- `WorkerCapabilityDescriptor`;
- `WorkerClassRef`;
- `DispatchRequest`;
- immutable `ExecutionEnvelope`;
- `DispatchRecord` / dispatch intent;
- `WorkerAssignment`;
- `ExecutionHandle` / backend job handle;
- `DispatchAcknowledgement`;
- worker heartbeat/liveness evidence;
- cancellation request/ack evidence;
- execution result/child-operation handoff;
- backend reconciliation result.

Exact names may change, but canonical TDLA run/attempt identity must remain separate from backend-native job/task IDs.

### 2. A-9 grant consumption and final revalidation

Before physical dispatch:

- verify `DispatchEligibilityGrant` semantic digest/signature/integrity as applicable;
- verify it targets this exact stage materialization/environment/mode;
- verify it has not expired;
- re-check all required current-authority witnesses identified by A-9/ADR-0006;
- fail closed and request reevaluation when stale;
- do not silently mint a new grant inside the backend layer.

Define the exact boundary between A-10 current-authority verification and A-11 final logical idempotency/attempt creation.

### 3. ExecutionEnvelope contract

Define an immutable, hashable envelope sufficient to reproduce/audit the physical attempt.

At minimum consider:

- TDLA WorkflowRun/StageRun/RunAttempt refs as applicable;
- stage materialization/ref/version;
- resolved plan digest;
- A-9 eligibility evaluation/grant ref/digest;
- sport scope/scope revision;
- schedule resolution/time/deadline context;
- immutable execution target/release/image digest;
- adapter descriptor/protocol/capability binding;
- validated non-secret configuration ref/digest;
- logical idempotency reference supplied under A-11 contract;
- input/output manifest refs;
- execution mode/environment;
- worker/backend class requirements;
- resource requirement hints;
- timeout/cancellation policy refs (exact mechanics A-11);
- service identity/secret references, never secret values;
- trace/correlation IDs;
- created/issued time;
- envelope schema/version/digest.

### 4. Backend abstraction

A-10 should support interchangeable physical mechanisms such as:

- local subprocess for development/test;
- OCI/Docker container worker;
- authenticated sport service invocation;
- queue-backed worker;
- Prefect worker/deployment;
- Kubernetes Job/worker pool;
- dedicated GPU/heavy-CPU/research/publication worker classes later.

Backend-native IDs are cross-references only.

### 5. Worker capability matching

Define generic capabilities such as:

- CPU architecture/OS where needed;
- container support;
- network/provider access class;
- GPU class;
- memory/storage class;
- sport-adapter protocol/capability compatibility;
- environment authorization;
- secret/service-identity capability;
- side-effect/customer-visible authorization class where applicable;
- version/capability descriptor digest.

A stage must fail closed if no compatible authorized worker/backend exists.

A-15 later owns resource/concurrency budgeting and optimization, not A-10.

### 6. Worker classes vs individual workers

Separate:

```text
WorkerClassRef
    = stable logical class/capability target

WorkerInstance
    = ephemeral physical worker/process/node/pod
```

A plan may target a certified worker class/hints without binding business identity to one machine hostname/pod ID.

### 7. Dispatch intent must be durable before irreversible external action

Architectural requirement:

```text
durable TDLA dispatch intent / attempt authority
    -> backend submission/invocation
```

not:

```text
start external child first
    -> maybe record it later
```

Exact transaction/outbox mechanics remain A-13.

### 8. Dispatch acknowledgement identity

Separate:

- TDLA dispatch/attempt identity;
- backend submission/message ID;
- worker assignment ID;
- backend-native job/task/pod/process ID;
- A-5 sport child execution ref.

A backend returning “accepted” does not prove the sport child operation started or succeeded.

### 9. Lost acknowledgement / ambiguous submission

Critical case:

```text
TDLA records dispatch intent
-> sends to backend
-> backend accepts/starts work
-> acknowledgement lost
-> TDLA restarts
```

A-10 must define backend reconciliation capability or safe handoff into A-11/A-12 so TDLA does not blindly submit a duplicate.

This is separate from the A-5 child-operation acknowledgement-loss case; both layers may exist.

### 10. Worker claim / lease semantics

Define semantic requirements for claiming queued work:

- one logical dispatch attempt can be physically observed/claimed more than once under failure;
- leases/claims are runtime coordination, not canonical attempt identity;
- expired lease does not automatically prove the prior worker stopped;
- lease loss cannot by itself authorize duplicate external side effects;
- exact persistence/lease algorithm remains A-13/A-21.

### 11. Worker heartbeat / liveness

Heartbeat absence means worker liveness is uncertain, not necessarily that child work terminated.

Distinguish:

- worker lost;
- backend job still running;
- sport child still running;
- result exists but worker died before reporting;
- truly never started.

Reconciliation must precede destructive retry decisions.

### 12. Worker crash before child dispatch

Expected behavior:

```text
attempt assigned
worker dies before invoking sport adapter
```

TDLA can eventually determine/recover without falsely assuming a child exists.

Exact retry attempt semantics remain A-11.

### 13. Worker crash after child dispatch

Expected behavior:

```text
sport child accepted
worker dies before persisting/reporting child ref
```

A-5 logical-idempotency/child-reconciliation contract must be usable to recover the child before another invoke.

A-10 must preserve the logical idempotency context in the immutable envelope.

### 14. Worker crash after result produced

Expected behavior:

```text
sport child terminal/result artifact exists
worker dies before TDLA marks attempt complete
```

Recovery/reconciliation should retrieve/validate the existing result rather than rerun merely because worker state is lost.

### 15. Synchronous vs asynchronous sport execution

A-10 must support both A-5 shapes:

- synchronous invocation returns terminal `SportExecutionResult`;
- asynchronous invocation returns child ref/ack and requires polling/event/reconciliation.

TDLA canonical attempt identity remains stable across transport shape.

### 16. Execution target immutability

Production worker must execute the exact immutable target declared by the resolved plan/envelope:

- image digest rather than mutable `latest`;
- immutable package/release/commit where appropriate;
- exact adapter implementation version/capability;
- validated config digest.

Worker may verify target digest before start and must fail closed on mismatch.

### 17. Input materialization / staging

Define generic worker responsibility for obtaining declared inputs without filename guessing:

- resolve input manifest refs;
- verify schema/digests;
- stage read-only/local copies when needed;
- preserve provenance refs;
- avoid mutating source evidence;
- output only through declared logical output/artifact contracts.

A-14 later owns artifact storage/retention details.

### 18. Secret handling boundary

ExecutionEnvelope contains stable secret/service-identity references only.

Worker obtains secret material through A-20-approved mechanism at runtime.

Secrets must not enter:

- Git;
- envelope semantic digest as raw values;
- logs;
- persisted safe diagnostics;
- output manifests.

### 19. Network/provider access classes

Some stages may require controlled egress or provider credentials while others should run isolated.

Worker capability matching must support generic network/access classes without encoding sport/provider business meaning in the control plane.

### 20. Side-effect classes / worker authorization

Customer-visible/destructive stages may require a worker/backend/service identity class authorized for that side-effect category.

Worker capability does not itself grant plan/certification/operator authority; all prior gates still apply.

### 21. Timeouts boundary

A-10 carries timeout/deadline policy references and enforces backend-level deadline signals as instructed, but exact retry/timeout state machine belongs to A-11.

A TDLA timeout does **not** prove the backend job or sport child stopped.

### 22. Cancellation boundary

Define separate states/evidence:

- cancellation requested;
- backend accepted cancellation;
- worker observed cancellation;
- sport child cancellation requested/accepted;
- child actually terminal;
- unable to cancel;
- cancellation status unknown.

Never equate “cancel request sent” with “side effects stopped.”

### 23. Result validation handoff

A backend/process exit code `0` or Prefect `Completed` is not semantic success.

A-10 must obtain/forward:

- A-5 `SportExecutionResult`;
- required A-6 output/artifact manifest refs;
- child execution ref;
- semantic result/degradation/failure status;
- backend/worker timing/evidence;
- output contract validation evidence.

A-12 later owns generalized failure/degradation propagation.

### 24. Backend reconciliation interface

Each production-capable backend should declare whether it supports reconciliation by:

- TDLA attempt/dispatch key;
- backend job handle;
- submission/idempotency token where applicable;
- worker assignment;
- A-5 child ref/logical idempotency context.

If a backend cannot safely reconcile ambiguous submission for a side-effecting production path, fail certification or require a proven compensating A-11 design.

### 25. Backend health / outage

Backend unavailable/capacity exhausted is operational state, not sport failure and not readiness state.

A-10 should expose generic dispatch dispositions such as conceptually:

- `DISPATCHABLE`;
- `WAITING_BACKEND`;
- `NO_COMPATIBLE_WORKER`;
- `BACKEND_UNAVAILABLE`;
- `SUBMISSION_AMBIGUOUS`;
- `SUBMITTED`;
- `RUNNING`;
- `RECONCILING`;
- `CANCEL_REQUESTED`;
- terminal transport/backend error.

Names can be refined during review.

### 26. Queue ordering

Do not assume global FIFO implies business priority or correctness.

A-15 later defines resource/priority policies. A-10 must preserve exact stage/deadline/authority context so a queued item can be rejected/revalidated if it becomes stale before start.

### 27. Queued work stale before worker start

Critical case:

```text
grant valid at enqueue
-> waits in queue
-> schedule/readiness/plan changes
-> worker receives item later
```

Worker/backend must not start merely because the message exists. Final current-authority/grant validation is required near the actual side-effect boundary.

### 28. Environment isolation

Development/test/staging/production worker pools/service identities/queues must be logically isolated enough that staging work cannot accidentally use production publication authority.

Exact deployment topology remains A-21.

### 29. Shadow/supervised/production

- shadow worker path must maintain no uncontrolled customer-visible side effects;
- supervised work must stop at declared approval boundary;
- production worker must verify production-authorized envelope/target/mode/service identity;
- worker backend cannot promote mode/certification itself.

### 30. Worker execution logs

Logs are operational evidence, not output authority.

Logs must include correlation IDs and sanitize secrets, but semantic success is based on versioned result/artifact contracts.

A-16 later owns telemetry standards.

### 31. Canonical execution-envelope digest

Define deterministic semantic hashing with schema-controlled field participation.

Physical worker hostname/pod UID/runtime log path should normally be audit metadata, not change the requested execution semantics.

Immutable target/config/input/grant/idempotency/environment/mode fields are semantic.

### 32. Result/output atomicity boundary

A worker may produce multiple artifacts before terminal result handoff.

A-10 should require an explicit final manifest/result commit point; partial files alone cannot be mistaken for successful outputs.

Exact object-store/database atomicity remains A-13/A-14.

### 33. Orphan detection

Define generic orphan possibilities:

- TDLA attempt says dispatched, backend has no job;
- backend job exists, TDLA worker record missing/stale;
- sport child exists but backend worker lost;
- child terminal but TDLA attempt nonterminal;
- backend job terminal but child state unknown.

A-10 must preserve enough handles to reconcile; A-12 owns final recovery policy.

### 34. Backend replacement neutrality

Migrating from local/Docker/Prefect to Kubernetes/queue worker must not change:

- StageRun identity;
- logical operation identity;
- A-9 eligibility evidence;
- A-11 idempotency semantics;
- sport child identity;
- historical audit meaning.

### 35. No direct worker authority

Prohibit:

```text
worker receives message -> trust it -> run
```

Require conceptually:

```text
DispatchEligibilityGrant
+ current-authority revalidation
+ A-11 logical idempotency/attempt authority
+ immutable ExecutionEnvelope
+ compatible authorized backend/worker
    -> physical invocation
```

---

# A-10 stress cases before certification

At minimum test:

1. Valid current grant dispatches to compatible local/test worker.
2. Grant expired while waiting in queue.
3. Schedule revision changes after enqueue before worker start.
4. Readiness expires after enqueue before worker start.
5. Upstream output retracted after enqueue.
6. Plan revision supersedes queued work.
7. Worker capability mismatch.
8. No authorized production worker available.
9. GPU-required stage with only CPU workers.
10. Production stage accidentally routed toward staging worker pool.
11. Immutable image digest available and verified.
12. Worker sees mutable `latest` target in production -> fail closed.
13. Input manifest digest mismatch before execution.
14. Required input missing from artifact storage.
15. Worker obtains secrets through reference without persisting raw value.
16. Secret accidentally appears in adapter error/log -> sanitization/incident boundary.
17. Dispatch intent persisted; worker crashes before adapter invocation.
18. Backend accepts submission but acknowledgement is lost.
19. Worker invokes async sport child; worker dies before persisting child ref.
20. Worker invokes async child and records child ref, then dies.
21. Sport child completes successfully while worker is dead.
22. Sport child fails while worker is dead.
23. Synchronous adapter returns semantic success plus valid outputs.
24. Synchronous process exit code 0 but required result/output contract missing.
25. Prefect/backend says Completed but sport semantic result is failed/degraded.
26. Backend job fails before sport child invocation.
27. Worker heartbeat lost while backend job still running.
28. Worker heartbeat lost while sport child still running independently.
29. Lease expires; previous worker might still be running.
30. Two workers observe/claim same physical dispatch work.
31. Duplicate queue message for same dispatch/attempt.
32. Backend submission reconciliation finds existing job after acknowledgement loss.
33. Backend cannot reconcile ambiguous side-effecting submission.
34. A-5 child reconciliation finds existing child after worker loss.
35. Cancellation requested before worker starts.
36. Cancellation requested after backend job starts but before child invocation.
37. Cancellation requested after sport child starts; child declines/unsupported.
38. Backend accepts cancellation but child continues.
39. Timeout reached but backend/child status is unknown.
40. Worker produces partial files then crashes before final manifest/result.
41. Worker produces final manifest/result then crashes before TDLA acknowledgement.
42. Result manifest schema mismatch.
43. Result digest mismatch.
44. Shadow compute runs on isolated worker and cannot publish.
45. Supervised compute finishes and waits at explicit approval boundary.
46. Production customer-visible stage uses authorized service identity/backend.
47. Same StageRun later uses a different physical worker backend after a retry attempt; canonical identity remains stable according to A-11 semantics.
48. Backend migration Prefect -> Kubernetes preserves TDLA identity/audit contracts.
49. Worker instance/pod restarts and gets a new physical ID; attempt lineage remains intact.
50. Backend outage/capacity exhaustion delays work without becoming sport failure.
51. Queue FIFO order conflicts with deadline priority; correctness still uses plan/deadline authority, not queue position.
52. Queued message becomes past deadline before claim.
53. Stale superseded queued message is delivered after current replacement already ran.
54. Duplicate backend completion callback.
55. Out-of-order backend running/completed callbacks.
56. Backend reports terminal success but child reconciliation says still running/unknown.
57. Child terminal result exists but backend native job record disappeared.
58. Worker class descriptor changes incompatibly while work queued.
59. ExecutionEnvelope semantic fields serialize differently but canonical digest stays deterministic.
60. Physical worker metadata changes without changing semantic envelope digest when schema classifies it audit-only.

## Expected A-10 outputs

Create at minimum:

- `docs/architecture/A10_WORKER_EXECUTION_BACKEND_V1.md`;
- A-10 V1.1 addendum if review exposes ambiguities;
- A-10 architecture conformance/certification review with stress matrix;
- ADR if dispatch-intent/backend-reconciliation/execution-envelope authority introduces a durable tradeoff;
- updated ADR index;
- updated architecture index;
- updated `ARCHITECTURE_CERTIFICATION_LOG.md`;
- detailed `CHANGE_JOURNAL.md` entry;
- updated root `README.md`;
- updated `CURRENT_RESUME_POINT.md` pointing to A-11.

## Do not do yet

Until A-10 is certified:

- do not implement final worker/backend Pydantic models as frozen authority;
- do not create production Prefect deployments/work pools;
- do not add Kubernetes Jobs/queues/Celery workers as production architecture;
- do not design PostgreSQL dispatch/lease/outbox tables around guessed fields;
- do not wire live Daily-MLB/NFL/NCAAF execution into TDLA;
- do not choose backend-native job IDs as canonical RunAttempt identity;
- do not let queue delivery bypass A-9 grant/current-authority validation;
- do not finalize A-11 retry/idempotency key construction prematurely;
- do not enable production publication.

## Required reading for next session

1. `README.md`
2. `AGENTS.md`
3. this file
4. `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`
5. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_V1.md`
6. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md`
7. `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`
8. `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md`
9. `docs/architecture/A09_DEPENDENCY_READINESS_ENGINE_V1.md`
10. `docs/architecture/A09_DEPENDENCY_READINESS_ENGINE_ADDENDUM_V1_1.md`
11. `docs/implementation/A09_ARCHITECTURE_CONFORMANCE_REVIEW_20260905.md`
12. `docs/adr/ADR-0006_VERSION_BOUND_DISPATCH_ELIGIBILITY_AND_FINAL_REVALIDATION.md`
13. current A-5 child reconciliation/idempotent invocation requirements;
14. A-8 timing/deadline/current-authority rules.

The next architecture checkpoint is **A-10 Worker / Execution Backend Architecture**.
