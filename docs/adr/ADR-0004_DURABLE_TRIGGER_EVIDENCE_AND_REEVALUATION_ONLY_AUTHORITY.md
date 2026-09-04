# ADR-0004 — Durable Trigger Evidence and Reevaluation-Only Authority

Date: 2026-09-04  
Status: **ACCEPTED**

## Context

The Daily Line Automation must react to timers, sport-state changes, dependency changes, operator requests, external callbacks, and recovery events across many sports.

A naïve event architecture can easily create unsafe behavior:

```text
webhook/timer -> run stage / publish result
```

That design makes source delivery semantics part of execution authority and creates several failure modes:

- duplicate webhook delivery creates duplicate work;
- stale timers revive superseded work;
- corrected/retracted source events rewrite history;
- operator or external callbacks bypass readiness/timing/approval gates;
- a source outage is misread as “nothing changed”;
- crashes between receipt and processing lose causal evidence;
- the orchestration engine/broker becomes the permanent identity authority.

A-0 through A-6 already establish immutable TDLA identity, sport-owned semantics, declarative resolved plans, and separate logical work vs physical attempts. A-7 requires an event model consistent with those guarantees.

## Decision

TDLA adopts a **durable evidence, reevaluation-only trigger architecture**.

The canonical chain is:

```text
TriggerDelivery
    -> TriggerEvent
        -> TriggerBinding
            -> TriggerEvaluation
                -> EligibilityReevaluationRequest
                    -> normal plan/timing/readiness/idempotency/side-effect gates
```

A trigger never directly authorizes dispatch or a side effect.

### Separate delivery from semantic event identity

A physical delivery is not the semantic source occurrence.

Redelivery may create a new `TriggerDelivery` while mapping to the same `TriggerEvent` occurrence/revision.

This preserves transport diagnostics without turning at-least-once delivery into duplicate logical events.

### Durable evidence before irreversible action

Accepted trigger evidence is persisted before it can cause irreversible downstream behavior.

The exact database transaction/outbox design is deferred to A-13, but the architecture requires restart-safe continuation from persisted trigger evidence.

### Trigger deduplication is not stage idempotency

Trigger deduplication suppresses redundant reevaluation.

A-11 stage logical idempotency remains the final duplicate-work defense because multiple distinct legitimate triggers may race to request the same stage reevaluation.

### Corrections/retractions preserve history

Source corrections/retractions are new immutable event revisions/lineage.

They may request reevaluation or later recovery/compensation but never erase the earlier event or completed StageRun evidence.

### Source/sport semantics remain outside generic TDLA

A sport may say “relevant state changed.” TDLA routes that event generically and invokes A-5 readiness when required.

TDLA does not hardcode MLB lineup/pitcher semantics, NFL inactive semantics, or equivalent sport-specific meanings.

### Trigger bindings are immutable resolved-plan authority

Production trigger bindings are versioned/digested and tied to the exact resolved-plan/stage/scope authority they may reevaluate.

A moving runtime subscription or broker rule cannot silently redefine historical plan behavior.

## Alternatives considered

### Alternative 1 — Direct webhook/timer-to-dispatch

Rejected.

It is operationally simple but unsafe under duplicate delivery, stale source state, late events, corrections, and side-effecting workflows.

### Alternative 2 — Let Prefect/broker event IDs be canonical trigger identity

Rejected.

Runtime transport IDs are not durable TDLA semantic identity and may change when infrastructure is replaced.

### Alternative 3 — Deduplicate only at the final StageRun layer

Rejected as the sole defense.

A-11 logical idempotency is still required, but retaining distinct delivery/event identity allows TDLA to avoid unnecessary reevaluations and preserve accurate source behavior diagnostics.

### Alternative 4 — Treat corrected source state as mutable “latest” state only

Rejected.

It destroys auditability and makes it impossible to reconstruct why an earlier production decision happened.

## Consequences

Positive:

- duplicate deliveries become safe and auditable;
- source corrections/retractions preserve causal history;
- triggers remain independent of orchestration/broker technology;
- stale/out-of-order events can be retained without rolling authority backward;
- every triggered action still follows certified plan/readiness/timing/side-effect gates;
- MLB/NFL/NCAAF can expose domain-change signals without moving sport logic into TDLA;
- crash recovery can resume from durable evidence.

Costs:

- more persistence entities and lineage;
- source integrations need explicit identity/revision contracts;
- some event sources cannot be production-authoritative until safe semantic occurrence identity is established;
- burst coalescing requires provenance-aware policies rather than dropping duplicate-looking messages.

## Compatibility / migration impact

No production trigger implementation currently exists, so there is no runtime migration.

Future source integrations must map their transport delivery semantics into:

- `TriggerSourceDescriptor`;
- `TriggerDelivery`;
- `TriggerEvent` identity/revision;
- immutable `TriggerBinding`;
- `TriggerEvaluation`;
- `EligibilityReevaluationRequest`.

Existing sport/manual pipelines remain unchanged until their eventual certified adapters expose trigger-compatible contracts.

## Security / operational impact

- untrusted/invalid external deliveries cannot become authoritative trigger events;
- secret-bearing payloads must be sanitized/rejected without raw secret persistence;
- operator triggers request reevaluation by default; overrides are separate A-19 actions;
- source outages do not become negative domain evidence;
- replay/test ingress remains explicitly labeled and environment-restricted.

## Validation required

A-7 certification must stress at least:

- duplicate timer/webhook delivery;
- conflicting duplicate event identity;
- out-of-order revisions;
- corrections/retractions;
- stale timer after schedule revision;
- process crash after trigger persistence;
- trigger burst/coalescing;
- late trigger after deadline;
- source without stable event ID;
- replay into non-production environment;
- operator trigger without override authority;
- invalid/untrusted/secret-bearing payloads.

## Related architecture

- A-3 run identity / lineage
- A-5 Sport Automation Adapter
- A-6 resolved plan/stage contracts
- A-7 Trigger Architecture
- A-8 event-relative scheduling
- A-9 dependency/readiness
- A-11 retry/idempotency
- A-13 persistence
- A-18 publication
- A-19 operator controls
- A-20 security/service identity

## Supersession

Supersedes: none.  
Superseded by: none.