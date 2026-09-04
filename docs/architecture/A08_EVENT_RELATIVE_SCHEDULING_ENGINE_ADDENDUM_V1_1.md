# A-8 Event-Relative Scheduling Engine — Certification Addendum V1.1

Date: 2026-09-04  
Status: **CERTIFICATION CLARIFICATION — governs A-8 V1 together with the base document**

This addendum records clarifications identified during the A-8 architecture conformance review. It does not replace `A08_EVENT_RELATIVE_SCHEDULING_ENGINE_V1.md`; the two documents together form the certified A-8 contract if certification is granted.

## 1. Missed-window policy names must preserve reevaluation-only scheduler authority

The A-8 V1 base describes a candidate policy family named conceptually `EXECUTE_IF_WITHIN_GRACE` while also stating correctly that the scheduler only emits a reevaluation cause.

That name is too easy for a future implementation to misread as scheduler execution authority.

The normative V1.1 policy family is therefore:

- `SKIP_MISSED`;
- `REQUEST_REEVALUATION_IF_WITHIN_GRACE`;
- `REQUEST_IMMEDIATE_REEVALUATION`;
- `SUPERSEDE_NO_ACTION`;
- `REQUIRE_OPERATOR_REVIEW`.

A-8 never directly executes sport work, including during grace/catch-up handling.

Even when `REQUEST_REEVALUATION_IF_WITHIN_GRACE` applies:

```text
missed schedule occurrence
    -> one A-7 late TIME_DUE / reevaluation cause
        -> A-9 dependencies/readiness/current-authority checks
            -> A-11 idempotent execution only if later authorized
```

## 2. Same absolute event instant under a new schedule revision still creates new schedule authority

A sport scope/schedule revision may change while the event's absolute UTC start instant remains unchanged. Examples include provider reconciliation, timezone/display correction, or another sport-owned schedule metadata revision.

Because A-8 binds schedule resolution to exact sport schedule authority, a new authoritative scope/schedule revision creates a new `ScheduleResolution` authority even when the resolved UTC window is numerically identical.

Required behavior:

```text
r7 start = 20:00Z -> resolution R7 target = 19:40Z
r8 start = 20:00Z -> resolution R8 target = 19:40Z
```

- `ScheduleSlotRef` remains the same;
- R7 remains immutable historical evidence;
- R8 becomes current authority;
- runtime infrastructure MAY reuse/coalesce the same physical timer instant when safe;
- runtime coalescing must not collapse R7/R8 provenance or make an old stale callback authoritative for R8;
- if a semantic `TIME_DUE` event was already emitted under R7, later authority handling follows current-stage/supersession policy rather than pretending R7 never existed.

This preserves exact authority history without requiring redundant physical timer creation solely because metadata revision changed.

## 3. One canonical semantic TIME_DUE event per logical ScheduleOccurrence

A logical `ScheduleOccurrence` may experience many physical scheduler callbacks, scans, leases, or retries, but it has at most one canonical semantic A-7 `TIME_DUE` source occurrence for that exact schedule-occurrence authority.

The A-7 source occurrence identity must be deterministically derived from or uniquely bound to the A-8 logical `ScheduleOccurrence` identity.

Required crash-safe invariant:

```text
ScheduleOccurrence O
    -> zero or one canonical TriggerEvent TIME_DUE(O)
    -> zero or many physical TriggerDeliveries/processing attempts
```

If TDLA crashes after A-7 has durably created `TIME_DUE(O)` but before A-8 records the linkage, recovery must reconcile the existing semantic event using O's stable identity. Creating `TIME_DUE_2(O)` as a second semantic event is non-conforming.

The exact transaction/outbox/unique-index implementation remains A-13.

## 4. Due-time selection when target is omitted must be explicit

A resolved timing declaration may omit `target_at` for some generic operations. The scheduler must not guess which remaining boundary is the due instant.

The timing schema must explicitly declare a due-boundary rule, conceptually one of:

- `TARGET` — `target_at` is required and is the due instant;
- `EARLIEST` — `earliest_at` is the due instant;
- `ABSOLUTE_ANCHOR` — the resolved anchor itself is the due instant;
- `RECURRENCE_OCCURRENCE` — the recurrence occurrence instant is the due instant.

A production declaration lacking enough information to deterministically identify the due boundary fails closed.

`earliest_at` remains a no-earlier-than constraint unless the declaration explicitly selects it as the due boundary.

## 5. Stale emitted timer authority must be revalidated before dispatch

A schedule occurrence can become stale after its `TIME_DUE` event has already been emitted but before the sport stage actually dispatches.

Example:

```text
R1 final_snapshot target 12:40
12:40 -> TIME_DUE(R1) emitted
12:41 -> event rescheduled; R1 superseded by R2
12:42 -> downstream evaluation of old TIME_DUE(R1) resumes
```

The old trigger remains valid historical evidence but cannot authorize current execution.

A-9/later dispatch eligibility must validate that the stage/materialization's applicable schedule resolution is still current or otherwise explicitly permitted by supersession/reprocess policy.

Therefore:

```text
TIME_DUE emitted != permanent current-time authority
```

This requirement is part of the A-8/A-7/A-9 boundary and must be reflected in future contract tests.

## 6. Local recurrence occurrence identity must include civil-time disambiguation authority

For local-calendar schedules near DST transitions, recurrence occurrence identity cannot be based only on the displayed local timestamp string.

When a local time is ambiguous or transformed by policy, the resolved occurrence must retain enough authority to distinguish the actual selected civil occurrence, including conceptually:

- recurrence definition/version/digest;
- intended local calendar date/time;
- IANA timezone;
- ambiguous/nonexistent-time policy;
- selected UTC offset/fold or transformed-local-time result;
- resolved UTC instant.

Thus two occurrences displaying the same local clock time during fall-back are not silently conflated.

## 7. Physical timer reuse/coalescing is optimization only

Different immutable schedule resolutions may share the same resolved due instant. Runtime infrastructure may optimize them using one wakeup/scan bucket, but canonical identities remain separate unless the architecture explicitly says they are the same semantic occurrence.

Physical timer reuse must never:

- merge different stage materializations;
- merge different plan/scope revisions;
- erase supersession lineage;
- merge shadow and production authority;
- collapse distinct recurrence occurrences;
- bypass A-7 trigger/event identities.

## Certification relationship

These seven clarifications are normative for A-8 certification and must be included in future scheduler/contract test vectors.