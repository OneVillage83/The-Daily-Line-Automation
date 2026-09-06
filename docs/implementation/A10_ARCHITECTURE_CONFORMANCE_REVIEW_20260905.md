# A-10 Architecture Conformance Review — Worker / Execution Backend Architecture

Review date: 2026-09-05  
Repository: `OneVillage83/The-Daily-Line-Automation`

Reviewed architecture:

- `docs/architecture/A10_WORKER_EXECUTION_BACKEND_V1.md`
- `docs/architecture/A10_WORKER_EXECUTION_BACKEND_ADDENDUM_V1_1.md`
- `docs/adr/ADR-0007_IMMUTABLE_EXECUTION_ENVELOPE_AND_RECONCILABLE_BACKEND_DISPATCH.md`

Foundation dependencies reviewed for consistency:

- A-0 through A-4 certified foundation;
- A-5 Sport Automation Adapter V1 + V1.1;
- A-6 Pipeline Plan / Stage Contracts V1 + V1.1;
- A-7 Trigger Architecture V1 + V1.1;
- A-8 Event-Relative Scheduling Engine V1 + V1.1;
- A-9 Dependency / Readiness Engine V1 + V1.1;
- ADR-0001 through ADR-0006;
- `AGENTS.md` repository constitution.

## Review purpose

A-10 must establish a production-grade execution-plane contract without making Prefect, Docker, Kubernetes, queues, hostnames, process IDs, worker leases, or backend callbacks canonical TDLA authority.

The review tests:

1. TDLA vs sport/DDC ownership;
2. A-9 grant/current-authority handoff;
3. A-11 boundary;
4. immutable execution-envelope authority;
5. durable dispatch intent before external action;
6. backend-native ID separation;
7. worker/backend capability matching;
8. lost acknowledgement and ambiguous submission recovery;
9. queue/claim/lease/heartbeat behavior;
10. sport-child reconciliation;
11. synchronous/asynchronous invocation;
12. cancellation/timeout ambiguity;
13. semantic result/output validation;
14. stale queued work;
15. environment/mode/side-effect safety;
16. backend replacement neutrality;
17. all 60 stored A-10 stress cases.

---

# Summary result

**PASS after seven V1.1 certification clarifications.**

No blocking contradiction remains after applying `A10_WORKER_EXECUTION_BACKEND_ADDENDUM_V1_1.md`.

The review identified seven areas where V1 was directionally correct but needed tighter implementation authority:

1. final current-authority revalidation must occur immediately before irreversible backend submission, not only before A-11 attempt creation;
2. ambiguous backend acknowledgement recovery needs one stable `BackendSubmissionKey` per RunAttempt submission authority;
3. backend callbacks/events are observations and cannot define canonical lifecycle ordering by receipt time;
4. worker/backend capability compatibility must be revalidated at actual assignment/start when descriptors can change while queued;
5. a final result/manifest must correlate to the exact attempt/envelope/child authority;
6. backend execution handle and sport child ref remain distinct logical roles even when a direct service integration happens to reuse one external ID;
7. cancellation races never suppress terminal result reconciliation.

With these clarifications, A-10 is suitable for architecture certification.

---

# Ownership review

## TDLA vs sport repositories — PASS

A-10 coordinates generic physical execution only.

TDLA does not absorb:

- model/prediction logic;
- sport result meaning;
- sport child identity;
- sport-specific readiness;
- sport settlement semantics.

All sport work remains behind A-5.

## TDLA vs DDC — PASS

A-10 does not create a competing acquisition/provider execution system. DDC child/acquisition/provider refs remain nested provenance where used by sport runtimes.

---

# Identity review

## Canonical TDLA identity vs physical backend IDs — PASS

The architecture preserves:

```text
WorkflowRun
-> StageRun
-> RunAttempt
-> DispatchRecord
-> backend ExecutionHandle
-> sport child ref
```

Backend/job/pod/message/process IDs remain cross-references only.

## Backend-vs-child role distinction — PASS after V1.1

A direct sport-service integration may expose one external service job ID for both physical roles, but TDLA retains typed logical roles separately. This preserves architecture when a queue/container/backend layer is introduced later.

---

# A-9/A-11 boundary review

## A-9 grant revalidation — PASS after V1.1

A-9 grant evidence is checked before A-11 attempt authority and again immediately before physical submission.

A RunAttempt existing does not override newly stale plan/scope/schedule/readiness/dependency authority.

## A-11 deferral — PASS

A-10 does not prematurely freeze:

- logical idempotency key formulas;
- retry attempt creation;
- retry schedules;
- timeout state machine.

It does require a stable logical idempotency context and a stable backend submission identity for the A-11-authorized RunAttempt.

---

# Dispatch durability/reconciliation review

## Durable intent before external action — PASS

The architecture requires frozen envelope + durable TDLA dispatch intent before irreversible external submission.

Exact transaction/outbox DDL remains A-13.

## Backend acknowledgement loss — PASS after V1.1

`BackendSubmissionKey` provides stable submission authority for reconciliation/idempotent retransmission of the same RunAttempt submission.

Ambiguity is not permission to create a new submission or attempt.

## A-5 child acknowledgement loss — PASS

A-10 preserves A-11 logical idempotency context in the envelope so a sport child accepted before worker failure can be recovered using A-5 child reconciliation.

The backend and child ambiguity layers remain independent.

---

# Queue/worker/liveness review

## Duplicate message / claim / lease behavior — PASS

Duplicate physical delivery/claim can occur without creating new canonical RunAttempt identity.

Lease expiry and heartbeat loss do not prove previous work stopped.

## Worker capability drift — PASS after V1.1

Queued work must revalidate selected worker/backend descriptor compatibility at assignment/start.

A changed/incompatible worker descriptor invalidates the physical assignment but does not rewrite A-9 sport eligibility evidence.

## Stale queued work — PASS

A queue message is not execution authority. Current A-9 witnesses are checked near start/submission.

---

# Cancellation/timeout review

## Timeout ambiguity — PASS

Timeout does not prove backend or sport child termination.

## Cancellation granularity — PASS after V1.1

Cancellation requested/accepted/observed/child-requested/child-terminal are separate evidence states.

If completion races cancellation, actual terminal sport result is still reconciled and retained.

---

# Result/output review

## Backend success vs semantic success — PASS

Exit code 0, Prefect Completed, Kubernetes Job Complete, or queue acknowledgement are insufficient.

A-5/A-6 semantic result/output contracts remain authoritative.

## Partial outputs — PASS

Partial/staged files cannot become success without a final immutable result/manifest authority.

## Exact result correlation — PASS after V1.1

Terminal result/manifests bind the exact StageRun/RunAttempt, envelope digest, plan/stage/scope authority, child/synchronous invocation correlation, logical idempotency identity, and expected output contracts.

Same-named or same-hash artifact from another attempt/replay/scope cannot silently satisfy current work.

---

# Backend callback/reconciliation review

## Duplicate/out-of-order callbacks — PASS after V1.1

Callbacks are retained evidence, not canonical state transitions applied blindly in receipt order.

Conflicting evidence triggers authoritative backend/child/result reconciliation.

## Backend health/outage — PASS

Backend capacity/outage remains operational execution-plane state and is not converted into sport readiness/failure.

---

# Security/environment review

## Secret handling — PASS at A-10 scope

Execution envelopes store only logical secret/service identity refs. Raw secret retrieval/authorization remains A-20.

## Environment/mode isolation — PASS

Staging workers cannot silently consume production side-effect authority; shadow/supervised/production remain explicit.

---

# Technology-neutrality review

## Backend replacement — PASS

Migrating among local subprocess, Docker, Prefect, queue workers, Kubernetes, or direct sport services does not redefine TDLA StageRun/RunAttempt or A-5 child identity.

ADR-0007 captures this as a durable decision.

---

# 60-case stress-test matrix

| # | Scenario | Result | Review notes |
|---|---|---|---|
| 1 | Valid current grant -> compatible local/test worker | PASS | Preflight + A-11 authority + final revalidation + envelope/dispatch path. |
| 2 | Grant expires in queue | PASS | Final revalidation rejects; reevaluation required. |
| 3 | Schedule revision changes after enqueue | PASS | Old grant/witness stale; no start. |
| 4 | Readiness expires after enqueue | PASS | Final current-authority check rejects. |
| 5 | Upstream output retracted after enqueue | PASS | A-9 witness invalidated; no start. |
| 6 | Plan revision supersedes queued work | PASS | Plan digest mismatch; fail closed. |
| 7 | Worker capability mismatch | PASS | No physical start; operational disposition. |
| 8 | No authorized production worker | PASS | `NO_COMPATIBLE_WORKER`/wait; not sport failure. |
| 9 | GPU-required stage, CPU-only workers | PASS | Capability mismatch. |
| 10 | Production work routed toward staging pool | PASS | Environment/mode authorization rejects. |
| 11 | Immutable image digest verified | PASS | Exact target allowed. |
| 12 | Mutable `latest` target in production | PASS | Fail closed before sport work. |
| 13 | Input manifest digest mismatch | PASS | Fail before invocation. |
| 14 | Required input missing | PASS | Fail before invocation; not guessed by filename. |
| 15 | Runtime secret retrieval by reference | PASS | Raw value excluded from envelope/persistence. |
| 16 | Secret appears in error/log | PASS | Must sanitize; later A-17/A-20 incident boundary. |
| 17 | Dispatch intent persisted; worker dies before adapter | PASS | Reconcile no child before A-11 retry decision. |
| 18 | Backend accepts; acknowledgement lost | PASS | Stable BackendSubmissionKey + backend reconciliation. |
| 19 | Async child accepted; worker dies before child ref persisted | PASS | A-5 logical-idempotency lookup recovers child. |
| 20 | Child ref recorded then worker dies | PASS | TDLA can reconcile child independently. |
| 21 | Child succeeds while worker dead | PASS | Existing result fetched/validated; no blind rerun. |
| 22 | Child fails while worker dead | PASS | Terminal semantic failure recovered. |
| 23 | Sync adapter semantic success + valid outputs | PASS | Can complete after output validation. |
| 24 | Exit 0 but required result/output missing | PASS | Semantic failure/incomplete; no success. |
| 25 | Backend Completed, sport failed/degraded | PASS | Sport semantic result retained; backend state separate. |
| 26 | Backend fails before sport invocation | PASS | Operational/backend failure; no child assumed. |
| 27 | Heartbeat lost, backend job still running | PASS | Reconcile; no duplicate permission. |
| 28 | Heartbeat lost, sport child running independently | PASS | A-5 child reconciliation. |
| 29 | Lease expires, prior worker may still run | PASS | Lease loss != stopped. |
| 30 | Two workers claim same dispatch | PASS | Same RunAttempt/dispatch authority; A-11 final duplicate protection. |
| 31 | Duplicate queue message | PASS | Delivery not identity; same stable dispatch/submission authority. |
| 32 | Backend reconciliation finds existing job | PASS | Reuse existing handle; no duplicate. |
| 33 | Backend cannot reconcile ambiguous side-effecting submission | PASS | Not production-certifiable without A-11 compensation. |
| 34 | A-5 child reconciliation finds existing child | PASS | Child layer independently recovered. |
| 35 | Cancel requested before start | PASS | Preserve cancel evidence; backend/start handling explicit. |
| 36 | Cancel after backend start before child | PASS | Backend/worker state reconciled; no assumed child. |
| 37 | Cancel after child start unsupported/declined | PASS | Child may continue; status explicit. |
| 38 | Backend accepts cancel, child continues | PASS | Backend cancel != child terminal. |
| 39 | Timeout, backend/child unknown | PASS | Reconciliation state; no blind retry. |
| 40 | Partial files then worker crash | PASS | No final manifest/result => no semantic success. |
| 41 | Final manifest/result then worker crash | PASS | Correlated result recovered/validated; no rerun. |
| 42 | Result manifest schema mismatch | PASS | Semantic validation failure. |
| 43 | Result digest mismatch | PASS | Fail closed; immutable evidence retained. |
| 44 | Shadow compute isolated from publication | PASS | Worker capability/side-effect restrictions enforce path. |
| 45 | Supervised compute waits at approval | PASS | Worker cannot self-approve. |
| 46 | Production customer-visible authorized service class | PASS | Technical worker capability plus all higher gates required. |
| 47 | Same StageRun uses different backend on later retry attempt | PASS | Backend changes; StageRun stays canonical; A-11 owns attempt lineage. |
| 48 | Prefect -> Kubernetes migration | PASS | TDLA identities/contracts preserved. |
| 49 | Worker/pod restart gives new physical ID | PASS | Physical metadata cross-reference only. |
| 50 | Backend outage/capacity exhaustion | PASS | Operational wait, not sport failure. |
| 51 | FIFO conflicts with deadline priority | PASS | Queue order not authority; current deadline/plan revalidated. |
| 52 | Queued message past deadline | PASS | Final revalidation rejects/reevaluates. |
| 53 | Superseded old message arrives after replacement ran | PASS | Old plan/grant/attempt authority rejected; no duplicate. |
| 54 | Duplicate backend completion callback | PASS | Callback retained/deduped/reconciled; no second semantic completion. |
| 55 | Out-of-order running/completed callbacks | PASS | V1.1: receipt order cannot roll canonical state backward. |
| 56 | Backend success, child still running/unknown | PASS | Backend completion not semantic result; reconcile child. |
| 57 | Child terminal result exists, backend record disappeared | PASS | Child/result authority can complete reconciliation independently. |
| 58 | Worker descriptor changes incompatibly while queued | PASS | V1.1: capability rechecked at assignment/start. |
| 59 | Semantic envelope serialized differently | PASS | Canonical schema-controlled digest remains deterministic. |
| 60 | Physical worker metadata changes | PASS | Audit-only metadata excluded when schema declares non-semantic. |

---

# Additional failure-path review

## Plan/schedule changes after A-11 attempt creation but before submission

Result: **PASS after V1.1**.

Final current-authority revalidation occurs after attempt/envelope preparation and immediately before durable dispatch/submission boundary. Existing RunAttempt does not override stale authority.

## Same backend submission resent after acknowledgement loss

Result: **PASS after V1.1**.

Same RunAttempt uses same stable backend submission identity for safe idempotent retransmission/reconciliation. A new transport request ID is not a new logical submission.

## Direct sport-service backend reuses one external job ID

Result: **PASS after V1.1**.

TDLA retains separate typed backend-handle and sport-child roles even if the external opaque value matches.

## Cancellation races with terminal success

Result: **PASS after V1.1**.

Cancellation evidence does not erase or suppress already-produced terminal sport result/output evidence.

## Final-looking manifest from another attempt

Result: **PASS after V1.1**.

Correlation to exact attempt/envelope/child authority is mandatory.

---

# Daily-MLB compatibility note

A-10 does not require current Daily-MLB manual internals to be rewritten.

Future M13/M14 integration may use an authenticated service, local/container wrapper, or another certified backend, but it must preserve:

- TDLA A-9 grant revalidation;
- A-11 logical idempotency identity;
- immutable A-10 execution envelope;
- durable backend dispatch intent;
- backend acknowledgement reconciliation;
- A-5 child lookup by logical idempotency for lost child acknowledgement;
- exact semantic result/output manifest validation.

Current Daily-MLB remains manual-first and receives no production automation authority from A-10 certification.

---

# Daily-NFL / NCAAF compatibility note

Football stages can use different worker classes or transports without changing sport readiness/snapshot semantics.

Late legitimate pre-kickoff changes can invalidate queued A-9 grants; A-10 final revalidation prevents stale football work from starting even if the queue message is old.

No football-specific worker decision logic is introduced.

---

# Deferred architecture review

A-10 does not improperly freeze later concerns.

Still deferred:

- A-11 exact logical idempotency/retry/timeout algorithms;
- A-12 generalized failure/degradation/recovery action policy;
- A-13 dispatch/outbox/lease/unique-key DDL and transaction mechanics;
- A-14 artifact storage/retention/replay mechanics;
- A-15 capacity/concurrency/priority/provider budgets;
- A-16 detailed telemetry;
- A-17 incident/alert policy;
- A-18 publication transport;
- A-19 approval mechanics;
- A-20 concrete service identities/secret retrieval;
- A-21 worker-pool/HA deployment topology;
- A-22 build/release supply chain.

This deferral is intentional and does not block A-10 certification.

---

# Certification recommendation

**Recommend A-10 as `ARCHITECTURE-CERTIFIED` governed by:**

- `docs/architecture/A10_WORKER_EXECUTION_BACKEND_V1.md`;
- `docs/architecture/A10_WORKER_EXECUTION_BACKEND_ADDENDUM_V1_1.md`;
- `docs/adr/ADR-0007_IMMUTABLE_EXECUTION_ENVELOPE_AND_RECONCILABLE_BACKEND_DISPATCH.md`.

Certification grants architecture authority only.

It does not certify:

- Prefect deployments/work pools;
- Docker/Kubernetes/queue implementations;
- worker Pydantic models;
- PostgreSQL dispatch/outbox/lease tables;
- exact retry/idempotency algorithms;
- production sport execution;
- publication side effects.

The next architecture checkpoint should be **A-11 Retry / Timeout / Idempotency Architecture**.