# A-9 Architecture Conformance Review — Dependency / Readiness Engine

Review date: 2026-09-05  
Repository: `OneVillage83/The-Daily-Line-Automation`

Reviewed architecture:

- `docs/architecture/A09_DEPENDENCY_READINESS_ENGINE_V1.md`
- `docs/architecture/A09_DEPENDENCY_READINESS_ENGINE_ADDENDUM_V1_1.md`
- `docs/adr/ADR-0006_VERSION_BOUND_DISPATCH_ELIGIBILITY_AND_FINAL_REVALIDATION.md`

Foundation dependencies reviewed for consistency:

- A-0 through A-4 Foundation V1 + addendum;
- A-5 Sport Automation Adapter V1 + V1.1;
- A-6 Pipeline Plan / Stage Contracts V1 + V1.1;
- A-7 Trigger Architecture V1 + V1.1;
- A-8 Event-Relative Scheduling Engine V1 + V1.1;
- ADR-0001 through ADR-0005;
- repository operating constitution in `AGENTS.md`.

## Review purpose

A-9 must produce a deterministic, auditable answer to whether one exact stage materialization is currently eligible to proceed toward dispatch without:

- absorbing sport readiness meaning;
- trusting stale `READY` state;
- accepting wrong/superseded upstream outputs;
- ignoring schedule/plan/scope revisions;
- turning technical errors into sport-domain states;
- creating a direct readiness-to-execution path;
- replacing A-11 final StageRun idempotency.

The review therefore focuses on current-authority checks, A-6 dependency/output semantics, A-5 readiness freshness, A-8 time authority, fan-in membership, TOCTOU handoff, crash/concurrency behavior, and mode/policy safety.

---

# Summary result

**PASS after six V1.1 certification clarifications.**

No blocking contradiction remains after applying `A09_DEPENDENCY_READINESS_ENGINE_ADDENDUM_V1_1.md` and ADR-0006.

The six clarifications were:

1. deterministic complete reason reporting must not force unnecessary external readiness calls after an earlier authoritative gate already determines non-eligibility;
2. `DispatchEligibilityGrant` is non-transferable evidence plus final current-authority revalidation, never a bearer execution token;
3. readiness-cache validity is the intersection of all freshness bounds and is immediately invalidated by incompatible authority revisions;
4. upstream output supersession/retraction invalidates dependent eligibility/grants even if the old artifact digest remains available;
5. composite readiness requires explicit required/optional semantics and keeps technical predicate failures distinct from sport `BLOCKED`;
6. eligibility semantic digest is separate from unique evaluation record identity and A-7 causal trigger lineage.

With these clarifications, A-9 is suitable for architecture certification.

---

# Ownership-boundary review

## TDLA vs sport readiness meaning — PASS

A-9 consumes only A-5 generic readiness dispositions:

- `READY`;
- `WAITING`;
- `BLOCKED`;
- `NOT_APPLICABLE`.

Sport reason codes remain opaque evidence.

No MLB/NFL/NCAAF branch is required or permitted to calculate generic eligibility.

## TDLA vs Daily-Data-Core — PASS

A-9 may validate generic provenance/freshness/output metadata but does not acquire odds/weather/provider facts or interpret their sport meaning.

## TDLA vs worker/idempotency layers — PASS

A-9 produces eligibility evidence only. It does not create child jobs, choose workers, or claim final execution uniqueness.

A-10 owns execution backend/dispatch mechanics and A-11 remains the final logical StageRun idempotency/retry authority.

---

# Current-authority review

## Current authority first — PASS

The engine validates current resolved plan, materialization, scope/scope revision, schedule authority, environment/mode, and relevant policy/config references before readiness can create dispatch eligibility.

Old authority cannot regain current status merely because its old dependencies/readiness remain valid historically.

## Final authority recheck — PASS after ADR-0006

A-9 rechecks current authority after evidence collection and produces a version-bound `DispatchEligibilityGrant` only when all gates pass.

A-10/A-11 must still revalidate the grant's witnesses before dispatch.

This closes the key TOCTOU gap without collapsing A-9 into the worker layer.

---

# Dependency-contract review

## Required upstream/output behavior — PASS

A required success/output edge remains unsatisfied when:

- upstream is non-terminal;
- upstream failed incompatibly;
- required output is missing;
- manifest/schema/digest/provenance mismatches;
- evidence belongs to the wrong plan/scope/slot/lineage.

## OPTIONAL semantics — PASS

`OPTIONAL` is not automatically ignored. A downstream stage requiring an optional stage's output remains blocked when that output is absent.

## NO_OP semantics — PASS

A valid `NO_OP` can satisfy only contracts explicitly allowing it. It cannot fabricate required output.

## Degraded success — PASS

`SUCCEEDED_DEGRADED` satisfies only exact validated outputs allowed by the bound failure/degradation policy.

## Terminal failure evidence — PASS

A downstream stage may intentionally consume terminal-failure evidence only through an explicit A-6 contract; ordinary required-success edges remain unsatisfied.

---

# Upstream evidence / revision review

## Exact authority binding — PASS

Dependency evidence binds exact upstream materialization/StageRun/output manifest/schema/digest/provenance and authority lineage.

A same-named file or logical port from an old plan/snapshot cannot silently satisfy the current stage.

## Supersession/retraction — PASS after V1.1

If an upstream result/output is superseded/retracted before downstream dispatch, old dependency/eligibility evidence remains historical but becomes stale current authority.

An old digest still being physically retrievable is insufficient to keep eligibility current.

---

# Fan-in/barrier review

## Exact membership — PASS

Barrier evaluation uses the exact A-6 `ScopeSetBinding` revision/digest.

TDLA never guesses which games/events belong to the slate.

## Membership revision change — PASS

A changed child set creates new barrier authority. Eight completed children from the old ten-member set are not silently counted toward a new membership revision unless the new resolved contract explicitly references compatible evidence.

## Empty-set behavior — PASS

Empty-set success/no-action behavior must be explicit; there is no accidental vacuous-success default.

---

# Readiness review

## A-5 mapping — PASS

`READY`, `WAITING`, `BLOCKED`, and `NOT_APPLICABLE` map to generic A-9 behavior without sport interpretation.

## Freshness/expiry — PASS after V1.1

Effective readiness validity is bounded by the strictest sport/plan/evidence/schedule/policy freshness requirement.

A result can be invalidated by revision change before its timestamp expires.

## Cache fallback during outage — PASS

A technically unavailable readiness source may use exact-authority cached readiness only while the cached result remains fully valid.

Expired cache + unavailable adapter is a technical evaluation failure, not `READY` and not sport `BLOCKED`.

## Composite readiness — PASS after V1.1

Required readiness predicates must all be valid and `READY` under explicit composition. Optional predicates cannot compensate for failed/missing required predicates.

Technical predicate error remains an evaluation error.

---

# Time/schedule review

## Due event does not override current schedule authority — PASS

A-9 validates the current A-8 resolution/window even if a historical `TIME_DUE` event exists.

## Reschedule after due — PASS

A superseded schedule resolution invalidates old eligibility/grants before dispatch.

## Deadline/freshness race — PASS

A stage can lose eligibility while evaluation is running if the window closes or an input/readiness freshness boundary expires. Final recheck prevents issuing current dispatch eligibility from stale evidence.

---

# PIT/input freshness review

## Generic PIT enforcement — PASS

A-9 enforces declared availability/cutoff/freshness metadata without defining sport-specific PIT semantics.

Evidence known to be available after a declared prediction cutoff cannot satisfy the input contract.

---

# Eligibility identity/reason review

## Complete deterministic reasons — PASS after V1.1

A-9 records a canonical reason set for semantically reachable/evaluated gates.

It does not make unnecessary external calls merely to populate diagnostic reasons after a prior authoritative gate already prevents eligibility.

## Semantic digest vs cause — PASS after V1.1

Different A-7 causes may lead to the same eligibility semantic digest when all execution-semantic authority/evidence/result is identical.

All causes remain auditable.

---

# Dispatch handoff / TOCTOU review

## Explicit grant — PASS

A `READY_FOR_DISPATCH` evaluation produces an immutable version-bound grant.

## Non-bearer semantics — PASS after V1.1 / ADR-0006

The grant does not override current state and cannot be reused across stage/scope/revision/environment/mode.

## Validity bound — PASS

Grant validity is no longer than the earliest applicable readiness/time/policy/current-authority validity boundary. When no safe TTL exists, immediate revalidation is required.

## Final dispatcher check — PASS

A-10/A-11 must compare current authoritative witnesses before using the grant.

This leaves implementation details to later sections while freezing the required safety semantics now.

---

# Concurrency/recovery review

## Simultaneous reevaluations — PASS

Equivalent evaluation attempts can coexist or coalesce, but neither creates StageRun identity directly.

A-11 prevents duplicate logical execution.

## Crash before result persistence — PASS

Durable A-7 reevaluation cause remains available for retry.

## Crash after result persistence — PASS

Recovery may reuse still-current semantically equivalent immutable evidence rather than create contradictory mutable readiness state.

A-13 will define transaction/current-head mechanics.

---

# Execution-mode / side-effect review

## Shadow — PASS

Shadow-safe compute may become eligible; customer-visible/destructive stages disabled by the resolved plan cannot become ready from sport readiness alone.

## Supervised — PASS

Sport/time/dependencies can all be ready while customer-visible work remains policy/approval blocked.

## Production — PASS

A-9 eligibility does not bypass production certification, mode, side-effect, operator, resource, or A-11 idempotency gates.

---

# Stress-test matrix

| # | Scenario | Result | Review notes |
|---|---|---|---|
| 1 | Due + dependencies satisfied + readiness READY | PASS | Produces READY_FOR_DISPATCH and bound grant after final authority recheck. |
| 2 | Readiness READY before time | PASS | WAITING_TIME; readiness may be cached only while still valid later. |
| 3 | Required upstream still running | PASS | WAITING_DEPENDENCY. |
| 4 | Dependencies satisfied, readiness WAITING | PASS | WAITING_READINESS. |
| 5 | Readiness BLOCKED opaque reason | PASS | BLOCKED_READINESS; reason stored, not interpreted. |
| 6 | Readiness NOT_APPLICABLE | PASS | Explicit no-dispatch applicability disposition. |
| 7 | READY expires one second before dispatch | PASS | Grant/current revalidation fails; new readiness required. |
| 8 | Plan max age stricter than adapter validity | PASS | Strictest boundary wins. |
| 9 | New scope/readiness revision after READY | PASS | Old evaluation/grant stale. |
| 10 | Event reschedule after TIME_DUE before dispatch | PASS | Old schedule witness rejected. |
| 11 | Plan revision after READY | PASS | Old plan grant rejected. |
| 12 | Materialization becomes NOT_APPLICABLE | PASS | Old waiting/ready state not carried forward. |
| 13 | Upstream succeeds but manifest missing | PASS | Required output unsatisfied. |
| 14 | Output schema incompatible | PASS | Dependency blocked/fail-closed. |
| 15 | Output digest/provenance mismatch | PASS | Dependency unsatisfied. |
| 16 | Accepted degraded output | PASS | Satisfies only explicit accepted output. |
| 17 | Degraded lacks required output | PASS | Downstream remains blocked. |
| 18 | NO_OP explicitly accepted | PASS | Edge may satisfy according to contract. |
| 19 | NO_OP missing required output | PASS | Output edge not satisfied. |
| 20 | Optional upstream fails, no dependency | PASS | Downstream may continue subject to remaining gates/A-12 policy. |
| 21 | Optional upstream fails, output required | PASS | Downstream blocked. |
| 22 | Required upstream terminal failure | PASS | Required-success dependency blocked. |
| 23 | Terminal failure evidence intentionally consumed | PASS | Explicit terminal-evidence edge can satisfy. |
| 24 | Fan-in 10/10 successful | PASS | Exact membership barrier satisfied. |
| 25 | Membership revision changes after 8/10 | PASS | Old barrier not silently promoted to new set. |
| 26 | Empty set explicit success | PASS | Declared empty behavior honored. |
| 27 | Empty set forbids vacuous success | PASS | Aggregate remains unsatisfied/no-action per contract. |
| 28 | Same-named old-plan artifact | PASS | Wrong plan authority rejected. |
| 29 | Old snapshot output presented to current slot | PASS | Wrong slot/materialization rejected. |
| 30 | Two trigger causes same stage | PASS | Causes may coalesce; lineage retained. |
| 31 | Two evaluator workers both compute READY | PASS | Equivalent semantic digests allowed; no StageRun created by A-9. |
| 32 | Stage already SUCCEEDED | PASS | Terminal no-action; no duplicate run. |
| 33 | Terminal failed + ordinary trigger | PASS | No implicit replay/reprocess. |
| 34 | Explicit historical replay/reprocess | PASS | Requires separate A-14 lineage/authority. |
| 35 | Readiness call timeout | PASS | Technical evaluation error, not sport waiting/blocked. |
| 36 | Malformed readiness schema | PASS | Technical/contract error; fail closed. |
| 37 | Exact valid cached readiness during outage | PASS | May be used only within all certified bounds. |
| 38 | Expired cache during outage | PASS | Cannot become READY; technical failure/wait policy later A-12. |
| 39 | Required readiness capability disappears | PASS | Incompatible current authority; fail closed. |
| 40 | MLB opaque reason waiting->ready | PASS | Generic disposition only; no pitcher/lineup parsing. |
| 41 | NFL/NCAAF opaque late context readiness | PASS | Same generic path. |
| 42 | PIT input available after cutoff | PASS | Input contract unsatisfied. |
| 43 | Input freshness expires mid-evaluation | PASS | Final recheck rejects stale evidence. |
| 44 | READY then schedule changes before dispatch | PASS | Grant witness mismatch rejects dispatch. |
| 45 | READY then upstream output superseded/retracted | PASS | Dependency authority invalidates old grant. |
| 46 | Shadow compute ready, customer-visible stage disabled | PASS | Disabled/not-applicable side-effect path stays non-ready. |
| 47 | Supervised compute ready, approval pending | PASS | Customer-visible stage remains policy blocked. |
| 48 | A-9 ready but A-11 finds existing logical run | PASS | A-11 prevents duplicate execution. |
| 49 | Settlement time/deps ready, sport readiness waiting | PASS | WAITING_READINESS. |
| 50 | No-games day | PASS | No fake event materializations/readiness checks. |
| 51 | Crash before result persistence | PASS | Reevaluation cause retries safely. |
| 52 | Crash after durable result before cause handled | PASS | Still-current semantic evaluation may be reused/reconciled. |
| 53 | Equivalent semantic inputs serialize differently | PASS | Versioned canonicalization must yield same digest. |
| 54 | Superseded eligibility evidence sent to dispatcher | PASS | Current-authority revalidation fails closed. |
| 55 | Technical readiness failure mislabeled BLOCKED | PASS | Explicitly prohibited. |
| 56 | Multiple blocking reasons | PASS | Canonical deterministic reason set for reachable gates. |
| 57 | Dependency arrives after schedule window closes | PASS | Time gate prevents unauthorized late proceed. |
| 58 | Readiness READY before due; later TIME_DUE | PASS | Reuse only if readiness remains exact-authority valid. |
| 59 | Time due first; readiness later READY | PASS | Same materialization becomes eligible without duplicate materialization. |
| 60 | Duplicate reevaluation cause, authority unchanged | PASS | Equivalent evaluation/no duplicate logical sport work. |

---

# Additional failure-path review

## Conflicting current-head observations during one evaluation

Result: **PASS**.

Final authority recheck detects revision change. The evaluation cannot emit a current grant based on a mixed authority snapshot.

Exact database snapshot/transaction implementation remains A-13.

## Grant queued past readiness expiry

Result: **PASS**.

Grant expiry/current revalidation rejects dispatch and routes back to reevaluation rather than silently refreshing the grant in A-10.

## Same artifact digest after explicit retraction

Result: **PASS after V1.1**.

Retraction/current-authority state overrides simple content equality for current dependency eligibility.

## Optional composite readiness predicate technical failure

Result: **PASS after V1.1**.

Behavior follows the explicit versioned composition contract; it cannot implicitly override a required predicate or convert technical error into domain state.

## Prefect task says Completed while A-9 says dependency unsatisfied

Result: **PASS**.

Prefect/runtime state is not canonical eligibility authority. The A-6/A-9 output/dependency contract wins.

---

# Daily-MLB compatibility note

A-9 does not require Daily-MLB to expose baseball-specific readiness semantics to TDLA.

A future certified MLB adapter can provide A-5 readiness results and stable A-6 output/provenance contracts around the final certified manual pipeline.

TDLA then evaluates:

- current MLB-owned scope/revision;
- current schedule/time authority;
- declared upstream outputs;
- generic freshness/PIT evidence;
- generic A-5 readiness disposition.

TDLA still does not parse probable-pitcher/lineup meanings.

Current Daily-MLB remains manual-first and is not production-ready merely because A-9 is certified.

---

# Daily-NFL / NCAAF compatibility note

Multiple legitimate pre-kickoff snapshots remain supported.

A readiness result for one schedule slot/materialization cannot silently authorize another slot. Late injury/inactive/weather semantics remain football-owned while TDLA enforces only the declared readiness/output/freshness contracts.

---

# Deferred-architecture review

A-9 correctly leaves later responsibilities unresolved:

- A-10 worker/backend/queue/dispatch transport;
- A-11 exact logical StageRun identity, retries, timeouts, idempotent create/dispatch;
- A-12 failure propagation/recovery/correction;
- A-13 PostgreSQL DDL/current-head/outbox/transaction design;
- A-14 replay/backfill/reprocess artifact lineage;
- A-15 resource/concurrency/provider budgets;
- A-16 observability;
- A-17 alerts/incidents;
- A-18 publication;
- A-19 operator approvals/overrides;
- A-20 security/service identity.

The explicit DispatchEligibilityGrant does not preempt those designs; it defines the evidence they must consume safely.

---

# Certification recommendation

**Recommend A-9 as `ARCHITECTURE-CERTIFIED` governed by:**

- `docs/architecture/A09_DEPENDENCY_READINESS_ENGINE_V1.md`;
- `docs/architecture/A09_DEPENDENCY_READINESS_ENGINE_ADDENDUM_V1_1.md`;
- `docs/adr/ADR-0006_VERSION_BOUND_DISPATCH_ELIGIBILITY_AND_FINAL_REVALIDATION.md`.

Certification grants architecture authority only. It does not certify eligibility/readiness Pydantic models, cache implementation, database tables, Prefect tasks, worker dispatch, or real sport readiness automation.

The next architecture checkpoint should be **A-10 Worker / Execution Backend Architecture**.