# A-7 — Trigger Architecture V1

Status: **DOCUMENTED — REVIEW PENDING**  
Repository: `OneVillage83/The-Daily-Line-Automation`  
Architecture section: A-7  
Version: 1.0  
Initial documentation date: 2026-09-04

This document defines the generic durable trigger/event boundary by which The-Daily-Line-Automation (TDLA) learns that one or more resolved plan/stage eligibility states may need reevaluation.

A-7 deliberately does **not** define the final event-relative scheduler algorithm, readiness/dependency state machine, retry/idempotency algorithm, database DDL, publication transport, or operator-override implementation. Those remain owned by A-8, A-9, A-11, A-13, A-18, and A-19 respectively.

The central rule is:

> **A trigger is durable evidence that TDLA should reevaluate eligibility. A trigger does not directly authorize execution, dispatch, publication, destructive action, or any bypass of the certified plan.**

---

# A-7.0 — Governing intent

TDLA must safely accept trigger causes from timers, sport systems, dependencies, operator actions, callbacks, and recovery processes without turning those signals into uncontrolled execution.

The trigger architecture must tolerate:

- duplicate deliveries;
- at-least-once sources;
- out-of-order events;
- corrected/retracted events;
- stale timer fires;
- source clock skew;
- process crashes between receipt and evaluation;
- trigger bursts;
- replay/test ingestion;
- source outages;
- malformed or untrusted payloads;
- multiple independent sources reporting related changes.

A trigger therefore has three separate meanings that must not be collapsed:

1. **delivery evidence** — a transport/source occurrence reached TDLA;
2. **semantic event evidence** — what logical source occurrence/revision that delivery represents;
3. **evaluation cause** — which resolved plan/stage bindings should be reevaluated because of that event.

None of these meanings is equivalent to permission to execute a stage.

---

# A-7.1 — Design invariants

The following are mandatory for certified trigger implementations.

1. **Trigger != authorization.** A trigger can request eligibility reevaluation only.
2. **Durable-before-action.** Accepted trigger evidence is durably recorded before it can cause irreversible downstream action.
3. **Delivery identity != semantic event identity.** Redelivery does not create a new logical source event merely because the transport delivered it again.
4. **Trigger dedup != stage idempotency.** Trigger-level deduplication reduces redundant reevaluations; A-11 logical idempotency remains the final duplicate-work defense.
5. **Source meaning stays source/sport-owned.** TDLA may compare declared opaque values but does not interpret MLB/NFL/NCAAF semantics.
6. **No global ordering assumption.** Source wall clock, network arrival order, and TDLA receipt order are not universal truth ordering.
7. **Corrections/retractions are append-only lineage.** Prior trigger evidence is never silently rewritten or deleted.
8. **Stale evidence cannot revive superseded work.** Old plan/scope/timer revisions fail closed against current binding authority.
9. **Absence of events is not evidence of no change.** Source silence/outage does not become sport truth.
10. **Raw burst evidence remains auditable.** Coalescing may reduce reevaluations but cannot erase accepted trigger lineage.
11. **Replay is explicitly labeled.** Historical replay/test ingestion cannot masquerade as original live receipt.
12. **No direct trigger-to-side-effect path exists.** Every triggered action still passes A-6 plan/stage validation, A-8 timing, A-9 dependency/readiness, execution-mode/certification, immutable target, and side-effect policy checks.
13. **Rejected/untrusted payload handling is safe.** Secrets or unsafe raw payloads are not blindly persisted as trigger data.
14. **Runtime/orchestrator neutrality.** Trigger identity and audit semantics do not depend on Prefect event IDs, queue-message IDs, webhook delivery IDs, or a specific broker.

---

# A-7.2 — Canonical trigger entities

A-7 defines the following canonical concepts.

## A-7.2.1 `TriggerSourceDescriptor`

Describes one logical trigger source implementation/capability profile.

Conceptual fields:

```text
TriggerSourceDescriptor
- source_namespace
- source_kind
- implementation_version
- descriptor_version
- descriptor_digest
- declared_delivery_semantics
- source_event_identity_capability
- source_revision_capability
- ordering/sequence_capability
- replay_capability
- trust_class
- supported_trigger_kinds[]
- safe metadata
```

`source_namespace` is stable logical source identity, not an individual process instance.

Examples of source kinds may include timer engine, sport adapter, internal dependency engine, operator control plane, publication callback adapter, or recovery subsystem.

## A-7.2.2 `TriggerDelivery`

Represents one physical ingress/delivery attempt.

Every accepted or safely rejected ingress attempt receives a TDLA delivery identity where policy permits retention.

Conceptual fields:

```text
TriggerDelivery
- trigger_delivery_id
- source_namespace
- transport_delivery_ref (optional)
- received_at
- persisted_at
- ingress_mode
- authentication/trust result
- schema/validation result
- sanitized payload digest/reference
- resolved trigger_event_ref (optional)
- duplicate-of delivery/event refs (optional)
- delivery disposition
- safe diagnostics
```

A webhook retransmission, queue redelivery, duplicated timer callback, or replay message may create another `TriggerDelivery` while resolving to the same semantic `TriggerEvent`.

## A-7.2.3 `TriggerEvent`

Represents one semantic source occurrence/revision known to TDLA.

Conceptual fields:

```text
TriggerEvent
- trigger_event_id
- source_namespace
- source_event_id / deterministic occurrence identity
- source_event_revision (when supported)
- trigger_kind
- occurred_at / source_effective_at (when known)
- published_at (optional source evidence)
- first_observed_at
- payload_schema_version
- semantic_payload_digest
- generic correlation refs
- scope/plan/stage refs when declared
- source sequence/revision evidence (optional)
- correction/retraction/supersession lineage refs
- event status/disposition
- trace/correlation context
```

A `TriggerEvent` is immutable evidence. If its source later corrects or retracts the occurrence, TDLA records another event/revision linked to the prior evidence.

## A-7.2.4 `TriggerBinding`

Defines an immutable/versioned rule connecting accepted trigger events to eligibility reevaluation targets.

Conceptual fields:

```text
TriggerBinding
- binding_id
- binding_version
- binding_digest
- resolved_plan_id/version/digest
- target StageRef / StageMaterialization selector
- accepted source namespaces[]
- accepted trigger kinds[]
- generic/opaque declared match predicates
- scope-binding rule
- validity/effective interval
- environment/mode restrictions
- debounce/coalescing policy binding
- required trust/source capability constraints
```

A binding may compare opaque values declared by the source/sport fragment, but generic TDLA code cannot hardcode sport meaning. For example, a sport fragment may declare an opaque change category and a binding may compare that value for equality; TDLA still does not know what the category means.

## A-7.2.5 `TriggerEvaluation`

Records how one event/delivery affected one or more bindings.

Conceptual fields:

```text
TriggerEvaluation
- evaluation_id
- trigger_event_ref
- trigger_delivery_refs[]
- binding_ref(s)
- evaluated_at
- resolved_plan/scope/stage revision refs
- evaluation disposition
- reevaluation request refs[]
- coalescing/cause-set ref (optional)
- safe diagnostics
```

Representative dispositions include:

- `NO_MATCH`
- `MATCHED_REEVALUATION_REQUESTED`
- `MATCHED_COALESCED`
- `NO_ACTION_STAGE_TERMINAL`
- `NO_ACTION_STAGE_SUPERSEDED`
- `NO_ACTION_NOT_APPLICABLE`
- `NO_ACTION_STALE_EVENT`
- `NO_ACTION_STALE_BINDING`
- `REJECTED_TRUST`
- `REJECTED_SCHEMA`
- `REJECTED_POLICY`
- `EVALUATION_FAILED_RETRYABLE`
- `EVALUATION_FAILED_TERMINAL`

Exact persistence enums are deferred to implementation, but the semantic distinctions are normative.

## A-7.2.6 `EligibilityReevaluationRequest`

Represents the generic downstream request created by trigger evaluation.

It identifies the plan/stage/materialization context to reevaluate and retains the complete trigger-cause lineage.

It is **not** a dispatch command.

Conceptually:

```text
EligibilityReevaluationRequest
- reevaluation_request_id
- target plan/stage/materialization refs
- trigger cause-set/event refs
- requested_at
- plan/scope revision context
- environment/mode context
- reevaluation reason class
```

A-8/A-9 and later execution gates determine whether anything can actually run.

---

# A-7.3 — Trigger families

V1 supports generic trigger families. Names may become implementation enums later, but semantics are fixed.

## `TIME_DUE`

A due occurrence generated from A-8 scheduling state.

## `SPORT_CHANGE_HINT`

A sport-owned adapter/service reports that relevant domain state may have changed.

TDLA does not interpret whether that means a lineup, pitcher, inactive player, weather impact, injury status, or another sport concept.

## `PLAN_SCOPE_REVISION`

A resolved plan, sport scope, scope-set membership, schedule revision, or other versioned planning authority changed and may require reevaluation/supersession.

## `DEPENDENCY_CHANGE`

An internal dependency/output/terminal-state fact changed in a way that may affect downstream eligibility.

## `READINESS_HINT`

A source suggests readiness may have changed. The authoritative A-5 readiness check still runs when required.

## `OPERATOR_REQUEST`

An authenticated operator requests reevaluation or another non-bypass action. Overrides remain separate A-19 actions.

## `EXTERNAL_CALLBACK`

A typed external callback/receipt may advance a follow-up stage. Publication-specific semantics remain A-18-owned.

## `RECOVERY_RECONCILIATION`

TDLA recovery/reconciliation discovers state that warrants reevaluation after restart, worker loss, or child reconciliation.

## `SYSTEM_CONFIGURATION_CHANGE`

A versioned, authorized system/configuration change may require reevaluation of future pending work when its governing plan/policy declares such behavior.

No trigger family gives direct execution authority.

---

# A-7.4 — Source identity, event identity, and delivery identity

## A-7.4.1 Stable semantic identity

When the source supplies a stable semantic event ID, TDLA uses the source namespace plus stable source event identity and declared revision semantics to resolve duplicate deliveries.

Conceptually:

```text
semantic occurrence key =
  source_namespace
  + source_event_id
  + semantic revision identity when the source defines revisions
```

A transport delivery ID alone is not sufficient because it may change on redelivery.

## A-7.4.2 Sources without stable event IDs

If a source cannot supply a stable semantic event ID, the integration may use a **certified deterministic ingress identity strategy** only when it can prove that the strategy will not dangerously collapse distinct occurrences or create uncontrolled duplicates.

Such a strategy must be versioned and documented per source. It may use stable source-owned semantic fields and canonical payload material, but it must not rely casually on arrival-time bucketing or arbitrary transport metadata.

If safe deterministic occurrence identity cannot be established, the source cannot be used as a high-authority production event-driven trigger for side-effect-capable paths. It may be:

- advisory only;
- combined with polling/readiness/timer fallback;
- or rejected for that use case.

This does not require inventing fake event IDs.

## A-7.4.3 Duplicate delivery retention

Duplicate delivery evidence is retained even when it maps to an existing semantic event.

This allows later operational questions such as:

- how many times did the provider redeliver?
- did a queue retry storm occur?
- was duplicate evaluation successfully suppressed?

---

# A-7.5 — Event revisions, ordering, correction, and retraction

## A-7.5.1 No global ordering

TDLA must never assume that:

```text
larger received_at == newer domain truth
```

or that:

```text
larger source occurred_at == authoritative revision ordering
```

unless the source contract explicitly guarantees those semantics.

Clock skew and network delay are expected.

## A-7.5.2 Preferred ordering evidence

Where available, TDLA retains and uses source-declared:

- monotonic sequence numbers;
- event revisions;
- version IDs;
- scope/schedule revisions;
- explicit supersedes/corrects/retracts references.

Source timestamps remain evidence but are not automatically universal ordering keys.

## A-7.5.3 Stale revisions

An older known revision arriving after a newer revision remains auditable but cannot silently replace the newer known revision.

Its evaluation may resolve to `NO_ACTION_STALE_EVENT` unless the binding/policy has an explicit historical/reconciliation use for it.

## A-7.5.4 Corrections

A correction is recorded as a new semantic event/revision linked through `corrects_event_ref` or equivalent lineage.

The original event remains immutable evidence.

The correction may request eligibility reevaluation/supersession; it does not rewrite already-recorded StageRun history.

## A-7.5.5 Retractions

A retraction is also a new semantic event/revision with explicit lineage.

If prior trigger-driven work has already executed, retraction cannot pretend it never happened. Recovery, compensation, reprocess, or publication correction behavior must follow later explicit policies.

---

# A-7.6 — Time-trigger boundary with A-8

A-7 does not calculate event-relative timestamps.

A-8 owns:

- schedule-slot resolution;
- event-relative due-time calculation;
- recalculation after event/scope revision;
- missed-window determination;
- timer occurrence generation policy.

A-7 owns the durable representation and processing of the resulting `TIME_DUE` occurrence.

## A-7.6.1 Timer occurrence identity

A timer occurrence must be tied to the stable A-6 schedule slot/materialization plus the schedule/scope/due-time revision that produced it.

A duplicate fire of the same timer occurrence resolves to duplicate delivery/event evidence, not a new logical stage.

## A-7.6.2 Stale timers

When A-8 supersedes an old due occurrence after a game/kickoff/reschedule revision, a late callback from the old timer remains evidence but cannot revive the superseded stage/timing authority.

The trigger evaluation records the stale/superseded relationship and stops before execution authorization.

---

# A-7.7 — Sport-trigger boundary with A-5

A sport adapter may emit a generic `SPORT_CHANGE_HINT`, `PLAN_SCOPE_REVISION`, or `READINESS_HINT` carrying sport-owned references and opaque change metadata.

Examples conceptually include:

```text
sport says: relevant pregame state changed
TDLA: record trigger -> match binding -> request reevaluation
A-5 readiness: READY / WAITING / BLOCKED / NOT_APPLICABLE
```

TDLA must not contain generic code such as:

```text
if sport == MLB and change == LINEUP_POSTED: dispatch()
```

or:

```text
if sport == NFL and INACTIVES_FINAL: publish()
```

The sport system owns the meaning; TDLA owns only generic routing and reevaluation.

---

# A-7.8 — TriggerBinding / subscription architecture

## A-7.8.1 Immutable binding authority

Production trigger bindings are immutable/versioned/digested and tied to exact resolved-plan authority.

A moving alias such as `current-trigger-rules` may be resolved during plan resolution but must not silently change a production plan that already exists.

## A-7.8.2 Matching dimensions

Bindings may match on generic fields such as:

- source namespace;
- trigger family/kind;
- exact resolved plan/stage identity;
- A-5 sport scope references/revisions;
- declared generic correlation keys;
- opaque equality/set membership selectors supplied declaratively by a plan fragment;
- environment/mode;
- validity interval.

Bindings must not rely on hidden sport interpretation.

## A-7.8.3 Multiple matches

One event may legitimately match multiple bindings.

Each resulting reevaluation target is deterministic and independently auditable.

TDLA does not collapse them merely because they came from one event.

## A-7.8.4 No match

A valid accepted event matching no active binding is not a system failure. `NO_MATCH` is a valid evaluation result.

---

# A-7.9 — Durable ingestion pipeline

The required logical sequence is:

```text
receive delivery
    -> authenticate / trust-check / sanitize
        -> validate envelope/schema
            -> durably record TriggerDelivery
                -> resolve/create immutable TriggerEvent evidence
                    -> match immutable TriggerBinding(s)
                        -> record TriggerEvaluation
                            -> create EligibilityReevaluationRequest(s)
                                -> later eligibility engine decides what may run
```

The exact PostgreSQL transaction/outbox/locking implementation is deferred to A-13.

The architectural guarantee is that a crash must not leave TDLA in a state where an irreversible action occurred with no durable trigger/cause evidence.

After restart, persisted accepted trigger evidence whose evaluation was incomplete can be safely resumed/reprocessed.

---

# A-7.10 — Duplicate handling and defense-in-depth

A-7 trigger deduplication and A-11 stage idempotency solve different problems.

## Trigger deduplication

Prevents or reduces redundant reevaluation caused by repeated delivery of the same semantic source occurrence.

## Stage logical idempotency

Prevents duplicate logical sport work/side effects even if multiple distinct trigger events or trigger evaluations legitimately request reevaluation concurrently.

Therefore:

```text
duplicate trigger suppression PASS
```

is never used as proof that duplicate dispatch is impossible.

The A-11 logical idempotency key remains mandatory.

---

# A-7.11 — Trigger cause sets and burst coalescing

High-frequency events can produce repeated reevaluation requests for the same target.

A-7 permits a versioned generic debounce/coalescing policy that creates a `TriggerCauseSet` or equivalent object referencing all contributing immutable events.

Conceptually:

```text
TriggerCauseSet
- cause_set_id
- target binding/stage context
- event refs[]
- first/last observed time
- coalescing policy id/version/digest
- created_at
```

Coalescing may reduce reevaluation work, but:

- every raw accepted `TriggerDelivery` remains retained;
- every semantic `TriggerEvent` remains retained;
- the cause set references all contributing events;
- no event disappears from provenance;
- cross-source events are not silently deduplicated into one semantic event.

Two independent sources reporting the same real-world change remain distinct semantic source evidence unless an explicit higher-level correlation/coalescing policy links them.

---

# A-7.12 — Late triggers and timing boundaries

A trigger arriving after a stage deadline or validity window remains valid evidence if otherwise authentic/valid.

It does not grant permission to run late.

The reevaluation path must check:

- exact A-6 plan/stage/timing declaration;
- current scope/schedule revision;
- A-8 missed-window/deadline state;
- A-9 dependency/readiness state;
- execution mode/certification;
- immutable target/policies;
- side-effect authority.

A late legitimate update may therefore end with `NO_ACTION` while still being preserved for audit/research.

---

# A-7.13 — Operator/manual triggers

An authoritative operator trigger must retain:

- authenticated operator/service identity;
- requested action class;
- reason/comment where policy requires it;
- environment;
- target plan/stage/materialization;
- requested_at;
- trace/correlation context.

By default, an operator trigger requests reevaluation only.

An explicit operator override that bypasses a normal gate, if allowed at all, is a distinct A-19 control-plane action with separate authorization and audit semantics. It must not be smuggled through an ordinary trigger payload.

---

# A-7.14 — External callbacks and receipts

A typed external callback may be accepted as a trigger cause for follow-up work.

Examples include publication/delivery acknowledgement, external processing completion, or future third-party receipts.

The callback:

- has its own source/delivery/event identity;
- is schema/version validated;
- can be redelivered safely;
- remains evidence rather than direct authorization;
- must still match an immutable binding;
- preserves domain ownership of callback semantics under the relevant architecture (for example A-18 publication).

---

# A-7.15 — Recovery/reconciliation triggers

After restart or reconciliation, TDLA may create internal `RECOVERY_RECONCILIATION` trigger events when newly reconciled state means eligibility should be reevaluated.

Examples:

- an async sport child is discovered completed after TDLA restart;
- a dependency state is reconstructed;
- a persisted trigger was never evaluated;
- a previously unknown child state becomes known.

Recovery triggers remain ordinary durable causes and do not bypass normal gates.

---

# A-7.16 — Replay, backfill, and test ingestion

A trigger delivery identifies an ingress mode, at minimum conceptually:

- `LIVE`
- `REPLAY`
- `BACKFILL_TEST`
- `SHADOW_TEST`

A replayed event retains:

- original source occurrence/effective time when known;
- original semantic source event identity/revision;
- actual replay delivery/ingestion time;
- replay session/reason/reference;
- target environment/mode restrictions.

Trigger replay is not StageRun replay/reprocess. Trigger replay re-exercises trigger/eligibility behavior; StageRun replay/reprocess has separate A-3/A-14 lineage.

Historical replay into staging/shadow must not accidentally match a production-authorized side-effect binding.

---

# A-7.17 — Source outage and negative evidence

A trigger source becoming silent, unhealthy, or unavailable is operational evidence only.

TDLA must not infer:

```text
no events arrived -> no relevant sport state changed
```

Plans may use independent fallback mechanisms such as:

- timer-driven reevaluation;
- adapter readiness polling;
- reconciliation;
- other certified sources.

The fallback strategy is declared by later scheduling/readiness/failure policy architecture. Source-health alerting/incidents remain A-17.

---

# A-7.18 — Security and payload hygiene boundary

A-7 defines security requirements while A-20 owns concrete auth/service-identity implementation.

Required properties:

- trust/auth result is evaluated before authoritative event acceptance;
- external sources must use authenticated/verifiable delivery mechanisms appropriate to their trust class;
- invalid signature/untrusted delivery fails closed for authoritative use;
- raw credentials/tokens/passwords/private keys must not become trigger payload data;
- rejected payloads are retained only in sanitized diagnostic form according to policy;
- trigger payload schemas explicitly identify persistable fields;
- diagnostic serialization must not leak auth headers or secret query parameters;
- replay/test ingress cannot reuse production credentials/authority implicitly.

---

# A-7.19 — Trigger payload contracts and canonical digests

Accepted semantic trigger payloads are schema/version controlled.

Their semantic digest must use deterministic canonicalization rules consistent with A-6 principles:

- semantically unordered collections normalized deterministically;
- meaningful order preserved only when declared by schema;
- normalized timestamps encoded unambiguously;
- presentation/transport-only metadata excluded only when the schema explicitly classifies it as non-semantic;
- unknown critical fields fail closed according to schema-version rules.

A transport wrapper/header change alone must not change semantic event identity when it does not change source meaning.

---

# A-7.20 — Evaluation against current authority

Trigger evaluation never acts against stale assumptions merely because the event originally matched them.

Before requesting downstream reevaluation, TDLA checks or binds current authoritative references such as:

- resolved plan digest;
- StageRef / StageMaterialization revision;
- A-5 SportScopeRef/scope revision;
- A-6 ScopeSetBinding revision when relevant;
- TriggerBinding digest/validity;
- environment/mode.

If the referenced work is already terminal, superseded, or `NOT_APPLICABLE`, the evaluation records that result rather than resurrecting work.

---

# A-7.21 — No direct trigger-to-side-effect path

The prohibited architecture is:

```text
webhook/timer
    -> run model / publish / delete / mutate external system
```

The required architecture is:

```text
TriggerDelivery
    -> TriggerEvent
        -> TriggerBinding
            -> TriggerEvaluation
                -> EligibilityReevaluationRequest
                    -> A-8 timing validity
                    -> A-9 dependency/readiness eligibility
                    -> A-6 resolved stage / immutable target / policy validation
                    -> A-11 idempotent execution authority
                    -> A-5 adapter execution when sport-owned
                    -> A-18/A-19 side-effect or approval gates when applicable
```

No source, including an operator or publication callback, bypasses this chain by default.

---

# A-7.22 — Failure handling boundary

A-7 distinguishes trigger ingestion/evaluation failures from sport-stage failures.

Examples:

- malformed trigger envelope;
- trust verification failure;
- payload-schema mismatch;
- event-identity conflict;
- unknown incompatible source descriptor;
- trigger-binding mismatch/corruption;
- transient persistence/evaluation failure.

Exact retry/terminal-failure policy belongs to A-11/A-12, but every failure must preserve safe diagnostic evidence and must not authorize downstream work from an uncertain trigger state.

---

# A-7.23 — A-7 validation requirements

Before a trigger binding/source can be used for authoritative production reevaluation, validation must prove at minimum:

- source descriptor/version is supported;
- trust class and auth capability meet environment policy;
- semantic event identity/dedup strategy is defined;
- payload schema/version is supported;
- trigger binding exists and is immutable/versioned;
- plan/stage/scope refs are valid;
- coalescing/debounce policy is immutable when execution-affecting;
- replay/test restrictions are explicit;
- no direct side-effect path exists;
- crash recovery can resume from durably persisted trigger evidence;
- duplicate deliveries cannot create duplicate logical work when combined with A-11 guarantees.

---

# A-7.24 — Explicit non-goals / deferred architecture

A-7 does not define:

- A-8 exact event-relative timer calculation/recalculation algorithm;
- A-9 final dependency/readiness state transitions;
- A-10 queue/broker/worker/executor technology;
- A-11 exact trigger-processing retry or stage logical-idempotency keys;
- A-12 incident-specific recovery/compensation policy;
- A-13 table/constraint/transaction/outbox DDL;
- A-15 trigger-ingress resource/concurrency budgets;
- A-16 metrics/traces implementation;
- A-17 alerting/incident routing;
- A-18 publication callback semantics;
- A-19 override authorization semantics;
- A-20 signatures, credentials, service identity implementation.

These are intentional deferrals, not missing A-7 requirements.

---

# A-7.25 — Certification invariants

A-7 cannot be certified unless the following remain true:

1. trigger delivery and semantic event identity are separate;
2. semantic event and execution authorization are separate;
3. accepted evidence is durable before irreversible action;
4. duplicate delivery is auditable and does not imply duplicate event/work;
5. stable source identity or a certified deterministic occurrence strategy exists for authoritative event-driven use;
6. corrections/retractions preserve append-only lineage;
7. out-of-order evidence cannot silently roll authoritative revision backward;
8. timer events bind exact schedule/materialization revisions;
9. stale timers cannot revive superseded work;
10. sport-change events remain opaque hints to generic TDLA;
11. A-5 readiness remains authoritative where the plan requires readiness;
12. trigger bindings are immutable/versioned and plan-bound;
13. multiple matches are deterministic/auditable;
14. no-match is valid;
15. burst coalescing retains every source event in provenance;
16. trigger dedup and A-11 stage idempotency remain separate defenses;
17. late triggers cannot bypass timing/deadline rules;
18. operator triggers cannot silently become overrides;
19. replay/test ingress is explicitly labeled and environment-restricted;
20. source silence cannot be interpreted as domain no-change truth;
21. untrusted/malformed/secret-bearing payloads fail closed safely;
22. every trigger-derived execution still traverses certified plan/eligibility/idempotency/side-effect gates.

---

# A-7.26 — Certification stress cases

The certification review must test at minimum:

1. same timer occurrence delivered twice;
2. same webhook delivered multiple times with one stable source event ID;
3. source has no stable event ID and no safe deterministic occurrence identity;
4. older schedule/scope revision arrives after newer revision;
5. source sends a corrected event revision;
6. source retracts an earlier event;
7. MLB generic pregame-change event causes readiness reevaluation without MLB semantics in TDLA;
8. NFL/NCAAF generic pregame-change event does the same;
9. readiness hint arrives but A-5 still says `WAITING`;
10. trigger arrives after stage deadline;
11. dependency completion event is delivered twice;
12. trigger targets already-`SUCCEEDED` stage;
13. trigger targets superseded old plan/stage revision;
14. trigger targets `NOT_APPLICABLE` stage;
15. no-games/empty-scope revision creates no fake event work;
16. burst of 100 relevant events is coalesced with complete provenance;
17. crash after trigger persistence before evaluation;
18. crash after evaluation before/around dispatch;
19. two source namespaces report related change and are not silently deduplicated;
20. source clock skew makes `occurred_at` later than `received_at`;
21. trigger payload digest/schema mismatch;
22. unauthenticated/invalid-signature external trigger;
23. trigger payload contains secret-like credential material;
24. authenticated operator reevaluation cannot bypass ordinary gates;
25. future explicit A-19 override remains separate from ordinary trigger event;
26. publication callback/receipt is redelivered;
27. event-time move creates new timer occurrence while stale old timer later fires;
28. trigger source is down for hours;
29. historical trigger replay into staging retains original + replay time and cannot reach production side effects;
30. valid trigger matches no binding;
31. one trigger matches multiple declared bindings deterministically;
32. same semantic payload arrives with different transport headers/delivery IDs and remains one semantic event;
33. correction arrives after prior work already completed;
34. coalescing window closes, then a genuinely new semantic event arrives and causes a new reevaluation request;
35. binding has expired while source event is still valid;
36. event references a scope revision that no longer matches the current resolved plan;
37. replayed event is accidentally delivered to production ingress and is rejected/restricted by mode policy;
38. recovery finds an unevaluated persisted trigger and resumes without requiring source redelivery;
39. source sequence number regresses/repeats unexpectedly;
40. trigger trust/source descriptor version is incompatible with the production binding.

---

# A-7.27 — Implementation implications

Later M1/M4 implementation should eventually provide typed/versioned contracts corresponding to:

- `TriggerSourceDescriptor`;
- `TriggerDelivery`;
- `TriggerEvent`;
- `TriggerBinding`;
- `TriggerEvaluation`;
- `EligibilityReevaluationRequest`;
- `TriggerCauseSet` / coalescing lineage.

Later implementation must include deterministic contract test vectors for:

- event identity resolution;
- payload canonical digest;
- duplicate delivery resolution;
- correction/retraction lineage;
- stale revision handling;
- binding matching;
- replay labeling;
- burst cause-set provenance.

No implementation should invent database fields or queue semantics that contradict this architecture.

---

# A-7.28 — Relationship to the broader architecture

```text
A-5 sport/service source
A-8 timer/scheduler source
A-9 dependency/readiness source
A-18 callback source
A-19 operator source
          |
          v
      A-7 TriggerDelivery
          |
          v
      A-7 TriggerEvent
          |
          v
      A-7 TriggerBinding
          |
          v
      A-7 TriggerEvaluation
          |
          v
EligibilityReevaluationRequest
          |
          +--> A-8 timing validity
          +--> A-9 dependency/readiness
          +--> A-6 resolved plan/stage authority
          +--> A-11 logical idempotency/retry
          +--> A-5 sport adapter execution
          +--> A-18/A-19 side-effect gates
```

This preserves one durable trigger architecture across MLB, NFL, NCAAF, and future sports without making TDLA understand sport-specific trigger meaning.