# A-8 — Event-Relative Scheduling Engine V1

Status: **DOCUMENTED — REVIEW PENDING**  
Repository: `OneVillage83/The-Daily-Line-Automation`  
Architecture section: A-8  
Version: 1.0  
Initial documentation date: 2026-09-04

This document defines the generic scheduling architecture that resolves A-6 timing declarations and stable `ScheduleSlotRef` identities against authoritative time anchors, preserves schedule revisions and supersession, classifies late/missed occurrences, and emits A-7 `TIME_DUE` evidence without directly executing sport work.

A-8 intentionally defines scheduling semantics rather than a specific scheduler product. Prefect schedules, APScheduler jobs, Kubernetes CronJobs, delayed queue messages, operating-system cron entries, and in-process timers may later implement parts of this contract, but none are canonical TDLA scheduling identity or audit authority.

---

# A-8.0 — Governing rule

> **A wall-clock timestamp is a resolution of a stable logical schedule slot under a specific immutable timing declaration and anchor/scope authority. The timestamp is not the stage/snapshot identity. When authoritative timing changes, pending schedule authority is superseded/re-resolved rather than silently mutated or duplicated.**

The scheduler therefore answers:

- Which logical schedule slot is being resolved?
- Which exact timing declaration/policy produced it?
- Which exact anchor/scope/schedule revision supplied the time authority?
- What UTC window was resolved?
- Is the occurrence pending, due, emitted, missed, superseded, unresolved, or no longer applicable?
- Has A-7 already received the logical `TIME_DUE` occurrence?
- If TDLA was down or the event moved, what declared missed-window policy applies?

The scheduler does **not** answer:

- whether an MLB lineup is ready;
- whether an NFL inactive list is final;
- whether a model should rerun;
- whether a dependency is satisfied;
- whether publication should be approved;
- whether an execution retry is allowed.

Those meanings remain in A-5/A-9/A-11/A-12/A-19 and sport-owned contracts.

---

# A-8.1 — Scheduling authority layers

A-8 separates six identities that must not be collapsed.

```text
TimingDeclaration
    |
ScheduleSlotRef
    |
ScheduleAnchorRef + exact anchor revision/value
    |
ScheduleResolution
    |
ScheduleOccurrence
    |
physical scheduler callback/scan/claim attempt
```

## A-8.1.1 `TimingDeclaration`

The versioned A-6 declaration that says how a slot should be resolved. It may define:

- anchor reference;
- offset/duration;
- earliest/not-before boundary;
- target/due boundary;
- deadline/cutoff;
- validity/end boundary;
- grace/missed-window policy reference;
- recurrence rule reference when applicable.

A production resolution binds the exact declaration version/digest.

## A-8.1.2 `ScheduleSlotRef`

Stable logical scheduling intent from A-6, for example conceptually:

- `early_context`;
- `late_refresh`;
- `final_snapshot`;
- `settlement_check`;
- `daily_maintenance`.

TDLA treats sport-owned slot names as opaque identifiers. A clock timestamp is never substituted for slot identity.

## A-8.1.3 `ScheduleAnchorRef`

A typed reference identifying the authority from which time is resolved.

Supported V1 anchor classes include:

- `ABSOLUTE_UTC_INSTANT`;
- `SPORT_SCOPE_EVENT_START`;
- `SPORT_SCOPE_EFFECTIVE_START`;
- `SPORT_SCOPE_EFFECTIVE_END`;
- `PLAN_DECLARED_ABSOLUTE_ANCHOR`;
- `LOCAL_CALENDAR_ANCHOR` for explicitly calendar-defined platform operations;
- `RECURRENCE_OCCURRENCE_ANCHOR` for a resolved recurring occurrence.

A sport-defined milestone with unknown future timing such as "lineup posted" or "inactives final" is **not** a clock anchor unless the sport contract actually supplies an authoritative timestamp. Such domain changes belong to A-7 trigger/A-5 readiness mechanisms.

## A-8.1.4 `ScheduleResolution`

Immutable record of resolving one slot under one exact authority set.

Conceptually:

```text
ScheduleResolution
- resolution_id
- schema_version
- stage_materialization_ref
- schedule_slot_ref
- timing_declaration_ref/version/digest
- resolved_plan_digest
- sport_scope_ref + scope/schedule revision when applicable
- schedule_anchor_ref
- anchor_value_utc or unresolved reason
- anchor_revision/digest
- resolved_earliest_at
- resolved_target_at
- resolved_deadline_at
- resolved_valid_until
- resolved_grace_until where applicable
- missed_window_policy binding/version/digest
- recurrence occurrence ref where applicable
- environment
- execution_mode
- resolved_at
- resolution_digest
- supersedes/superseded_by lineage
```

The exact database schema is deferred to A-13.

## A-8.1.5 `ScheduleOccurrence`

Logical due occurrence generated from a valid schedule resolution.

Conceptually:

```text
ScheduleOccurrence
- occurrence_id
- occurrence_key / semantic identity
- schedule_resolution_id/digest
- stage_materialization_ref
- schedule_slot_ref
- due_target_at
- effective due window
- plan/scope/schedule revisions
- environment/mode
- occurrence_status
- due_observed_at
- emitted_time_due_event_ref when present
- supersession lineage
```

A physical scheduler process waking up is not a `ScheduleOccurrence`.

## A-8.1.6 physical scheduler attempt

A runtime scan, lease acquisition, delayed-message delivery, Prefect callback, process wakeup, or worker attempt is physical evidence only.

Multiple physical attempts may correspond to one logical occurrence.

---

# A-8.2 — Time representation and arithmetic

## A-8.2.1 UTC persistence rule

All durable resolved instants are timezone-aware UTC timestamps.

Naive datetimes are invalid in production scheduling contracts.

Meaningful source/event/local IANA timezone metadata is retained separately for provenance, presentation, and local-calendar recurrence interpretation.

## A-8.2.2 Event-relative elapsed duration arithmetic

For a resolved event instant, event-relative offsets use elapsed-duration arithmetic on the resolved UTC instant.

Example:

```text
event_start = 2026-09-10T02:10:00Z
T-120m      = 2026-09-10T00:10:00Z
```

A DST transition in the venue timezone does not turn a two-hour elapsed offset into one or three hours.

## A-8.2.3 Local civil-time schedules

Calendar schedules explicitly defined in local civil time retain:

- IANA timezone;
- local date/time expression;
- ambiguous-time policy;
- nonexistent-time policy;
- resolved UTC occurrence.

The architecture does not silently guess during fall-back duplicate local times or spring-forward nonexistent local times.

## A-8.2.4 monotonic process time

Monotonic clocks may be used for process-local sleeps/timeouts, but monotonic values are never durable schedule identity or historical due timestamps.

---

# A-8.3 — Timing window contract

A-8 does not collapse scheduling into one `scheduled_at` value.

A resolved timing window may contain:

- `earliest_at` — stage must not become time-eligible before this;
- `target_at` — preferred due instant;
- `deadline_at` — hard latest time for the declared purpose;
- `valid_until` — validity boundary when distinct from deadline;
- `grace_until` — optional policy-bound late execution/reevaluation boundary.

Not every slot requires every field. Missing fields must have defined schema semantics rather than being guessed.

Validation includes:

```text
earliest_at <= target_at <= deadline_at <= valid_until
```

for fields that coexist, except where a versioned schema explicitly defines a different valid relation.

Impossible windows fail before due emission.

---

# A-8.4 — Stable slot identity vs resolved time

Example:

```text
ScheduleSlotRef = final_snapshot
TimingDeclaration = EVENT_START - 20m
```

Initial authority:

```text
event revision r7
start = 13:00
resolution R1 target = 12:40
```

Sport later supplies:

```text
event revision r8
start = 16:00
```

A-8 creates:

```text
same ScheduleSlotRef final_snapshot
R1 -> SUPERSEDED
R2 target = 15:40 under r8
```

It does not rename the snapshot, mutate R1, or infer that two different logical snapshot types exist.

A schedule change alone also does not automatically imply that already-completed sport work must rerun. Completed StageRuns remain immutable; plan/sport/reprocess policy decides whether additional materialization/work is required.

---

# A-8.5 — Anchor authority and unresolved anchors

## A-8.5.1 authoritative value required

A schedule resolution must identify the exact anchor value and the authority revision/digest from which it came.

For a sport event anchor, the authoritative event time comes through sport-owned A-5 scope/schedule authority. TDLA does not resolve conflicting league/provider IDs itself.

## A-8.5.2 unknown/TBD

When the required anchor is unknown:

```text
resolution disposition = UNRESOLVED_ANCHOR
```

TDLA must not invent a placeholder due clock.

When an authoritative anchor later appears, a new resolution is produced.

## A-8.5.3 anchor withdrawal

If a previously known start time becomes TBD/postponed without replacement:

- prior resolution remains historical evidence;
- pending occurrences tied to the old authority are superseded;
- current slot becomes unresolved under the new scope/schedule revision;
- stale old callbacks cannot revive the superseded occurrence.

## A-8.5.4 cancelled/not applicable

When sport authority declares the scope cancelled/no longer applicable and the plan contract supports that disposition, pending schedule resolutions/occurrences transition through explicit cancellation/not-applicable supersession rather than being deleted.

---

# A-8.6 — Schedule resolution identity and digest

A production `ScheduleResolution` has deterministic semantic identity over execution-affecting fields including at least:

- schema version;
- stage materialization identity;
- schedule slot identity;
- timing declaration version/digest;
- resolved plan digest;
- sport scope reference/revision where applicable;
- anchor type/ref/revision/value;
- resolved window boundaries;
- missed-window policy version/digest;
- recurrence occurrence identity where applicable;
- environment/mode.

Presentation labels, UI descriptions, and non-semantic diagnostics participate only when the versioned schema declares them semantic.

Canonicalization follows the same architecture discipline established by A-6: deterministic normalization plus SHA-256, with implementation test vectors required later.

---

# A-8.7 — Logical schedule occurrence identity

A logical due occurrence must be stable across physical scheduler retries/replicas.

Its semantic key binds the exact schedule authority, conceptually:

```text
hash(
  environment,
  resolved_plan_digest,
  stage_materialization_ref,
  schedule_slot_ref,
  schedule_resolution_digest,
  recurrence_occurrence_ref if any
)
```

The exact serialization/key format is finalized during contract implementation/A-11/A-13 integration, but these semantics are mandatory.

Changing only the scheduler runtime worker or callback ID does not create a new occurrence.

A superseding schedule resolution creates a distinct occurrence authority linked to the prior resolution. It does not overwrite the old occurrence.

---

# A-8.8 — Occurrence lifecycle/dispositions

V1 conceptually supports at least:

- `UNRESOLVED_ANCHOR`;
- `SCHEDULED`;
- `DUE`;
- `TIME_DUE_EMIT_PENDING`;
- `EMITTED`;
- `SUPERSEDED`;
- `MISSED_SKIPPED`;
- `MISSED_WITHIN_GRACE`;
- `MISSED_REEVALUATION_REQUESTED`;
- `OPERATOR_REVIEW_REQUIRED`;
- `CANCELLED_NOT_APPLICABLE`;
- `ERROR_RETRYABLE`;
- `ERROR_TERMINAL`.

Exact persisted state-machine mechanics remain A-13/A-12 implementation work, but these meanings must remain distinguishable in audit history.

`EMITTED` means the logical A-7 `TIME_DUE` evidence has been durably established/reconciled, not that the sport stage ran successfully.

---

# A-8.9 — Due determination

A scheduler evaluation may determine a pending occurrence is due when the authoritative clock is at/past its target/eligible boundary under the resolved declaration.

Due determination does not grant execution.

```text
ScheduleOccurrence DUE
    -> durable A-7 TIME_DUE TriggerEvent
        -> EligibilityReevaluationRequest
            -> A-9 dependencies/readiness
                -> later StageRun authority
```

If readiness remains `WAITING`, the same logical stage/materialization remains pending under A-9 logic. A-8 does not create repeated snapshot identities merely because readiness is checked again.

---

# A-8.10 — A-7 `TIME_DUE` handoff

A-8 and A-7 share a strict boundary.

A-8 supplies a stable logical due-occurrence identity and scheduling provenance.

A-7 creates/retains the durable trigger evidence with conceptually:

```text
trigger_kind = TIME_DUE
source_namespace = tdla.scheduler
source_occurrence_id = schedule occurrence identity
source_revision = schedule resolution revision/digest
occurred_at = resolved due occurrence time / due detection semantics
received_at = actual A-7 ingress time
payload = safe schedule refs/digests
```

Duplicate physical scheduler callbacks map to the same semantic due occurrence/source occurrence.

A-8 never invokes a sport adapter or executor directly.

---

# A-8.11 — Reschedule recalculation

An authoritative sport scope/schedule revision can require a new resolution for every pending event-relative slot affected by the anchor change.

Generic cases:

## Later move

Future pending occurrences are superseded/re-resolved later.

Already emitted/completed history remains historical evidence.

## Earlier move

Each affected slot is independently re-resolved. If the new target/window is already past, A-8 evaluates its immutable missed-window policy. It does **not** fire every overdue stage blindly.

## Multiple moves

Every schedule authority revision is retained. Only the currently authoritative pending resolution may produce current due work.

## TBD/postponed

Pending old occurrences are superseded and current resolution becomes unresolved until a new authoritative anchor exists.

## cancellation

Pending schedule work is marked cancelled/not-applicable under plan/sport authority; nothing is deleted.

## scope replacement/split

If the sport adapter supplies new scope references, TDLA treats them according to new sport-owned authority and plan lineage. It does not infer continuity from team/date/time similarity.

---

# A-8.12 — Earlier reschedule and missed slots

Critical example:

```text
original start: 20:00
new start:      16:00
change learned: 15:30
```

Suppose slots are:

```text
T-4h  -> new target 12:00  already missed
T-2h  -> new target 14:00  already missed
T-20m -> new target 15:40  still future
```

A-8 produces three independent classifications using their resolved immutable policies.

Possible result:

```text
T-4h  -> MISSED_SKIPPED
T-2h  -> MISSED_REEVALUATION_REQUESTED
T-20m -> SCHEDULED for 15:40
```

No generic rule says "all overdue stages execute immediately."

---

# A-8.13 — Missed-window policy contract

A production timing declaration resolves to an immutable missed-window policy version/digest.

V1 policy outcome families include conceptually:

- `SKIP_MISSED` — retain missed evidence, no immediate time-due reevaluation;
- `EXECUTE_IF_WITHIN_GRACE` — if current time is within declared grace, emit one late reevaluation cause; downstream gates still apply;
- `REQUEST_IMMEDIATE_REEVALUATION` — request one reevaluation even though preferred target was missed; does not guarantee execution;
- `SUPERSEDE_NO_ACTION` — old slot is superseded with no current action;
- `REQUIRE_OPERATOR_REVIEW` — create an explicit review-required scheduling outcome; operator action semantics remain A-19.

Exact enum names/implementation are versioned contracts, but these distinctions are mandatory.

## A-8.13.1 side-effect-aware lateness

Customer-visible or destructive stages must never rely on a generic "catch up everything" default.

A publication stage late after kickoff, for example, cannot auto-publish unless its exact certified timing/side-effect/mode policy explicitly permits the action and all later gates pass.

---

# A-8.14 — Scheduler restart and catch-up

Production correctness cannot depend on in-memory timers.

After startup/recovery, the scheduler reconciles durable current schedule authority and classifies each occurrence:

- future -> remain/rebuild runtime timer;
- due but not emitted -> establish/reconcile one logical `TIME_DUE` event;
- overdue -> apply missed-window policy;
- emitted -> do not emit a new semantic due event merely because the process restarted;
- superseded -> ignore for current authority while retaining audit evidence;
- unresolved anchor -> wait for new anchor authority.

Repeated restart scans must converge on the same logical occurrence/evaluation state.

---

# A-8.15 — Crash windows and durable intent

A-8 must remain correct across at least these crash windows.

## Crash after occurrence becomes due, before A-7 event exists

Recovery recognizes due occurrence with no durable corresponding `TIME_DUE` event and retries/reconciles creation of the same semantic event.

## Crash after A-7 event persists, before A-8 marks occurrence emitted

Recovery looks up/reconciles A-7 by the stable schedule occurrence/source occurrence identity and marks/reconciles the existing event rather than creating a new semantic event.

The exact transaction/outbox protocol belongs to A-13, but the required semantic behavior is certified here.

---

# A-8.16 — Multiple scheduler replicas / HA

A-8 assumes more than one scheduler process may observe a due occurrence.

Required behavior:

```text
replica A sees occurrence O due
replica B sees occurrence O due
```

Both must refer to the same logical occurrence O.

Runtime leases/locks may reduce duplicate work, but correctness cannot rely only on a singleton scheduler.

A-7 event identity/dedup and A-11 final StageRun idempotency remain independent additional defenses.

---

# A-8.17 — Clock skew and jumps

The persistent scheduler uses UTC wall-clock instants as resolved due authority, while runtime timing should tolerate clock correction.

If the system clock jumps:

- historical `target_at`/resolution identity never changes;
- scheduler reevaluates current time against durable due authority;
- one logical occurrence remains one occurrence;
- a backward jump must not re-emit an already-emitted due occurrence;
- a forward jump may make occurrences overdue, which then use missed-window/catch-up policy.

NTP/clock health alerting is operational work under later deployment/observability architecture.

---

# A-8.18 — DST and timezone behavior

## Event-relative slots

Once the event anchor is an aware UTC instant, elapsed offsets are computed in UTC.

## Local recurring schedules

For civil-time recurrence, the plan must declare handling for:

- nonexistent local times during spring-forward;
- ambiguous repeated local times during fall-back.

Permitted policy families may include:

- shift to next valid instant;
- skip the occurrence;
- choose earlier offset;
- choose later offset;
- require explicit resolution/fail closed.

The exact choice is part of the recurrence declaration/policy and must not be an implicit library default.

---

# A-8.19 — Recurring/calendar scheduling

A-8 supports recurring platform operations without making a cron string canonical identity.

Conceptual `RecurrenceDefinition` includes:

- recurrence namespace/id;
- schema/version/digest;
- calendar/timezone context;
- recurrence expression/rule;
- effective_from/effective_until;
- ambiguous/nonexistent local-time policy;
- missed/catch-up policy;
- environment/mode.

Each derived recurrence occurrence gets stable occurrence identity from the recurrence definition plus logical calendar occurrence, not from a scheduler vendor job ID.

A cron expression may be a serialized rule representation but is not itself sufficient permanent authority.

---

# A-8.20 — Plan revision vs schedule revision

A-8 distinguishes at least:

### same plan, sport event anchor changes

New `ScheduleResolution` under new scope/schedule revision; stable slot remains.

### plan changes timing declaration

New resolved plan/timing declaration authority. Old pending resolution is superseded; new plan creates its own current resolution.

### plan removes a slot

Pending resolution becomes superseded/not applicable under the new plan. Historical completed/emitted evidence remains.

### plan adds a slot

New stage/slot materialization follows A-6 plan revision rules; if its target is already past, missed-window policy is evaluated rather than blindly backfilled.

These cases are not silently conflated.

---

# A-8.21 — Completed work and later schedule changes

A schedule resolution does not rewrite completed StageRun history.

Example:

```text
final_snapshot completed at 12:40 under event revision r7
kickoff later moves from 13:00 to 16:00 under r8
```

The completed snapshot remains attached to r7/resolution R1.

Whether r8 should produce another prediction snapshot is determined by the certified plan/sport contract and materialization/supersession policy, not by mutating the old StageRun timestamp.

---

# A-8.22 — Dependency/readiness independence

A stage can be time-due but not executable.

A-8 only establishes time evidence/reevaluation cause.

A-9 may still return/derive states such as:

- dependency waiting;
- readiness waiting;
- blocked;
- stale required input;
- prior required failure;
- not applicable.

Thus:

```text
DUE != READY
DUE != DISPATCHED
DUE != SUCCEEDED
```

---

# A-8.23 — No-games, slates, and multiple event scopes

## Zero-game day

No per-event `SportScopeRef` means no fake event timer is created.

A slate/day/platform stage may still have its own explicit plan-defined schedule.

## Doubleheader/multiple events

Each sport-owned event ref has its own anchor and schedule resolutions.

TDLA does not decide game ordering or canonical continuity from names/times.

## membership revision

A changed A-6 `ScopeSetBinding` may affect slate aggregation or future materializations. Event schedule authority remains attached to exact sport refs/membership revisions.

---

# A-8.24 — Validation/fail-closed conditions

A schedule cannot become production-current when any required condition fails, including:

- missing/unresolvable required anchor;
- naive datetime;
- malformed timezone;
- impossible window;
- timing declaration digest mismatch;
- scope/schedule revision mismatch;
- unresolved mutable missed-window policy;
- plan digest mismatch;
- duplicate/conflicting current resolution identity;
- recurrence rule/version incompatibility;
- ambiguous/nonexistent local time without declared handling;
- stale resolution presented as current after supersession;
- mutable scheduler runtime ID used as canonical authority;
- side-effect/mode timing policy contradiction.

An unresolved anchor may be a valid waiting state rather than an error when the plan declares that possibility.

---

# A-8.25 — Technology-neutral runtime mapping

Implementations may use one or more of:

- Prefect scheduling APIs;
- database-driven scanner/claim workers;
- delayed queue messages;
- APScheduler;
- Kubernetes CronJobs;
- OS cron for limited maintenance wrappers;
- cloud scheduling services.

But runtime IDs are cross-references only.

Replacing the scheduler engine must preserve:

- slot identity;
- resolution identity/digest;
- occurrence identity;
- supersession lineage;
- missed-window result;
- A-7 causal trigger linkage.

---

# A-8.26 — Explicit deferrals

A-8 deliberately does not finalize:

- A-9 dependency/readiness state-machine algorithms;
- A-10 worker/backend dispatch;
- A-11 exact final execution idempotency/retry key format;
- A-12 failure recovery policies beyond scheduler-specific dispositions;
- A-13 PostgreSQL tables, locks, leases, transactions/outbox;
- A-15 resource scheduling;
- A-16 clock/scheduler metrics implementation;
- A-17 alert thresholds/incidents;
- A-19 operator approval UI/actions;
- A-20 service authentication;
- A-21 HA topology/NTP infrastructure.

These later sections must conform to A-8 semantic identity/recovery rules.

---

# A-8.27 — Required implementation test vectors

When M1/M4 implementation begins, create deterministic contract tests for at least:

1. same slot/declaration/anchor authority -> same schedule resolution digest;
2. same semantic data serialized in different incidental order -> same digest;
3. changed event start revision -> new resolution digest while slot identity remains;
4. two physical scheduler callbacks -> one logical occurrence identity;
5. stale superseded occurrence cannot emit current `TIME_DUE` authority;
6. crash-after-A7-persist recovery finds the existing trigger event;
7. event-relative UTC arithmetic across DST produces correct elapsed offset;
8. ambiguous/nonexistent local recurrence follows explicit declared policy;
9. mutable/unversioned production timing policy fails resolution;
10. missed-window outcome is deterministic from immutable inputs/policy.

---

# A-8.28 — Certification criteria

A-8 may be architecture-certified when review shows that:

- logical slot identity is independent of wall-clock timestamp;
- exact anchor/scope/plan/timing policy authority is retained;
- reschedules supersede/re-resolve rather than mutate;
- earlier reschedules deterministically classify newly missed slots;
- TBD/cancelled states are explicit;
- restart/replica races converge on one logical due occurrence;
- A-7 handoff is durable/idempotency-aware;
- missed-window behavior is explicit and side-effect safe;
- local calendar/DST behavior is explicit;
- schedule engine remains sport-neutral and vendor-neutral;
- completed StageRun history remains immutable;
- no direct scheduler-to-executor path exists.

Certification grants architecture authority only. It does not certify any scheduler implementation, database schema, live sport integration, or production automation.