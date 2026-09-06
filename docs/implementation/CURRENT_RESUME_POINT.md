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
- A-10 Worker / Execution Backend V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-10 review evidence: `docs/implementation/A10_ARCHITECTURE_CONFORMANCE_REVIEW_20260905.md`.
- ADR-0001: TDLA canonical identity / replaceable orchestration runtime.
- ADR-0002: transport-neutral Sport Automation Adapter protocol.
- ADR-0003: immutable plan fragments / explicit composition / resolved-plan authority.
- ADR-0004: durable trigger evidence / reevaluation-only trigger authority.
- ADR-0005: stable schedule slots / immutable resolved-time authority / reevaluation-only due events.
- ADR-0006: version-bound dispatch eligibility / mandatory final current-authority revalidation.
- ADR-0007: immutable execution envelope / durable and reconciliable backend dispatch.
- No production implementation milestone is certified.
- No TDLA automation is production-authoritative.
- Daily-MLB remains manual-first; later automation must prove equivalence after its final manual production pipeline is certified.

## Certified nested architecture through A-10

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
                                       |
                                       v
                           DispatchEligibilityGrant
                         (version-bound, non-bearer)
                                       |
                                       v
                        A-10 preflight validation
                                       |
                                       v
                           A-11 logical operation /
                             RunAttempt authority NEXT
                                       |
                                       v
                         A-10 ExecutionEnvelope
                                       |
                                       v
                        A-10 FINAL authority recheck
                                       |
                                       v
                     durable DispatchRecord / intent
                                       |
                                       v
                   replaceable worker/backend submission
                                       |
                      +----------------+----------------+
                      |                                 |
                      v                                 v
              backend ExecutionHandle          A-5 sport child ref
                                                        |
                                                        v
                                       semantic result + manifests
                                                        |
                                                        v
                                      DDC/provider evidence where used
```

## Important locked A-9 rules

1. `READY` is derived immutable evidence, not a persistent mutable boolean.
2. A-5 sport `READY` is only one readiness gate and never direct TDLA execution authority.
3. A-9 checks current plan/materialization/scope/schedule/mode/policy authority before and after evidence collection.
4. Dependency satisfaction binds exact upstream StageRun/materialization/output manifest/schema/digest/provenance authority.
5. Upstream output supersession/retraction invalidates dependent current eligibility/grants before dispatch.
6. `OPTIONAL`, `NO_OP`, `NOT_APPLICABLE`, and `SUCCEEDED_DEGRADED` satisfy only explicit compatible contracts.
7. Fan-in binds exact A-6 `ScopeSetBinding` membership revision/digest.
8. A-5 sport reason codes remain opaque; technical readiness failure is not sport waiting/blocked/ready.
9. Readiness cache validity is the intersection of all freshness/authority bounds and is revision-sensitive.
10. `DispatchEligibilityGrant` is immutable version-bound evidence and never a bearer execution token.
11. Grant validity cannot outlive the strictest readiness/time/window/policy/current-authority boundary.
12. A-10/A-11 must revalidate grant witnesses/current authority before dispatch.
13. A-9 does not create StageRun/RunAttempt or replace A-11 final logical idempotency authority.

## Important locked A-10 rules

1. A worker/backend is an execution mechanism, not workflow authority.
2. TDLA WorkflowRun/StageRun/RunAttempt identity remains separate from Prefect/Docker/Kubernetes/queue/message/process/backend identity.
3. A-10 performs A-9 grant/current-authority preflight and a second **final** current-authority revalidation immediately before irreversible backend submission.
4. An existing RunAttempt does not override newly stale plan/scope/schedule/dependency/readiness/policy authority.
5. Every physical attempt uses one immutable schema-versioned `ExecutionEnvelope` with exact plan/stage/scope/grant/target/adapter/config/input/output/environment/mode/A-11 idempotency authority.
6. Durable TDLA `DispatchRecord`/intent exists before backend submission; exact outbox/transaction DDL remains A-13.
7. One A-11-authorized RunAttempt has a stable backend-submission identity for safe ambiguous-ack reconciliation/idempotent retransmission where supported.
8. Backend request/message/callback IDs are transport evidence, not new logical submissions or RunAttempts.
9. Backend submission acknowledgement loss and A-5 sport-child acknowledgement/reference loss are two independent ambiguity layers; both must be recoverable or fail closed.
10. `WorkerClassRef` is stable logical capability; physical worker instance/hostname/pod/container is ephemeral provenance.
11. Worker/backend capability and environment/mode/side-effect authorization are revalidated at actual assignment/start; descriptor drift can invalidate an old assignment.
12. Duplicate queue delivery/claim, lease expiry, or heartbeat loss does not prove prior worker/backend/child stopped and cannot by itself authorize retry.
13. A-5 child logical-idempotency context remains in the envelope so a child accepted before worker failure can be recovered.
14. Timeout means elapsed policy boundary, not proof backend/child stopped.
15. Cancellation requested/accepted/worker-observed/child-requested/child-terminal are distinct evidence; cancel acknowledgement is not terminal truth.
16. Cancellation/completion races still require terminal result reconciliation.
17. Backend callbacks are observations; duplicate/out-of-order callbacks cannot roll authoritative state backward by receipt order.
18. Process exit 0, Prefect `Completed`, Kubernetes Job Complete, or queue acknowledgement never equals semantic StageRun success.
19. Terminal semantic result/manifests must correlate to the exact StageRun/RunAttempt, ExecutionEnvelope, plan/stage/scope, logical idempotency, and A-5 child/synchronous invocation authority.
20. Partial or unrelated files cannot become terminal output merely because filenames/hashes resemble expected output.
21. Backend ExecutionHandle and A-5 sport child ref remain distinct logical roles even when one direct-service implementation uses the same opaque external ID.
22. Stale queued work must fail current-authority validation near physical start.
23. Backend outage/capacity is operational state, not sport readiness/failure.
24. Backend replacement must preserve TDLA canonical identity, A-9 evidence, A-11 idempotency, A-5 child identity, and historical audit meaning.

## Daily-MLB / football compatibility note that must not be forgotten

Current Daily-MLB remains manual-first and is not production-automated because A-10 is certified.

Future M13/M14 MLB integration may use an authenticated service, container, Prefect/Kubernetes worker, or another certified backend, but it must preserve:

- certified final manual MLB behavior;
- A-5 caller-stable logical child idempotency/reconciliation;
- A-6 immutable plan/stage/output contracts;
- A-9 current eligibility/freshness;
- A-10 immutable ExecutionEnvelope and durable backend dispatch identity;
- exact semantic result/output validation;
- shadow/supervised/production side-effect separation.

NFL/NCAAF may use different worker classes/backends without generic TDLA learning football-specific execution meaning.

---

# Exact next step — A-11 Retry / Timeout / Idempotency Architecture

Design the canonical logical-execution identity and retry state machine that guarantees duplicate trigger/evaluation/queue/backend delivery and transient failures do not create duplicate logical sport work or duplicate external effects.

The central A-11 rule should be:

> **A retry is a new physical `RunAttempt` of the same logical StageRun/operation, carrying the same stable logical idempotency identity. Timeout, lease loss, heartbeat loss, missing acknowledgement, or unknown state is not proof the prior attempt/child/side effect disappeared. Reconciliation and current-authority revalidation come before any retry that could duplicate work.**

A-11 must define exact logical/idempotency semantics while leaving generalized failure/degradation recovery policy to A-12 and PostgreSQL uniqueness/outbox mechanics to A-13.

## A-11 must define at minimum

### 1. Logical operation identity

Freeze the exact concept that represents **one intended logical execution** of a StageMaterialization under a specific lineage.

Potential contract:

```text
LogicalOperationIdentity
- namespace/schema version
- environment
- execution lineage kind
- workflow_run/logical workflow identity
- stage_materialization_ref
- resolved plan/stage authority
- sport scope/scope revision as already bound by materialization
- replay/backfill/reprocess lineage ref when applicable
- logical operation digest/key
```

The exact formula should avoid depending on physical attempt IDs, backend IDs, timestamps, or mutable targets.

### 2. StageRun uniqueness

Define when duplicate requests converge on the same logical StageRun vs create a new logical operation.

At minimum:

- duplicate timer/trigger/reevaluation cause -> same StageRun;
- duplicate queue/backend submission -> same StageRun;
- retry after transient failure -> same StageRun, new RunAttempt;
- lost backend acknowledgement -> same StageRun/RunAttempt while reconciling the same submission;
- lost A-5 child acknowledgement -> same StageRun/RunAttempt/logical child identity;
- explicit replay -> new lineaged logical operation;
- reprocess with changed code/model/config -> new lineaged logical operation;
- backfill historical operation -> separate backfill lineage;
- superseding plan/stage materialization -> new authority/logical operation as declared by A-6/A-14.

### 3. Stable LogicalIdempotencyKey

A-11 must freeze a canonical, versioned, deterministic logical idempotency key for the StageRun operation.

Requirements:

- stable across all RunAttempts of the same StageRun;
- stable across worker/backend changes for the same logical operation;
- supplied through A-10 ExecutionEnvelope;
- propagated into A-5 child invocation/dedup lookup;
- safe to persist/log in sanitized form;
- no secrets/raw credentials;
- collision-resistant and namespace/version scoped;
- distinct across replay/reprocess/backfill lineages and distinct StageMaterializations.

Do **not** include `attempt_id` in the logical idempotency key.

### 4. Idempotency-key hierarchy

Explicitly distinguish at least:

```text
LogicalOperationKey / LogicalIdempotencyKey
    = stable across retries of StageRun

RunAttempt identity
    = new physical TDLA attempt when A-11 authorizes a retry

BackendSubmissionKey
    = stable submission authority inside one RunAttempt

A-5 child logical idempotency key
    = derived/bound from stable logical operation identity,
      not physical attempt identity

external side-effect idempotency key(s)
    = stable logical effect identity where supported
```

Define which keys are reused vs regenerated at each layer.

### 5. Exactly-once terminology

Do not claim exactly-once transport/execution in a distributed system unless the external system contract truly provides it.

Prefer explicit guarantees such as:

- at-least-once delivery + idempotent logical acceptance;
- effectively-once logical operation/side effect under certified dedup/reconciliation;
- duplicate transport evidence retained.

### 6. RunAttempt identity and sequence

Define immutable physical attempts under one StageRun:

```text
StageRun S
  RunAttempt 1
  RunAttempt 2
  RunAttempt 3
```

Each attempt has:

- unique attempt ID;
- monotonic attempt ordinal/sequence within StageRun;
- immutable attempt policy/envelope/dispatch refs;
- start/end/reconciliation evidence;
- parent/prior attempt lineage;
- exact reason a new attempt was authorized.

Concurrent systems must not create conflicting attempt ordinals/duplicate active attempts for the same logical operation without explicit architecture allowance.

Exact uniqueness DDL remains A-13.

### 7. New-attempt authorization gate

A new RunAttempt may be created only after A-11 can prove the prior attempt is in a state whose bound policy permits another attempt.

Examples:

- confirmed backend rejection before child creation;
- confirmed child terminal retryable technical failure under policy;
- confirmed no backend submission/child exists;
- prior attempt cancelled/terminal with safe retry policy;
- retry budget/deadline/current authority still permit proceed.

Unknown/ambiguous prior state is **not** automatically retryable.

### 8. Single active attempt / overlap policy

Define the default V1 invariant for whether more than one active RunAttempt of one StageRun may exist simultaneously.

Recommended default:

> one active attempt per logical StageRun unless a future explicitly certified speculative/hedged-execution policy exists.

Duplicate HA coordinators must converge rather than intentionally race attempts.

### 9. Current-authority revalidation before every attempt

Every new retry attempt must obtain/reuse only current valid A-9 eligibility evidence according to A-9/ADR-0006.

A retry cannot inherit stale permission from attempt 1 if:

- schedule changed;
- readiness expired;
- upstream output retracted;
- plan superseded;
- deadline passed;
- policy/mode changed.

### 10. Retry policy binding

Every StageRun/attempt must bind immutable retry policy identity/version/digest from the A-6 resolved policy authority.

Policy may define:

- max attempts;
- total retry elapsed budget;
- retryable transport/error classes;
- backoff schedule;
- jitter behavior;
- start/deadline constraints;
- cancellation-before-retry requirements;
- reconciliation requirements;
- side-effect safety requirements.

Moving a mutable `current_retry_policy` alias after a StageRun begins must not silently alter historical behavior.

### 11. Retry budget

Define bounded retry behavior using at least:

- maximum attempt count;
- maximum total elapsed retry window/budget;
- A-8 stage deadline/validity window;
- optional per-error limits;
- operator/manual escalation boundary.

No unbounded automatic retries.

### 12. Backoff / jitter semantics

Define a versioned generic retry-delay policy.

Possible families:

- fixed;
- exponential;
- exponential with bounded jitter;
- provider/backend hint (`retry_after`) constrained by policy;
- no automatic retry.

The policy must be reproducible/auditable enough to explain when another attempt became eligible without requiring retry wakeup timestamps to become logical operation identity.

### 13. Timeout taxonomy

Do not use one generic `timeout` for all layers.

Define at least conceptually:

- eligibility/grant handoff expiry;
- queue wait/start timeout;
- backend submission acknowledgement timeout;
- backend start timeout;
- worker heartbeat/liveness timeout;
- sport child execution timeout;
- result retrieval/validation timeout;
- cancellation acknowledgement timeout;
- overall attempt deadline;
- stage/window hard deadline.

Each timeout means only what its layer can prove.

### 14. Timeout is evidence, not terminal proof

Certified invariant:

```text
timeout observed
!= backend stopped
!= worker stopped
!= sport child stopped
!= external side effect absent
!= safe retry
```

A timeout generally routes to reconciliation/cancellation/unknown handling before a new attempt.

### 15. Ambiguous backend submission

If A-10 backend submission acknowledgement is lost:

- preserve same RunAttempt;
- reuse same stable `BackendSubmissionKey`;
- reconcile backend by submission/attempt identity;
- safe idempotent retransmission, if supported, uses same submission identity;
- do not create RunAttempt N+1 merely because the acknowledgement timed out.

### 16. Ambiguous A-5 child creation

If the backend/worker reached A-5 child invocation but child acknowledgement/ref was lost:

- preserve same logical StageRun and logical idempotency key;
- use A-5 lookup/reconciliation by logical child idempotency identity;
- `ALREADY_EXISTS`/found child is normal recovery;
- do not create a second child because physical attempt identity changed.

### 17. Backend vs child retry ownership

Define nested retry ownership so TDLA does not multiply retries already happening inside sport/DDC/provider layers.

At minimum distinguish:

- TDLA RunAttempt retry;
- backend transport submission retransmission of same RunAttempt;
- sport-service internal child attempt/retry under one logical child;
- DDC provider/acquisition internal retries;
- provider SDK/network retries.

Each layer must have bounded responsibility; inner retries do not automatically become new TDLA RunAttempts.

### 18. Technical vs semantic failure retryability

A-11 should define generic retry mechanics/categories without interpreting sport meaning.

Examples:

- network/transport transient failure may be retryable;
- backend capacity/unavailable may defer/retry;
- malformed immutable contract/result likely terminal until authority changes;
- sport semantic failure/degraded result is not automatically retryable;
- sport-defined blocked/readiness state is not a RunAttempt failure;
- broad failure/degradation/recovery action remains A-12.

### 19. Retryability evidence

A new attempt should retain structured evidence explaining:

- prior attempt/result state;
- reconciliation result;
- retryability classification;
- retry policy/version;
- budget remaining;
- current A-9 eligibility/grant;
- scheduled retry eligibility time;
- operator action if any.

### 20. Side-effect idempotency / fencing

For side-effecting stages, define a stable logical external-effect identity separate from physical attempts.

Examples later may include publication, notification, destructive external operation, or write to another service.

Requirements:

- reuse the same external-effect idempotency identity across retries of the same intended effect;
- never key external effect on physical `attempt_id`;
- where the external system supports native idempotency keys, use them;
- where it does not, require a certified durable wrapper/fence/receipt design before production automation;
- unknown effect outcome blocks blind duplicate effect.

A-18 will specialize publication receipts/keys.

### 21. Partial side effects / unknown side effects

If an attempt may have created a side effect but acknowledgement is missing:

- do not retry the effect blindly;
- reconcile by external receipt/idempotency key when possible;
- record `UNKNOWN_EFFECT`/equivalent operational state if unresolved;
- A-12/A-19 later own recovery/escalation.

### 22. Idempotency collision handling

A key collision where one key maps to incompatible semantic payload/authority must fail closed.

Examples:

- same logical key but different stage materialization;
- same child key but different immutable target/config/input authority;
- same side-effect key but different publication package.

Do not silently treat incompatible content as `ALREADY_EXISTS`.

### 23. Idempotency semantic payload digest

Consider binding each idempotency record to a semantic request digest so `ALREADY_EXISTS` can be validated as the **same** intended operation rather than only the same text key.

This should cover exact execution-semantic authority required to detect key misuse/collision without making physical attempt metadata semantic.

### 24. Attempt policy after backend switch

Switching physical backend/worker during a later retry does not reset:

- StageRun logical identity;
- logical idempotency key;
- retry budget;
- side-effect idempotency identity;
- historical attempt lineage.

A new backend may require a new per-attempt BackendSubmissionKey because it is a new RunAttempt, but the logical operation identity remains stable.

### 25. Retry after worker/lease/heartbeat loss

Lease/heartbeat expiry alone cannot authorize a new RunAttempt.

Required sequence:

```text
worker/lease uncertain
-> backend reconciliation
-> A-5 child reconciliation when applicable
-> result reconciliation
-> only then classify prior attempt retryability
```

### 26. Retry after timeout + cancellation

A timeout followed by cancellation request still requires proof/reconciliation of terminal state.

`cancel accepted` does not automatically authorize next attempt while child may continue.

### 27. Deadline/window interaction

Retry cannot bypass A-8 timing authority.

If backoff/reconciliation pushes beyond deadline:

- no new normal attempt unless current missed-window/current-authority policy permits it;
- customer-visible/destructive work gets no generic catch-up permission;
- record retry budget/deadline exhaustion distinctly.

### 28. Scheduled retry wakeup identity

A retry timer/wakeup is a cause to reevaluate retry eligibility, not a new logical operation or permission to dispatch.

It should use A-7/A-8-style durable event principles where applicable.

### 29. Concurrent retry coordinators / HA

Two coordinators may simultaneously decide a retry might be due.

They must converge on one authorized next attempt ordinal/identity rather than create two active RunAttempts.

Exact database compare-and-set/unique constraint remains A-13.

### 30. Attempt terminality / immutability

Completed attempt evidence is immutable.

A later reconciliation correction should append/version state/evidence rather than rewrite history as though uncertainty never existed.

Define how canonical current attempt status can advance while preserving the full event/evidence trail.

### 31. Result after timeout

A sport child/result may arrive after TDLA marked a timeout/reconciliation state.

The actual terminal result must be reconciled and recorded; timeout does not erase it.

Retry must not already have created duplicate logical work unless safe overlap was explicitly certified.

### 32. Duplicate terminal callbacks

Repeated backend/child/result completion delivery should converge on one terminal attempt/result authority while retaining duplicate delivery evidence where useful.

### 33. Out-of-order retry/result events

An old retry wakeup or running callback arriving after terminal success cannot reopen the StageRun or create a new attempt.

### 34. Retry after terminal semantic success

Ordinary retry is forbidden once StageRun is successfully satisfied.

Replay/reprocess/backfill are separate A-14 lineages.

### 35. Retry after terminal semantic failure

Whether a semantic sport failure warrants another attempt depends on explicit generic retry/failure policy and A-12 classification; A-11 does not invent sport-specific retriability.

### 36. Operator retry boundary

An operator request to retry:

- cannot bypass stable logical idempotency;
- cannot bypass unresolved prior attempt/side-effect ambiguity;
- cannot bypass current A-9/A-8 authority by default;
- is distinct from replay/reprocess;
- explicit overrides remain A-19 and must be separately audited.

### 37. Policy supersession during StageRun

Production StageRun should retain immutable retry policy version/digest used for its logical operation unless a certified explicit policy-transition mechanism creates new authority.

A mutable alias change does not silently reset budget/backoff/retryability.

### 38. Retry budget exhaustion

Distinguish:

- terminal technical failure;
- retry budget exhausted;
- deadline/window exhausted;
- unresolved ambiguous prior effect;
- current authority superseded;
- operator review required.

A-12/A-17/A-19 later decide escalation/incident/manual recovery.

### 39. Retry counters and nested retries

TDLA attempt count must not accidentally count every inner HTTP/provider retry as a new RunAttempt.

Retain nested retry evidence/provenance where exposed, but each layer's counters remain separate.

### 40. Idempotency and replay/reprocess/backfill

Replay, reprocess, and backfill must not reuse the original production logical idempotency key as if they were the same logical operation.

They need explicit lineage-scoped identities while still preserving links to the original run/evidence.

A-14 later freezes artifact/input semantics for these modes.

### 41. Key privacy / security

Idempotency identities must not include raw secrets, credentials, protected payload data, or mutable tokens.

Hashing/serialization must be deterministic and safe for logs/diagnostics.

### 42. Technology neutrality

Do not make logical retry/idempotency authority depend on:

- Prefect retry count;
- Celery retry ID;
- queue redelivery count;
- Kubernetes restart count;
- process PID;
- Redis lock key;
- provider SDK retry counter.

These may be runtime evidence/cross-references only.

### 43. Recovery after coordinator crash

Durable StageRun/RunAttempt/idempotency/retry evidence must allow restart to determine:

- current logical operation;
- latest/active attempt;
- whether backend submission exists;
- whether child exists;
- whether result exists;
- budget remaining;
- next retry eligibility;
- whether current authority is still valid.

Exact persistence DDL remains A-13.

### 44. Fail-closed rules

A-11 must fail closed for at least:

- idempotency key collision with incompatible semantic digest;
- unknown prior attempt/side-effect state without safe reconciliation;
- concurrent active-attempt conflict;
- exhausted retry budget;
- stale A-9 authority;
- deadline/window closed;
- missing immutable retry policy;
- external side-effect path with no certified idempotency/reconciliation mechanism;
- child/backend lookup inconsistency that cannot be reconciled.

---

# A-11 stress cases before certification

At minimum test:

1. Duplicate trigger causes converge on one logical StageRun.
2. Duplicate eligibility evaluations converge on one logical StageRun.
3. Retry after confirmed transient backend failure creates RunAttempt 2 under same StageRun.
4. RunAttempt 2 uses same LogicalIdempotencyKey as attempt 1.
5. RunAttempt 2 gets a new RunAttempt ID and ordinal.
6. Backend switch on attempt 2 does not reset logical key/retry budget.
7. Physical attempt ID is accidentally included in child idempotency key -> fail contract test.
8. Duplicate queue delivery for attempt 1 does not create attempt 2.
9. Backend ack timeout with ambiguous submission keeps attempt 1 in reconciliation.
10. Backend reconciliation finds existing job; no new attempt.
11. Safe idempotent backend retransmission reuses same BackendSubmissionKey.
12. Backend reconciliation proves no submission existed and policy permits retry/new attempt.
13. Backend ambiguous and cannot reconcile side-effecting submission -> no automatic retry.
14. Worker dies before A-5 invocation and reconciliation proves no child.
15. Worker dies after child acceptance before child ref persisted; A-5 lookup finds existing child.
16. A-5 returns `ALREADY_EXISTS` for same logical child; treat as normal recovery.
17. Same child idempotency key is presented with incompatible target/config/input digest -> fail closed.
18. Child continues running after TDLA timeout.
19. Timeout occurs, cancel requested, child later succeeds.
20. Timeout occurs, cancel accepted by backend, child still runs.
21. Heartbeat lost but backend job running; no retry yet.
22. Lease expires while original worker still running; no duplicate attempt.
23. Child terminal result arrives after timeout state; reconcile result.
24. Attempt 1 succeeds while retry wakeup for attempt 2 is queued; retry wakeup becomes no-op/terminal current state.
25. Duplicate child terminal callbacks converge on one attempt result.
26. Out-of-order RUNNING callback arrives after terminal success; cannot reopen attempt.
27. Retry policy max attempts = 3; fourth attempt rejected.
28. Total retry elapsed budget expires before max attempt count.
29. Stage hard deadline expires during backoff.
30. Retry becomes due but A-9 readiness has expired -> reevaluate, no blind dispatch.
31. Retry becomes due but schedule revision changed -> new current authority required.
32. Retry becomes due but upstream output retracted -> no dispatch.
33. Plan superseded between attempts -> old StageRun does not continue normal retry under new plan.
34. Retry policy alias changes after attempt 1; pinned immutable policy remains authoritative.
35. Fixed backoff policy produces declared next eligible retry time.
36. Exponential+jitter policy stays within versioned bounds and is auditable.
37. Provider `retry_after` exceeds stage deadline -> no retry beyond current authority.
38. Backend capacity outage delays retry without becoming sport semantic failure.
39. Technical readiness `WAITING` is not counted as failed RunAttempt.
40. A-5 readiness call timeout before dispatch does not create a RunAttempt if no attempt authority/submission occurred.
41. Semantic sport `FAILED` result is not automatically retryable without policy/A-12 classification.
42. `SUCCEEDED_DEGRADED` accepted by output policy completes StageRun; no retry merely to seek non-degraded output unless explicitly separate reprocess policy.
43. Process exit 0 but missing semantic result -> retryability classified technically, not success.
44. Partial files exist after crash, no final manifest; no false success.
45. Final correlated manifest exists after worker crash; retrieve it instead of retrying.
46. Customer-visible side effect acknowledgement lost but external receipt lookup finds existing effect -> no duplicate effect.
47. Customer-visible effect outcome unknown and system has no idempotency lookup -> stop automatic retry/escalate.
48. External effect idempotency key accidentally includes RunAttempt ID -> fail contract test.
49. Same external effect key with different semantic publication/effect digest -> collision fail closed.
50. Operator presses retry while previous attempt state ambiguous -> cannot bypass reconciliation.
51. Operator retry after confirmed retryable terminal failure still uses same logical StageRun/idempotency key.
52. Explicit replay creates new lineaged logical operation/key, not attempt N+1 of production StageRun.
53. Explicit reprocess creates new lineaged operation/key with changed target/config authority.
54. Backfill historical run uses backfill lineage/key distinct from original production run.
55. Two HA retry coordinators race to create next attempt; only one attempt ordinal becomes authoritative.
56. Coordinator crashes after RunAttempt creation before backend submission; recovery sees no submission and handles same attempt safely.
57. Coordinator crashes after backend submission before recording ack; recovery uses same attempt/BackendSubmissionKey.
58. Retry wakeup is delivered twice; does not create two attempts.
59. Prefect/Celery/Kubernetes native retry counter changes without changing TDLA logical attempt authority.
60. Same semantic logical operation canonicalizes to the same LogicalIdempotencyKey across equivalent serialization/order.
61. Different StageMaterialization never collides to same logical key.
62. Same StageMaterialization in staging vs production gets distinct environment-scoped logical identity.
63. Same production StageRun retries on a different worker host; logical key unchanged.
64. A-5 sport service performs internal network/provider retries while TDLA remains on RunAttempt 1.
65. DDC provider acquisition retries remain nested and do not increment TDLA RunAttempt count.
66. Retry budget exhausted -> explicit exhausted disposition, no hidden infinite retry.
67. Deadline exhausted before side-effect retry -> no generic catch-up.
68. Cancel request is accepted but terminal state unknown -> retry remains blocked.
69. Prior attempt definitely cancelled before any child/effect and policy permits retry -> next attempt authorized.
70. Idempotency key/payload digest record is corrupted/mismatched -> fail closed and incident/recovery boundary.

---

# Expected A-11 outputs

Create at minimum:

- `docs/architecture/A11_RETRY_TIMEOUT_IDEMPOTENCY_V1.md`;
- A-11 V1.1 addendum if review exposes ambiguities;
- A-11 architecture conformance/certification review with stress matrix;
- ADR if logical-operation identity, key hierarchy, single-active-attempt, or exactly-once/effect-fencing semantics introduce durable tradeoffs;
- updated ADR index;
- updated architecture index;
- updated `ARCHITECTURE_CERTIFICATION_LOG.md`;
- detailed `CHANGE_JOURNAL.md` entry;
- updated root `README.md`;
- updated `CURRENT_RESUME_POINT.md` pointing to A-12.

## Do not do yet

Until A-11 is certified:

- do not implement final StageRun/RunAttempt/idempotency Pydantic models as frozen authority;
- do not create retry loops/backoff policies in Prefect/Celery/queues as production authority;
- do not design PostgreSQL unique/idempotency/attempt/outbox tables around guessed key fields;
- do not wire live Daily-MLB/NFL/NCAAF retry automation;
- do not use physical `attempt_id` as sport child or external-effect idempotency identity;
- do not treat timeout/lease/heartbeat/cancel acknowledgement as proof prior work stopped;
- do not permit automatic retry of ambiguous side effects without reconciliation/fencing;
- do not implement A-12 generalized recovery policy prematurely;
- do not enable production publication.

## Required reading for next session

1. `README.md`
2. `AGENTS.md`
3. this file
4. `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`
5. `docs/architecture/A03`/foundation run-identity rules in `A00-A04_AUTOMATION_FOUNDATION_V1.md` + addendum
6. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_V1.md`
7. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md`
8. `docs/architecture/A09_DEPENDENCY_READINESS_ENGINE_V1.md`
9. `docs/architecture/A09_DEPENDENCY_READINESS_ENGINE_ADDENDUM_V1_1.md`
10. `docs/architecture/A10_WORKER_EXECUTION_BACKEND_V1.md`
11. `docs/architecture/A10_WORKER_EXECUTION_BACKEND_ADDENDUM_V1_1.md`
12. `docs/implementation/A10_ARCHITECTURE_CONFORMANCE_REVIEW_20260905.md`
13. `docs/adr/ADR-0006_VERSION_BOUND_DISPATCH_ELIGIBILITY_AND_FINAL_REVALIDATION.md`
14. `docs/adr/ADR-0007_IMMUTABLE_EXECUTION_ENVELOPE_AND_RECONCILABLE_BACKEND_DISPATCH.md`
15. current A-5 child idempotency/reconciliation requirements.

The next architecture checkpoint is **A-11 Retry / Timeout / Idempotency Architecture**.
