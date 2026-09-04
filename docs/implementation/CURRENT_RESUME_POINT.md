# The Daily Line Automation — Current Resume Point

Last updated: 2026-09-04 (America/Los_Angeles)  
Authority: This file is the single exact continuation point for unfinished TDLA work. It does not override architecture/certification authority; it tells the next session where to resume.

## Current project state

- Repository constitution/documentation-memory policy is authoritative in `AGENTS.md`.
- A-0 through A-4 Foundation V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-5 Sport Automation Adapter V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-6 Pipeline Plan / Stage Contracts V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-7 Trigger Architecture V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-7 review evidence: `docs/implementation/A07_ARCHITECTURE_CONFORMANCE_REVIEW_20260904.md`.
- ADR-0001 establishes TDLA canonical identity and replaceable orchestration runtime.
- ADR-0002 establishes transport-neutral Sport Automation Adapter protocol.
- ADR-0003 establishes immutable plan fragments, explicit typed composition, and `ResolvedAutomationPlan` authority.
- ADR-0004 establishes durable trigger evidence and reevaluation-only trigger authority.
- No production implementation milestone is certified.
- No TDLA automation is production-authoritative.
- Daily-MLB remains manual-first; later automation must prove equivalence after its final manual production pipeline is certified.

## Certified nested architecture through A-7

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
        +-----------------------------+
        |                             |
        v                             v
A-6 TimingDeclaration            A-7 TriggerBinding
        |                             |
        |                     TriggerDelivery
        |                             |
        |                     immutable TriggerEvent
        |                             |
        |                     TriggerEvaluation
        |                             |
        +--------------------> EligibilityReevaluationRequest
                                      |
                                      v
                           A-8/A-9 eligibility gates
                                      |
                                      v
                             StageRun / RunAttempt
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

## Important locked A-7 rules

1. A trigger requests eligibility reevaluation only; it never grants execution or side-effect authority.
2. Physical `TriggerDelivery` and semantic `TriggerEvent` identity are separate.
3. A source occurrence family and an immutable event revision are separate identities.
4. Redelivery of the same occurrence/revision remains one semantic event with multiple delivery evidence records.
5. Same occurrence/revision with a different semantic payload digest is an identity conflict and fails closed.
6. Corrections/retractions create new immutable event revisions/lineage; prior evidence is never overwritten/deleted.
7. `TriggerBinding` is immutable/versioned/digested and tied to exact resolved-plan/stage/scope authority.
8. `TriggerEvaluation` and logical `EligibilityReevaluationRequest` are distinct from physical processing attempts.
9. Accepted trigger evidence and reevaluation intent must be durable before downstream irreversible execution can occur.
10. Trigger deduplication and A-11 stage logical idempotency are separate defenses.
11. There is no global source-event ordering assumption based on receipt time or source wall clock.
12. Stale/out-of-order schedule/scope revisions cannot roll current authority backward.
13. A-7 time triggers represent A-8 due occurrences; A-7 does not calculate event-relative due times.
14. Stale old timer callbacks cannot revive superseded schedule work.
15. Sport-change/readiness events remain opaque hints; generic TDLA cannot interpret MLB/NFL/NCAAF event meaning.
16. A-5 readiness remains authoritative when a stage declares readiness is required.
17. Raw trigger events remain auditable even when burst events are coalesced.
18. Coalescing cannot silently cross incompatible resolved-plan/stage/scope/binding/environment authority revisions.
19. Valid triggers may match zero, one, or multiple bindings; each result is explicit/deterministic.
20. Late trigger arrival cannot bypass deadline/missed-window policy.
21. Ordinary authenticated operator triggers request reevaluation; overrides are separate A-19 actions.
22. Trigger replay/test ingress is explicitly labeled and environment/mode restricted.
23. Trigger source silence/outage is not proof that no domain change occurred.
24. Untrusted/signature-failed external delivery cannot create an authoritative semantic `TriggerEvent`.
25. Secret-bearing/malformed payloads are sanitized/rejected rather than persisted as normal event data.
26. No webhook, timer, callback, or ordinary operator trigger can directly publish, dispatch, or execute a destructive side effect.

## Daily-MLB / football compatibility note that must not be forgotten

Future sport integration can emit generic signals such as:

```text
SPORT_CHANGE_HINT(scope_ref, revision, opaque metadata)
PLAN_SCOPE_REVISION(scope_ref, revision)
READINESS_HINT(scope_ref, stage_ref)
```

TDLA records/routes the signal and asks the A-5 sport adapter for readiness/plan information where required.

TDLA must never implement:

```text
if MLB lineup posted -> run
if probable pitcher changed -> rerun
if NFL inactives final -> publish
```

Those meanings remain sport-owned.

Current Daily-MLB remains manual-first and is **not** production event-driven merely because A-7 is certified.

---

# Exact next step — A-8 Event-Relative Scheduling Engine

Design the generic scheduler that resolves A-6 timing declarations and stable `ScheduleSlotRef` identities against authoritative sport scope/event timing, produces durable schedule-occurrence authority, recalculates safely when event times change, classifies missed/late windows, and emits A-7 `TIME_DUE` trigger occurrences without creating duplicate logical work.

The central A-8 rule should be:

> **A scheduled wall-clock time is a resolution of a stable logical schedule slot under a specific scope/schedule revision. The clock timestamp is not the stage/snapshot identity, and changing the authoritative event time must supersede/recalculate pending occurrences rather than create uncontrolled duplicate logical stages.**

## A-8 must define at minimum

### 1. Scheduling authority entities

Define clear identity/contracts for concepts such as:

- `TimingDeclaration` (from A-6);
- stable `ScheduleSlotRef` (from A-6);
- `ScheduleAnchorRef` / anchor authority;
- `ScheduleResolution`;
- `ScheduleOccurrence` / due occurrence;
- occurrence revision/version/digest;
- missed-window evaluation/result;
- supersession lineage;
- actual A-7 `TIME_DUE` TriggerEvent handoff.

Exact names may change during design, but logical identities must remain separate.

### 2. Schedule anchor model

Support generic anchors without sport semantics, including at least:

- absolute UTC instant;
- A-5 sport event/scope start time;
- scope effective start/end when declared;
- stable plan-defined anchor references supplied by sport/platform contracts;
- potentially calendar/local recurring anchor for generic maintenance/publication operations.

TDLA must not invent a baseball/football-specific anchor such as “lineups posted.” Domain milestones that are not predictable times belong to trigger/readiness/dependency mechanisms rather than fake clock anchors.

### 3. Event-relative offset semantics

Define exact behavior for declarations such as:

```text
T-24h
T-8h
T-120m
T-30m
T-20m
T+post-event offset when a real time anchor exists
```

Relative duration arithmetic should be unambiguous and canonical. For event-relative elapsed durations, use absolute UTC instants/durations so DST/local-zone transitions do not distort a 60-minute offset.

### 4. Window model

A resolved slot must distinguish, where declared:

- earliest eligible time;
- target/due time;
- hard deadline/cutoff;
- validity/end time;
- optional grace interval;
- no-earlier-than/not-before semantics;
- exact policy reference for missed/late resolution.

Do not collapse all of these into one `scheduled_at` timestamp.

### 5. Stable slot identity vs resolved clock time

Preserve A-6 rule:

```text
ScheduleSlotRef = stable logical intent
resolved_at      = one clock resolution under a specific scope/schedule revision
```

Example:

```text
final_snapshot
  old kickoff 13:00 -> due 12:40
  new kickoff 16:00 -> due 15:40
```

The slot remains `final_snapshot`; the old occurrence is superseded and the pending new occurrence is a new schedule resolution/revision, not a brand-new sport-stage meaning.

### 6. Scope/schedule revision binding

Every event-relative resolution must bind to exact A-5/A-6 authority:

- `SportScopeRef`;
- scope/schedule revision;
- `StageMaterialization`;
- `ScheduleSlotRef`;
- resolved plan digest;
- timing-policy digest;
- event/anchor value used.

A stale occurrence cannot be evaluated as though it belonged to the newest schedule revision.

### 7. Reschedule recalculation

Define generic behavior when an authoritative event time moves:

- later;
- earlier;
- multiple times;
- to unknown/TBD;
- postponed to a later date;
- cancelled/no-longer-applicable;
- split/changed scope membership where the sport adapter supplies new refs.

Pending schedule occurrences may be superseded/replaced. Completed StageRuns remain immutable and attached to the authority they actually used.

### 8. Earlier reschedule crossing already-passed slots

Critical scenario:

```text
kickoff moves from 20:00 to 16:00 at 15:30
T-4h and T-2h are now already missed
T-20m is still ahead
```

A-8 must deterministically classify each slot using its declared missed-window policy rather than firing every overdue stage blindly.

### 9. Missed-window policy model

Define generic, versioned behavior for missed targets/windows. Candidate policy outcomes may include:

- `SKIP_MISSED`;
- `EXECUTE_IF_WITHIN_GRACE`;
- `REQUEST_IMMEDIATE_REEVALUATION`;
- `SUPERSEDE_NO_ACTION`;
- `REQUIRE_OPERATOR_REVIEW` where appropriate.

Exact enum names can be refined, but production behavior must be explicit, immutable/policy-bound, and side-effect aware.

A missed target is never automatically permission to execute late.

### 10. Unresolved/TBD event time

If the sport's authoritative event time is unknown or not yet reliable:

- do not invent a due clock;
- keep schedule resolution explicitly unresolved/waiting;
- re-resolve when the sport scope revision supplies an authoritative time;
- preserve prior revisions if a time was withdrawn/TBD after previously being set.

### 11. Timer occurrence identity

Define a durable logical timer/due occurrence identity sufficient for A-7 dedup and stale-fire detection.

It should bind at least:

- `StageMaterialization`;
- `ScheduleSlotRef`;
- schedule resolution/revision;
- target/due instant;
- plan/scope revisions;
- environment/mode.

A physical scheduler callback/worker attempt is not the logical due-occurrence identity.

### 12. A-7 TIME_DUE handoff

A-8 creates/resolves a due occurrence; A-7 records the resulting durable trigger event/delivery/evaluation.

A-8 must not call the sport stage directly.

```text
ScheduleOccurrence becomes due
    -> A-7 TIME_DUE TriggerEvent
        -> eligibility reevaluation
            -> A-9 readiness/dependencies
                -> later execution authority
```

### 13. Scheduler restart/recovery

No production correctness may depend solely on in-memory timers.

After restart, TDLA must be able to reconstruct/reconcile:

- pending future occurrences;
- overdue unresolved occurrences;
- already-emitted logical due occurrences;
- superseded schedule revisions;
- occurrences whose physical timer callback status is unknown.

Exact DDL/leases/outbox mechanics remain A-13/A-21, but the semantic recovery behavior belongs here.

### 14. Multiple scheduler instances / HA boundary

Architecture must tolerate two scheduler workers noticing the same logical due occurrence.

Physical duplicate fire may occur, but:

- both refer to the same logical `ScheduleOccurrence`/TIME_DUE semantic occurrence;
- A-7 delivery/event dedup handles repeated trigger delivery;
- A-11 still protects final StageRun logical idempotency.

Do not rely solely on “only one scheduler process will ever run.”

### 15. Clock model

Define authoritative clock semantics:

- durable timestamps are UTC;
- event/source IANA timezone retained for provenance/presentation;
- no naive datetimes;
- wall-clock UTC used for persistent due instants;
- monotonic process time may be used for local waits but never as persistent schedule identity;
- system clock skew/adjustment cannot silently change historical due identity.

Concrete NTP/infrastructure monitoring belongs later, but the architecture must account for clock correction/jump behavior.

### 16. DST/local calendar schedules

For any schedule defined in local civil time:

- retain IANA timezone;
- explicitly define ambiguous/nonexistent local-time handling during DST changes;
- never silently guess between duplicate local times;
- normalize resolved durable instants to UTC.

Event-relative offsets from an already resolved UTC event instant should use elapsed-duration arithmetic and not be distorted by DST.

### 17. Calendar/recurring scheduling boundary

A-8 should support generic periodic/operational schedules without making cron strings the canonical identity.

Define:

- recurrence rule/version identity;
- occurrence identity;
- timezone/calendar context;
- skip/catch-up semantics;
- plan validity interval.

A raw cron expression may be one implementation/serialization form, not permanent TDLA business identity.

### 18. Catch-up / overdue processing

When TDLA was down while due times passed:

- one logical due occurrence per schedule occurrence remains authoritative;
- recovery evaluates lateness/missed-window policy;
- it does not emit one duplicate for every restart scan;
- overdue side-effect stages remain subject to mode/deadline/approval policy.

### 19. Schedule resolution canonicalization/digest

Production resolution must deterministically capture execution-semantic scheduling inputs:

- declaration version/digest;
- slot identity;
- anchor identity/value;
- scope/schedule revision;
- resolved window;
- missed-window policy binding;
- recurrence/occurrence identity where applicable.

Cosmetic display metadata cannot alter semantic schedule identity unless declared semantic by schema.

### 20. No-games / empty-scope behavior

A zero-game sport day should produce no fake per-event timers.

Slate-level/daily stages may still have their own declared schedule slots if the resolved plan includes them.

### 21. Doubleheaders/multiple event scopes

Each sport-owned event scope has its own event-time anchor and schedule occurrences.

TDLA never infers which event is “game 1” or “game 2” from names/times; it uses A-5 refs supplied by the sport.

### 22. Completed stage vs later reschedule

If a stage already completed under the old event time:

- do not erase or silently move that completed StageRun;
- later schedule revision may materialize/supersede only work allowed by plan/reprocess policy;
- whether a new prediction snapshot is required is determined by the plan/sport contract, not by mutating old history.

### 23. Dependency/readiness independence

Being due does not mean ready.

A `TIME_DUE` trigger only causes eligibility reevaluation. A-9 may still hold the stage because:

- dependency missing;
- readiness `WAITING`/`BLOCKED`;
- required input stale;
- prior required stage failed;
- stage no longer applicable.

### 24. Side-effect/deadline safety

Customer-visible/destructive stages require especially explicit missed-window behavior.

A publication slot that is late after kickoff, for example, must not “catch up” automatically unless the resolved certified policy explicitly permits the exact side effect.

### 25. Plan revision vs schedule revision

Distinguish:

- same plan, sport event time changed;
- new resolved plan version with different timing declaration;
- same logical slot with changed schedule anchor;
- different logical slot added/removed.

Each requires explicit lineage/supersession rather than mutation.

### 26. Scheduler evaluation status model

Define auditable states/dispositions such as conceptually:

- `UNRESOLVED_ANCHOR`;
- `SCHEDULED`;
- `DUE`;
- `EMITTED`;
- `SUPERSEDED`;
- `MISSED_SKIPPED`;
- `MISSED_WITHIN_GRACE`;
- `WAITING_REEVALUATION`;
- `CANCELLED_NOT_APPLICABLE`;
- `ERROR_RETRYABLE` / `ERROR_TERMINAL`.

Names can be refined, but history must distinguish them.

### 27. No direct scheduler-to-executor path

Prohibit:

```text
timer fires -> worker runs sport command
```

Require:

```text
schedule occurrence due
-> A-7 TIME_DUE evidence
-> eligibility reevaluation
-> A-9 dependency/readiness/timing validation
-> A-11 idempotent execution
```

### 28. Technology neutrality

Do not make canonical schedule identity depend on:

- Prefect schedule/deployment ID;
- APScheduler job ID;
- cron daemon entry;
- Kubernetes CronJob UID;
- queue delayed-message ID.

These may be runtime cross-references only.

---

# A-8 stress cases before certification

At minimum test:

1. MLB game at 19:10 with T-24h, T-4h, T-120m, T-30m, T-20m slots.
2. Same MLB game moves two hours later before any slot fires.
3. Same game moves earlier and some formerly-future slots are now missed.
4. Game time changes multiple times in one day.
5. Game becomes postponed with no new start time (`TBD`).
6. Previously-TBD event receives authoritative start time.
7. Game is cancelled/no-longer-applicable.
8. MLB doubleheader has two opaque event refs/times and separate schedules.
9. Zero-game day creates no fake event timers.
10. NFL kickoff time moves because of flex/reschedule.
11. NCAAF event time initially incomplete then becomes authoritative.
12. Stable `final_snapshot` slot keeps identity when kickoff moves.
13. Old stale timer callback fires after new schedule resolution exists.
14. Duplicate physical scheduler callbacks for the same logical occurrence.
15. Two scheduler replicas race on one due occurrence.
16. TDLA restarts before a future due time.
17. TDLA is down across the due time and restarts afterward.
18. TDLA crashes after marking occurrence due but before A-7 trigger persistence.
19. TDLA crashes after A-7 trigger persistence but before schedule occurrence is marked emitted/reconciled.
20. Due slot is still blocked by readiness.
21. Due slot is still blocked by dependency.
22. Late data trigger arrives after deadline; scheduler timing authority still blocks unauthorized execution.
23. Target time passed but still within declared grace interval.
24. Target and deadline both passed; `SKIP_MISSED` policy.
25. Missed customer-visible publication slot requiring manual review rather than catch-up.
26. Event-relative T-60m calculation crosses a DST boundary.
27. Local recurring schedule falls into nonexistent spring-forward local time.
28. Local recurring schedule falls into duplicated fall-back local time.
29. System wall clock jumps forward.
30. System wall clock jumps backward.
31. Event source timezone changes/correction but absolute UTC event instant remains same.
32. Sport event UTC instant changes but display timezone metadata does not.
33. Plan revision changes T-20m slot to T-15m before execution.
34. Plan revision removes a pending slot.
35. Plan revision adds a new future slot.
36. Event time changes after an earlier snapshot already completed.
37. Event time changes after final snapshot completed but before kickoff.
38. Recurring daily maintenance schedule skipped during TDLA outage and catch-up policy says no retroactive run.
39. Recurring evaluation schedule permits one catch-up occurrence.
40. Same recurrence definition serializes differently but canonical occurrence identity remains deterministic.
41. Schedule declaration references missing/unresolvable anchor.
42. Naive datetime appears in schedule input.
43. Impossible window: earliest start after deadline.
44. Mutable/unversioned missed-window policy in production resolution.
45. Schedule occurrence belongs to superseded plan digest.
46. Scope-set membership changes while slate-level aggregate schedule remains.
47. Event scope is replaced by new sport-owned scope ref; TDLA does not infer identity continuity.
48. Due occurrence matches shadow mode and must not reach production side effects.
49. Supervised customer-visible slot becomes due but stops at operator approval boundary.
50. Production slot becomes due; every downstream gate still must pass.

---

# Expected A-8 outputs

Create at minimum:

- `docs/architecture/A08_EVENT_RELATIVE_SCHEDULING_ENGINE_V1.md`;
- A-8 V1.1 addendum if review exposes ambiguities;
- A-8 architecture conformance/certification review with stress matrix;
- ADR if clock/schedule authority or missed-window semantics introduce a durable new tradeoff;
- updated ADR index;
- updated architecture index;
- updated `ARCHITECTURE_CERTIFICATION_LOG.md`;
- detailed `CHANGE_JOURNAL.md` entry;
- updated root `README.md`;
- updated `CURRENT_RESUME_POINT.md` pointing to A-9.

## Do not do yet

Until A-8 is certified:

- do not implement final scheduler Pydantic models as frozen authority;
- do not add real cron/Prefect/APScheduler/Kubernetes scheduling jobs;
- do not design PostgreSQL scheduler DDL around guessed fields;
- do not wire Daily-MLB/NFL/NCAAF live schedules into automation;
- do not make clock timestamps part of sport snapshot semantic identity;
- do not invent sport-specific reschedule logic inside TDLA;
- do not implement A-9 dependency/readiness state machine prematurely;
- do not enable production publication/catch-up behavior.

## Required reading for next session

1. `README.md`
2. `AGENTS.md`
3. this file
4. `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`
5. `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`
6. `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md`
7. `docs/architecture/A07_TRIGGER_ARCHITECTURE_V1.md`
8. `docs/architecture/A07_TRIGGER_ARCHITECTURE_ADDENDUM_V1_1.md`
9. `docs/implementation/A07_ARCHITECTURE_CONFORMANCE_REVIEW_20260904.md`
10. `docs/adr/ADR-0003_IMMUTABLE_PLAN_FRAGMENTS_AND_EXPLICIT_COMPOSITION.md`
11. `docs/adr/ADR-0004_DURABLE_TRIGGER_EVIDENCE_AND_REEVALUATION_ONLY_AUTHORITY.md`
12. current A-5 sport adapter contracts for scope/schedule revision authority.

The next architecture checkpoint is **A-8 Event-Relative Scheduling Engine**.
