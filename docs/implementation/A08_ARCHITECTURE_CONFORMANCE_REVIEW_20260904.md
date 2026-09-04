# A-8 Architecture Conformance Review — Event-Relative Scheduling Engine

Review date: 2026-09-04  
Repository: `OneVillage83/The-Daily-Line-Automation`

Reviewed architecture:

- `docs/architecture/A08_EVENT_RELATIVE_SCHEDULING_ENGINE_V1.md`
- `docs/architecture/A08_EVENT_RELATIVE_SCHEDULING_ENGINE_ADDENDUM_V1_1.md`
- `docs/adr/ADR-0005_STABLE_SCHEDULE_SLOTS_AND_RESOLVED_TIME_AUTHORITY.md`

Foundation dependencies reviewed for consistency:

- A-0 through A-4 Foundation V1 + addendum;
- A-5 Sport Automation Adapter V1 + addendum;
- A-6 Pipeline Plan / Stage Contracts V1 + addendum;
- A-7 Trigger Architecture V1 + addendum;
- ADR-0001 through ADR-0004;
- current Daily-Data-Core ownership boundary;
- current Daily-MLB manual/service boundary;
- current Daily-NFL/NCAAF event-relative/PIT direction.

## Review purpose

A-8 must establish a generic scheduling authority that can survive event-time movement, uncertain/TBD times, scheduler restart, HA races, DST/local calendar ambiguity, stale callbacks, late/missed windows, and plan/scope revisions without:

- turning timestamps into sport snapshot identity;
- hardcoding sport reschedule meaning;
- allowing a timer to execute work directly;
- using a scheduler-vendor ID as permanent identity;
- rewriting historical schedule evidence;
- creating duplicate logical StageRuns after retries/restarts.

---

# Summary result

**PASS after seven V1.1 certification clarifications.**

No blocking contradiction remains after applying `A08_EVENT_RELATIVE_SCHEDULING_ENGINE_ADDENDUM_V1_1.md`.

The review identified seven areas where the base architecture was directionally correct but needed stronger normative wording before implementation:

1. missed-window policy naming must not imply scheduler execution authority;
2. a new sport schedule revision remains new authority even when the absolute UTC event instant is unchanged;
3. one logical `ScheduleOccurrence` must map to at most one canonical semantic A-7 `TIME_DUE` event;
4. due-boundary selection must be explicit when `target_at` is omitted;
5. an old already-emitted `TIME_DUE` event must be revalidated against current schedule authority before dispatch;
6. DST/local recurrence occurrence identity must retain civil-time disambiguation authority;
7. physical timer reuse/coalescing is an optimization and cannot collapse canonical schedule identities.

With these clarifications, A-8 is suitable for architecture certification.

---

# Ownership-boundary review

## TDLA vs sport repositories — PASS

A-8 uses sport-owned A-5 `SportScopeRef` and schedule/scope revision authority but does not infer whether a provider event is the same game, whether a doubleheader member is game 1/game 2, or whether a domain state change should trigger a model rerun.

Sport repos remain authority for:

- canonical event identity;
- event/schedule revision meaning;
- whether a cancelled/postponed/replaced event exists;
- sport stage meaning;
- readiness semantics.

TDLA owns generic resolution/supersession/missed-window mechanics only.

## TDLA vs A-7 — PASS

A-8 produces a logical due occurrence and A-7 records the durable `TIME_DUE` trigger event/delivery/evaluation.

A-8 does not call sport execution directly.

## TDLA vs A-9 — PASS

Being due is time evidence only. Dependency/readiness/current-authority eligibility remains A-9 work.

---

# Identity review

## Stable slot vs resolved timestamp — PASS

A `ScheduleSlotRef` remains stable when event time moves.

The new time produces a new immutable `ScheduleResolution`; it does not create a new logical slot or mutate prior history.

## Schedule resolution identity — PASS

Resolution binds exact:

- resolved-plan digest;
- stage materialization;
- slot;
- timing declaration;
- sport scope/schedule revision;
- anchor value/revision;
- resolved window;
- policy bindings;
- environment/mode.

## Schedule occurrence vs physical callback — PASS

Physical callbacks/scans/leases are not logical occurrence identity.

Two replicas can observe the same due occurrence while preserving one semantic occurrence.

## Same instant/new schedule revision — PASS after V1.1

New sport schedule authority creates a new resolution even if the UTC start time is numerically unchanged. Runtime timer reuse is permitted without collapsing provenance.

---

# Time/window review

## UTC authority — PASS

Durable schedule instants are timezone-aware UTC.

## Event-relative arithmetic — PASS

Elapsed offsets are applied to resolved UTC instants, preventing DST distortion.

## Earliest/target/deadline/validity/grace distinction — PASS

A-8 does not collapse these boundaries into one timestamp.

## Explicit due-boundary selection — PASS after V1.1

A declaration without enough information to determine its due instant fails closed.

---

# Reschedule/supersession review

## Event moves later — PASS

Pending old resolution is superseded and re-resolved later.

## Event moves earlier — PASS

Newly overdue slots are independently classified by their immutable missed-window policy rather than all firing immediately.

## Event becomes TBD — PASS

Old pending occurrences are superseded; current resolution becomes explicitly unresolved.

## Event is cancelled — PASS

Pending schedule work is retained as cancelled/not-applicable evidence, not deleted.

## Scope replacement — PASS

TDLA does not infer continuity from similar team/date/time metadata.

---

# Missed-window review

## No automatic late execution — PASS after V1.1

Policy family is reevaluation-oriented, not execution-oriented.

Normative conceptual outcomes:

- `SKIP_MISSED`;
- `REQUEST_REEVALUATION_IF_WITHIN_GRACE`;
- `REQUEST_IMMEDIATE_REEVALUATION`;
- `SUPERSEDE_NO_ACTION`;
- `REQUIRE_OPERATOR_REVIEW`.

## Side-effect safety — PASS

Customer-visible/destructive catch-up is not allowed merely because the occurrence is late. All downstream mode/approval/readiness/idempotency controls still apply.

---

# Recovery/HA review

## Restart before due — PASS

Future durable occurrences can be reconstructed/re-timed without changing identity.

## Downtime across due — PASS

Recovery classifies overdue occurrence through immutable missed-window policy.

## Crash before A-7 persistence — PASS

Recovery retries establishment of the same logical `TIME_DUE` event.

## Crash after A-7 persistence — PASS after V1.1

Recovery reconciles the already-existing semantic event using the schedule occurrence identity rather than creating a second semantic event.

## Multiple scheduler replicas — PASS

Correctness does not rely on a singleton scheduler.

---

# Clock/DST review

## Forward wall-clock jump — PASS

Occurrences may become overdue and are evaluated through missed-window policy; historical due identity does not move.

## Backward wall-clock jump — PASS

Already-emitted logical occurrences do not re-emit merely because current time moved backward.

## DST event-relative offset — PASS

Resolved UTC elapsed-duration arithmetic is stable.

## DST local recurrence ambiguity — PASS after V1.1

Occurrence identity retains local calendar intent plus disambiguation policy/selected offset/fold/resolved UTC instant.

---

# Plan/scope revision review

## Plan changes T-20m to T-15m — PASS

New plan/timing authority supersedes pending old plan resolution.

## Plan removes slot — PASS

Pending old slot is superseded/not applicable under new plan; history remains.

## Plan adds slot after target passed — PASS

New slot uses missed-window policy rather than blind backfill.

## Completed stage then reschedule — PASS

Completed StageRun remains attached to original schedule authority. Additional work requires plan/sport/reprocess policy.

---

# Technology-neutrality review

**PASS.**

Canonical schedule identity does not depend on Prefect, APScheduler, Kubernetes, cron, queue, or cloud-scheduler identifiers.

These may be runtime cross-references only.

---

# Stress-test matrix

| # | Scenario | Result | Review notes |
|---|---|---|---|
| 1 | MLB 19:10 game with T-24h/T-4h/T-120m/T-30m/T-20m | PASS | Each stable slot resolves independently from exact event authority. |
| 2 | MLB game moves two hours later before any slot fires | PASS | Old pending resolutions superseded; new resolutions retain same slots. |
| 3 | Game moves earlier and some future slots become missed | PASS | Each slot applies immutable missed-window policy; no mass immediate execution. |
| 4 | Game time changes multiple times | PASS | Revision lineage retained; only current authority schedules pending work. |
| 5 | Game postponed to TBD | PASS | Current anchor unresolved; stale old occurrences superseded. |
| 6 | TBD event receives start time | PASS | New authoritative resolution generated; no guessed placeholder history. |
| 7 | Game cancelled/no longer applicable | PASS | Pending occurrences retained as cancelled/not-applicable. |
| 8 | MLB doubleheader two opaque refs/times | PASS | Separate sport-owned anchors; TDLA infers no game ordering. |
| 9 | Zero-game day | PASS | No fake event timers; explicit slate/day stages may still schedule. |
| 10 | NFL flex/reschedule moves kickoff | PASS | Same generic revision/re-resolution model; no football branch. |
| 11 | NCAAF time initially incomplete then authoritative | PASS | Unresolved anchor becomes new valid resolution when authority appears. |
| 12 | `final_snapshot` keeps identity across kickoff move | PASS | Slot stable; resolution changes. |
| 13 | Old stale timer fires after new resolution | PASS | Old callback remains evidence; stale resolution cannot become current authority. |
| 14 | Duplicate physical callbacks | PASS | Same logical occurrence; duplicate physical evidence tolerated. |
| 15 | Two scheduler replicas race | PASS | Same occurrence identity; A-7/A-11 provide additional independent dedup defenses. |
| 16 | Restart before future due | PASS | Runtime timers reconstructed from durable authority. |
| 17 | Downtime across due | PASS | One occurrence classified via catch-up/missed policy. |
| 18 | Crash after due mark before A-7 trigger | PASS | Recovery creates/reconciles same semantic `TIME_DUE`. |
| 19 | Crash after A-7 trigger before A-8 emitted mark | PASS | Existing event found using occurrence identity; no second semantic event. |
| 20 | Due slot still readiness-blocked | PASS | Due only requests reevaluation; A-9/A-5 may continue WAITING. |
| 21 | Due slot dependency-blocked | PASS | Time eligibility does not satisfy missing dependency. |
| 22 | Late data trigger after deadline | PASS | Trigger cannot override current schedule/deadline authority. |
| 23 | Target passed but within grace | PASS | `REQUEST_REEVALUATION_IF_WITHIN_GRACE`; execution still downstream-gated. |
| 24 | Target/deadline passed with `SKIP_MISSED` | PASS | Missed evidence retained, no immediate execution. |
| 25 | Late customer-visible publication | PASS | Can require operator review; no generic catch-up publish. |
| 26 | T-60m event-relative offset crosses DST | PASS | UTC elapsed-duration arithmetic yields true 60 minutes. |
| 27 | Local recurrence spring-forward nonexistent time | PASS | Explicit recurrence policy required; no library-default guessing. |
| 28 | Local recurrence fall-back duplicate time | PASS | Disambiguation/selected fold-offset retained in occurrence identity. |
| 29 | System clock jumps forward | PASS | Occurrences may become overdue; one logical occurrence remains. |
| 30 | System clock jumps backward | PASS | Emitted occurrence does not re-emit. |
| 31 | Source timezone corrected, UTC event instant unchanged | PASS | New schedule authority may create new resolution; physical timer can be reused. |
| 32 | UTC event instant changes, display timezone unchanged | PASS | New anchor value creates new resolution. |
| 33 | Plan changes T-20m to T-15m | PASS | New resolved plan/timing authority supersedes pending old resolution. |
| 34 | Plan removes pending slot | PASS | Old resolution superseded/not applicable; no deletion. |
| 35 | Plan adds new future slot | PASS | New slot/materialization resolves normally under new plan. |
| 36 | Event moves after earlier snapshot completed | PASS | Completed evidence immutable; later plan determines additional work. |
| 37 | Event moves after final snapshot completed pre-kickoff | PASS | No implicit mutation/rerun; sport/plan policy decides. |
| 38 | Daily maintenance outage, policy says no catch-up | PASS | Missed recurrence recorded/skipped once. |
| 39 | Evaluation recurrence allows one catch-up | PASS | One logical overdue occurrence requests one reevaluation. |
| 40 | Same recurrence serialized differently | PASS | Canonical semantic recurrence/occurrence identity required. |
| 41 | Missing/unresolvable anchor | PASS | Explicit `UNRESOLVED_ANCHOR` or terminal validation error per declaration; no guessed time. |
| 42 | Naive datetime | PASS | Fail closed. |
| 43 | Earliest after deadline | PASS | Impossible window rejected. |
| 44 | Mutable/unversioned missed policy | PASS | Production resolution rejected. |
| 45 | Occurrence tied to superseded plan digest | PASS | Cannot become current execution authority. |
| 46 | Scope-set membership changes while slate schedule remains | PASS | Aggregate/event schedule authority remains revision-bound; no sport inference. |
| 47 | Event ref replaced by new sport ref | PASS | TDLA treats new sport authority explicitly; no inferred continuity. |
| 48 | Due occurrence in shadow mode | PASS | Downstream shadow side-effect constraints still apply. |
| 49 | Supervised customer-visible due slot | PASS | Stops at explicit approval boundary; due is not publish authority. |
| 50 | Production slot due | PASS | All A-7/A-9/A-11/side-effect/certification gates remain mandatory. |

---

# Additional failure-path review

## Same source schedule revision, conflicting anchor payload

Result: **PASS / fail closed**.

If the same claimed sport schedule authority/revision arrives with a different semantic anchor value without a new revision identity, the integration cannot silently mutate the resolution. It must be treated as an authority conflict under A-5/A-8 evidence rules.

## Due boundary omitted ambiguously

Result: **PASS after V1.1**.

A production timing declaration must explicitly identify how due time is selected.

## Old TIME_DUE already emitted before reschedule

Result: **PASS after V1.1**.

The old event remains historical evidence but current-authority validation prevents it from dispatching obsolete work after supersession.

## Two resolutions share same target instant

Result: **PASS after V1.1**.

Runtime wakeup may be shared; canonical resolutions/occurrences remain separate.

## Recurrence validity period ends before delayed catch-up

Result: **PASS**.

Catch-up evaluation must honor recurrence/plan validity and missed-window policy; expired authority is not revived by restart.

## Scheduler vendor migration

Result: **PASS**.

Runtime timer IDs can change while TDLA schedule resolution/occurrence identity and history remain stable.

---

# Daily-MLB compatibility note

A-8 does not require Daily-MLB to be automated now.

Future M13/M14 integration can map the certified manual MLB event/scope schedule authority into A-5/A-6/A-8 contracts.

Important constraints:

- MLB remains authority for game/event/schedule revision identity;
- TDLA does not infer postponements/doubleheaders from provider naming;
- pending event-relative slots re-resolve from MLB-supplied current authority;
- lineup/probable-pitcher readiness is not represented as a fake time anchor;
- schedule due events still pass through A-7/A-9 before execution.

---

# NFL / NCAAF compatibility note

A-8 supports multiple stable pre-kickoff slots and flex/reschedule changes while retaining slot identity.

This is compatible with the football PIT direction: later legitimate pregame information may produce/update later snapshots until kickoff, but schedule timing alone never determines readiness or sport meaning.

---

# Deferred-architecture review

A-8 correctly leaves unresolved:

- A-9 dependency/readiness state machine;
- A-10 worker dispatch/runtime;
- A-11 final logical execution idempotency/retry/timeout algorithms;
- A-12 generalized failure/recovery policies;
- A-13 database schema, transaction/outbox, lease/claim design;
- A-15 resource/concurrency scheduling;
- A-16 metrics/clock monitoring;
- A-17 scheduler alerting/incidents;
- A-19 operator review mechanics;
- A-20 authentication/service identity;
- A-21 HA/NTP/deployment topology.

This deferral is intentional and does not block A-8 architecture certification.

---

# Certification recommendation

**Recommend A-8 as `ARCHITECTURE-CERTIFIED` governed by:**

- `docs/architecture/A08_EVENT_RELATIVE_SCHEDULING_ENGINE_V1.md`;
- `docs/architecture/A08_EVENT_RELATIVE_SCHEDULING_ENGINE_ADDENDUM_V1_1.md`;
- `docs/adr/ADR-0005_STABLE_SCHEDULE_SLOTS_AND_RESOLVED_TIME_AUTHORITY.md`.

Certification grants architecture authority only. It does not certify a scheduler implementation, Prefect deployment, timer worker, database schema, live Daily-MLB/NFL/NCAAF scheduling, or production publication.

The next architecture checkpoint should be **A-9 Dependency / Readiness Engine**.