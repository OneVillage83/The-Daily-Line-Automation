# A-7 Architecture Conformance Review — Trigger Architecture

Review date: 2026-09-04  
Repository: `OneVillage83/The-Daily-Line-Automation`

Reviewed architecture:

- `docs/architecture/A07_TRIGGER_ARCHITECTURE_V1.md`
- `docs/architecture/A07_TRIGGER_ARCHITECTURE_ADDENDUM_V1_1.md`
- `docs/adr/ADR-0004_DURABLE_TRIGGER_EVIDENCE_AND_REEVALUATION_ONLY_AUTHORITY.md`

Foundation dependencies reviewed for consistency:

- A-0 through A-4 Foundation V1 + V1.1;
- A-5 Sport Automation Adapter V1 + V1.1;
- A-6 Pipeline Plan / Stage Contracts V1 + V1.1;
- ADR-0001 canonical TDLA identity / replaceable orchestrator;
- ADR-0002 transport-neutral sport adapter protocol;
- ADR-0003 immutable plan fragments / resolved-plan authority;
- current TDLA documentation-memory/immutability rules.

## Review purpose

A-7 must define a durable, multi-source trigger architecture that can ingest timers, sport-change signals, dependency changes, callbacks, operator requests, and recovery causes while guaranteeing that a trigger remains **evidence for reevaluation rather than execution authority**.

The review tests:

1. separation of delivery vs semantic event vs execution identity;
2. append-only correction/retraction lineage;
3. durable ingestion/restart safety;
4. duplicate/out-of-order delivery handling;
5. trigger-binding immutability and plan authority;
6. sport-semantics isolation;
7. timer/scheduler boundary with A-8;
8. readiness/dependency boundary with A-9;
9. duplicate-work defense boundary with A-11;
10. replay/test isolation;
11. trust/payload hygiene;
12. burst/coalescing provenance;
13. compatibility with A-5/A-6 and future MLB/NFL/NCAAF integration.

---

# Summary result

**PASS after six V1.1 certification clarifications.**

No blocking contradiction remains after applying `A07_TRIGGER_ARCHITECTURE_ADDENDUM_V1_1.md`.

The review found six places where the V1 base was directionally correct but should be made implementation-proof before certification:

1. source occurrence-family identity needed to be separated explicitly from immutable event-revision identity;
2. same source occurrence/revision with a conflicting semantic payload digest must fail closed rather than be treated as a duplicate;
3. `EligibilityReevaluationRequest` needed its own logical identity separate from physical evaluation attempts;
4. durable causal intent needed to be explicit between accepted trigger evidence and downstream execution processing;
5. untrusted deliveries must not create authoritative semantic `TriggerEvent` objects;
6. burst coalescing must not silently cross incompatible plan/stage/scope/binding/environment revisions.

With those clarifications, A-7 is suitable for architecture certification.

---

# Ownership-boundary review

## Trigger layer vs sport systems — PASS

A-7 does not introduce sport interpretation into TDLA.

A sport system may report an opaque generic change hint or plan/scope revision. TDLA:

```text
records event
-> matches declared binding
-> requests eligibility reevaluation
-> invokes A-5 readiness when required
```

It does not calculate what a lineup, probable pitcher, inactive list, injury designation, or sport-specific weather change means.

## Trigger layer vs A-8 scheduler — PASS

A-7 stores/processes due occurrences but does not calculate event-relative due times.

A-8 remains authority for:

- target/due-time resolution;
- schedule revision recalculation;
- missed-window behavior;
- timer occurrence generation semantics.

A stale old timer is retained as evidence and cannot revive superseded work.

## Trigger layer vs A-9 dependency/readiness engine — PASS

A trigger requests reevaluation. It does not decide readiness/dependency satisfaction.

A `READINESS_HINT` can arrive while A-5 still returns `WAITING`; the stage remains non-dispatchable.

## Trigger layer vs A-11 idempotency — PASS after V1.1

A-7 performs event/delivery deduplication and assigns logical reevaluation identity.

A-11 still owns the final stage logical-idempotency/retry guarantee.

Multiple distinct legitimate trigger causes can race toward one stage without relying on trigger dedup as the sole duplicate-work defense.

---

# Identity review

## Delivery identity vs semantic event identity — PASS

Physical webhook/queue/timer delivery is distinct from semantic source occurrence.

Repeated transport delivery can create multiple `TriggerDelivery` records resolving to one semantic event revision.

## Occurrence family vs revision — PASS after V1.1

A correction/retraction needs lineage around one source occurrence family without mutating the original revision.

Certified model:

```text
TriggerOccurrenceKey
    -> TriggerEventRevisionKey v1
    -> TriggerEventRevisionKey v2 correction
    -> TriggerEventRevisionKey v3 retraction
```

Each revision is immutable.

## Conflicting duplicate identity — PASS after V1.1

The same claimed occurrence+revision with a different semantic payload digest is an event-identity conflict, not a harmless duplicate.

Authority fails closed pending source-specific resolution.

## Reevaluation identity — PASS after V1.1

Logical reevaluation work is separate from physical trigger-evaluation attempts.

A crash/retry can create a new processing attempt while preserving one logical reevaluation request for the same target/cause/binding authority.

---

# Durable-ingestion review

## Durable evidence before action — PASS

A-7 requires accepted trigger evidence to be persisted before downstream irreversible action.

V1.1 clarifies that reevaluation intent/cause must also be durable enough to resume after restart.

The exact database transaction/outbox implementation remains A-13.

## Crash after persistence before evaluation — PASS

Persisted accepted evidence can be resumed after restart without source redelivery.

## Crash after evaluation before dispatch — PASS

Durable reevaluation identity/cause persists. Final duplicate stage dispatch remains protected by A-11.

---

# Ordering / revision review

## No global ordering assumption — PASS

A-7 does not rely blindly on TDLA receipt order or source wall-clock timestamps.

## Source sequence/revision evidence — PASS

Monotonic source sequence/version is used only when the source contract guarantees those semantics.

## Older revision after newer revision — PASS

Older evidence is retained but cannot silently roll known authority backward.

## Source clock skew — PASS

An `occurred_at` later than `received_at` does not by itself corrupt ordering; the timestamps remain distinct evidence clocks.

---

# Correction/retraction review

## Correction before work executes — PASS

Correction becomes a new immutable revision and can cause reevaluation/supersession.

## Correction after work executes — PASS

The original completed StageRun remains historical truth of what happened. Later correction requires explicit recovery/reprocess/publication-correction policy rather than historical rewrite.

## Retraction — PASS

Same append-only lineage rule applies.

---

# TriggerBinding review

## Immutable plan-bound authority — PASS

Production binding is versioned/digested and tied to exact resolved-plan/stage authority.

A mutable broker subscription cannot redefine historical plan behavior.

## Generic matching only — PASS

Bindings may compare source namespace/kind, scope refs, plan/stage refs, environment/mode, and declaratively supplied opaque values.

There is no sport-specific branch in generic code.

## Multiple matches — PASS

One event may deterministically create several reevaluation targets, each independently auditable.

## No match — PASS

Valid `NO_MATCH` is not a system failure.

## Expired/stale binding — PASS

An otherwise valid event cannot resurrect work through an expired/superseded binding.

---

# Burst/coalescing review

## Raw evidence retention — PASS

100 source events may produce one coalesced reevaluation cause set while every delivery/event remains retained.

## Cross-source correlation — PASS

Two source namespaces remain distinct semantic events unless an explicit correlation/coalescing policy links them.

## Authority revision boundary — PASS after V1.1

A cause set cannot silently mix incompatible resolved-plan/stage/scope/binding/environment authority revisions.

---

# Replay / environment review

## Historical trigger replay to staging — PASS

Original occurrence time and actual replay time are both retained.

Replay is labeled and cannot inherit production side-effect authority merely because the original event was once production-relevant.

## Replay accidentally reaches production ingress — PASS

Mode/environment restrictions fail closed unless explicitly authorized by a future controlled test policy.

## Trigger replay vs StageRun replay — PASS

The concepts remain separate: trigger replay re-exercises event/eligibility behavior; StageRun replay/reprocess follows A-3/A-14 lineage.

---

# Security / trust review

## Invalid authentication/signature — PASS after V1.1

A sanitized rejected `TriggerDelivery` may be retained under policy, but no authoritative semantic `TriggerEvent` is created and no reevaluation occurs.

## Secret-bearing payload — PASS

Raw secret material cannot be persisted as ordinary trigger data. Sanitized diagnostics only.

## Source descriptor incompatibility — PASS

Unsupported source/trust/descriptor version fails closed for authoritative production binding.

Concrete credential/signature implementation remains A-20.

---

# No-direct-side-effect review

**PASS.**

Certified trigger path is:

```text
TriggerDelivery
-> TriggerEvent
-> TriggerBinding
-> TriggerEvaluation
-> EligibilityReevaluationRequest
-> A-8/A-9/A-6/A-11 gates
-> A-5 execution
-> A-18/A-19 side-effect/approval gates when applicable
```

Prohibited path remains:

```text
webhook/timer -> publish / destructive operation
```

This rule also applies to authenticated operator triggers by default.

---

# Stress-test matrix

| # | Scenario | Result | Review notes |
|---|---|---|---|
| 1 | Same timer occurrence fires twice | PASS | Two deliveries can resolve to one semantic timer occurrence; A-11 still protects stage work. |
| 2 | Same webhook delivered repeatedly with stable event ID | PASS | Duplicate deliveries retained; one occurrence/revision event. |
| 3 | Source has no stable event ID and no safe deterministic identity | PASS | Cannot be high-authority event-driven production source; advisory/fallback or fail closed. |
| 4 | Older schedule/scope revision arrives after newer | PASS | Retained as stale evidence; cannot roll authority backward. |
| 5 | Corrected event revision | PASS | New immutable revision linked to same occurrence family. |
| 6 | Retraction | PASS | Append-only lineage; no historical deletion. |
| 7 | MLB pregame-change hint | PASS | Generic reevaluation; A-5 owns readiness meaning. |
| 8 | NFL/NCAAF pregame-change hint | PASS | Same generic behavior; no football branches. |
| 9 | Readiness hint but A-5 says WAITING | PASS | Trigger cannot override readiness. |
| 10 | Trigger after deadline | PASS | Evidence retained; A-8 timing/missed-window rule blocks unauthorized late run. |
| 11 | Dependency-completion event delivered twice | PASS | Trigger dedup + stage idempotency are separate defenses. |
| 12 | Trigger for SUCCEEDED stage | PASS | `NO_ACTION_STAGE_TERMINAL`. |
| 13 | Trigger for superseded plan/stage | PASS | Stale binding/revision cannot resurrect work. |
| 14 | Trigger for NOT_APPLICABLE stage | PASS | No dispatch; audit result retained. |
| 15 | No-games/empty-scope plan change | PASS | No fake event work created. |
| 16 | 100-event burst | PASS | Cause-set/coalescing allowed; all raw evidence retained. |
| 17 | Crash after trigger persistence before evaluation | PASS | Restart resumes from durable evidence. |
| 18 | Crash after evaluation before/around dispatch | PASS | Durable logical reevaluation + A-11 protects stage dispatch. |
| 19 | Two sources report same real-world change | PASS | Distinct source evidence unless explicit correlation policy. |
| 20 | Source clock skew | PASS | Ordering does not rely blindly on wall clock. |
| 21 | Payload schema/digest mismatch | PASS | Fails closed; no authoritative reevaluation. |
| 22 | Invalid/untrusted external trigger | PASS | Sanitized rejected delivery only; no TriggerEvent. |
| 23 | Secret-like data in payload | PASS | Sanitize/reject; no raw secret persistence. |
| 24 | Authenticated operator asks reevaluation | PASS | Ordinary gates remain required. |
| 25 | Future operator override | PASS | Must be separate A-19 action. |
| 26 | Publication callback redelivered | PASS | Typed source event/delivery dedup; publication meaning stays A-18. |
| 27 | New timer after event-time move; old timer later fires | PASS | Old timer ties superseded schedule revision and cannot revive work. |
| 28 | Trigger source down for hours | PASS | Silence is not no-change truth; fallback may be timer/readiness/poll policy. |
| 29 | Historical trigger replay into staging | PASS | Original + replay clocks retained; no production side effects. |
| 30 | Valid event matches no binding | PASS | `NO_MATCH`. |
| 31 | One event matches multiple bindings | PASS | Deterministic independently auditable reevaluation requests. |
| 32 | Same semantic payload with different transport headers/IDs | PASS | Transport-only differences do not change semantic event identity. |
| 33 | Correction after previous StageRun completed | PASS | Historical work remains; later recovery/reprocess policy required. |
| 34 | New event after coalescing window closes | PASS | New cause/request; not absorbed into old closed cause set. |
| 35 | Binding expired before event arrival | PASS | No action through stale binding. |
| 36 | Event references obsolete scope revision | PASS | Current authority check prevents resurrection. |
| 37 | Replay delivered to production ingress | PASS | Mode/environment restriction fails closed. |
| 38 | Recovery finds persisted unevaluated trigger | PASS | Internal recovery continues without source redelivery. |
| 39 | Source sequence regresses/repeats unexpectedly | PASS | Sequence conflict/staleness evidence retained; no blind ordering rollback. |
| 40 | Trigger source descriptor/trust version incompatible | PASS | Binding/source validation fails before authoritative reevaluation. |

---

# Additional failure-path review

## Same occurrence/revision, different semantic payload

Result: **PASS after V1.1**.

This is an event-identity conflict. The original immutable event is not overwritten and the conflicting delivery is quarantined/fails closed.

## Same occurrence, higher valid revision

Result: **PASS after V1.1**.

This is a legitimate new revision, not an identity conflict.

## Evaluation worker retries

Result: **PASS after V1.1**.

The processing attempt may change while logical reevaluation identity remains stable.

## Coalescing while scope revision changes

Result: **PASS after V1.1**.

Events under incompatible authority revisions cannot silently share one cause set.

## Source says “ready” but plan requires authoritative readiness check

Result: **PASS**.

Source hint cannot bypass A-5 readiness.

---

# Daily-MLB compatibility note

A-7 does not require Daily-MLB to expose baseball-specific event names to generic TDLA.

The future MLB adapter can emit generic change/scope-revision/readiness-hint events carrying opaque sport references.

Example shape:

```text
MLB service detects relevant state change
    -> SPORT_CHANGE_HINT(scope_ref, revision, opaque change metadata)
        -> TDLA durable trigger evidence
            -> A-5 readiness check
                -> A-8/A-9 eligibility decision
```

Important: current Daily-MLB manual architecture remains the target to certify first. A-7 certification does not authorize wiring the unfinished starter service into production event-driven automation.

---

# Daily-NFL / NCAAF compatibility note

The same design supports late legitimate pre-kickoff changes without embedding football meaning in TDLA.

A sport system can signal that relevant pregame state changed; the later snapshot/materialization remains governed by A-6 schedule-slot identity, A-8 timing, and A-5/A-9 readiness/dependencies.

---

# Deferred-architecture review

A-7 intentionally leaves these unresolved:

- A-8 due-time/timer generation/recalculation algorithms;
- A-9 dependency/readiness state machine;
- A-10 transport/broker/worker technology;
- A-11 exact logical keys/retries/timeouts;
- A-12 recovery/compensation policy;
- A-13 PostgreSQL DDL, transaction, outbox, locking;
- A-15 ingress/concurrency budgets;
- A-16 metrics/tracing;
- A-17 incidents/alerts;
- A-18 publication callback contract specifics;
- A-19 operator override mechanics;
- A-20 signatures/service identities/secrets.

This deferral is appropriate and does not block certification.

---

# Certification recommendation

**Recommend A-7 as `ARCHITECTURE-CERTIFIED` governed by:**

- `docs/architecture/A07_TRIGGER_ARCHITECTURE_V1.md`;
- `docs/architecture/A07_TRIGGER_ARCHITECTURE_ADDENDUM_V1_1.md`;
- `docs/adr/ADR-0004_DURABLE_TRIGGER_EVIDENCE_AND_REEVALUATION_ONLY_AUTHORITY.md`.

Certification grants architecture authority only. It does not certify trigger Pydantic models, database tables, message brokers, webhook endpoints, timer workers, Prefect events, security/signature code, or any live sport trigger integration.

The next architecture checkpoint should be **A-8 — Event-Relative Scheduling Engine**.