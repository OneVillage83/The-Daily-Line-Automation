# ADR-0005 — Stable Schedule Slots, Resolved Time Authority, and Reevaluation-Only Due Events

Date: 2026-09-04  
Status: **ACCEPTED**

## Context

The Daily Line needs event-relative scheduling across MLB, NFL, NCAAF, and future sports. Real event times change frequently: games are delayed, flexed, postponed, cancelled, split into separate scopes, or initially announced without a reliable start time.

A naive scheduler often makes the resolved wall-clock timestamp or scheduler-vendor job ID the identity of the work. That creates several production hazards:

- moving a game time can create duplicate logical snapshots;
- stale timers can revive obsolete work;
- scheduler restarts can recreate already-emitted due work;
- multiple scheduler replicas can race into duplicate callbacks;
- due callbacks can bypass readiness/dependency/side-effect gates;
- historical evidence becomes difficult to reconstruct because old schedule authority is overwritten;
- cron/Prefect/APScheduler identity leaks into permanent business semantics.

A-6 already established stable `ScheduleSlotRef` identity independent of wall-clock timestamp. A-7 established that triggers request eligibility reevaluation only. A-8 must connect these decisions into a durable scheduling model.

## Decision

TDLA scheduling uses the following authority hierarchy:

```text
stable ScheduleSlotRef
    + immutable TimingDeclaration
    + exact ScheduleAnchorRef/value/revision
    + exact resolved-plan/scope/policy authority
        -> immutable ScheduleResolution
            -> logical ScheduleOccurrence
                -> one canonical semantic A-7 TIME_DUE event
                    -> eligibility reevaluation only
```

### Stable slot identity

The logical schedule slot is the semantic scheduling intent. A resolved timestamp is one resolution of that intent under exact current authority.

Rescheduling creates a new immutable `ScheduleResolution`; it does not mutate the old resolution or rename the slot.

### Exact time authority

Every production event-relative resolution binds the exact sport-owned scope/schedule revision and anchor value used. TDLA does not infer sport event continuity from names, dates, teams, or provider IDs.

### Durable occurrence identity

Physical scheduler callbacks, scans, delayed messages, leases, or runtime worker IDs are not canonical occurrence identity.

Multiple physical scheduler attempts may correspond to one logical `ScheduleOccurrence`.

### Reevaluation-only due event

A due occurrence causes one canonical semantic A-7 `TIME_DUE` event for that exact occurrence authority. That event requests eligibility reevaluation; it never directly executes sport work.

A-9 readiness/dependency/current-authority checks and later A-11 execution idempotency still apply.

### Supersession instead of mutation

When event/scope/plan timing authority changes:

- pending old resolutions/occurrences are superseded;
- historical evidence remains immutable;
- new current authority is resolved separately;
- stale old callbacks/events remain audit evidence but cannot silently regain current execution authority.

### Missed-window behavior is explicit

A missed target does not imply catch-up execution. Each production timing declaration binds an immutable missed-window policy that can skip, request reevaluation within grace, request immediate reevaluation, supersede with no action, or require operator review.

The scheduler itself never directly executes work.

### Technology neutrality

Prefect schedule IDs, APScheduler job IDs, CronJob UIDs, delayed-message IDs, and OS cron entries are runtime cross-references only.

Replacing the scheduling engine must preserve TDLA slot/resolution/occurrence/supersession identities and A-7 causal linkage.

## Alternatives considered

### Alternative 1 — Wall-clock timestamp is schedule identity

Rejected.

A game-time change would make a stable logical snapshot appear to be a different workflow concept and would make duplicate/supersession reasoning fragile.

### Alternative 2 — Mutate existing timer rows/jobs when event time changes

Rejected as canonical behavior.

Runtime timer objects may be updated or reused for efficiency, but TDLA authority must retain immutable old/new schedule resolutions and supersession lineage.

### Alternative 3 — Scheduler callback directly dispatches the stage

Rejected.

This would bypass A-7 durable trigger evidence, A-9 readiness/dependencies/current-authority validation, and A-11 final logical idempotency.

### Alternative 4 — Singleton scheduler guarantees correctness

Rejected.

HA/restart correctness must survive duplicate physical observation of one due occurrence.

### Alternative 5 — Make Prefect schedule/deployment identity canonical

Rejected.

This violates ADR-0001 and would couple historical scheduling identity to a replaceable runtime.

## Consequences

### Positive

- reschedules are reproducible and auditable;
- stable snapshot intent survives clock-time changes;
- stale timers cannot silently revive obsolete authority;
- multiple scheduler replicas are safe at the semantic level;
- scheduler replacement remains possible;
- due events cannot bypass downstream safety gates;
- historical prediction timing can be reconstructed precisely;
- missed/late customer-visible behavior is explicit rather than accidental.

### Costs

- more persisted authority objects and lineage;
- scheduler recovery requires reconciliation rather than simple in-memory timers;
- A-13 needs careful unique constraints/outbox/transaction design;
- plan/scope revisions can create more schedule-resolution history even when the UTC time is unchanged;
- DST/local calendar recurrence requires explicit disambiguation contracts.

These costs are accepted because production correctness and reproducibility outweigh implementation simplicity.

## Compatibility / migration impact

No production scheduler exists yet, so no runtime migration is required now.

Future implementation must map any Prefect/APScheduler/queue timer identity onto TDLA canonical schedule-resolution/occurrence identities rather than adopting vendor IDs as authority.

Future Daily-MLB/NFL/NCAAF integrations supply sport-owned event/schedule authority through A-5; they do not need to expose their internal scheduling implementation.

## Validation required

A-8 certification and future implementation tests must prove at least:

- slot identity remains stable across event-time moves;
- old resolutions remain immutable/superseded;
- repeated physical callbacks map to one logical occurrence;
- one logical occurrence maps to one canonical semantic A-7 `TIME_DUE` event;
- crash windows reconcile rather than duplicate events;
- earlier reschedules classify missed slots deterministically;
- stale emitted old timer authority is rejected after supersession;
- local DST ambiguity is handled explicitly;
- scheduler runtime replacement does not alter canonical identity.

## Related architecture

- A-3 Run identity / lifecycle
- A-5 Sport Automation Adapter
- A-6 Pipeline Plan / Stage Contracts
- A-7 Trigger Architecture
- A-8 Event-Relative Scheduling Engine
- future A-9 Dependency / Readiness
- future A-11 Retry / Timeout / Idempotency
- future A-13 Persistence / Audit / Provenance
- ADR-0001 Control Plane / Vendor-Neutral Identity
- ADR-0003 Immutable Plan Fragments / Resolved Plan Authority
- ADR-0004 Durable Trigger Evidence / Reevaluation-Only Authority