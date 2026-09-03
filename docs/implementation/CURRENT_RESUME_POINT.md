# The Daily Line Automation — Current Resume Point

Last updated: 2026-09-03 (America/Los_Angeles)  
Authority: This file is the single exact continuation point for unfinished TDLA work. It does not override architecture/certification authority; it tells the next session where to resume.

## Current project state

- Repository constitution/documentation-memory policy is authoritative in `AGENTS.md`.
- A-0 through A-4 Foundation V1 + V1.1 nested-lifecycle addendum are **ARCHITECTURE-CERTIFIED**.
- A-5 Sport Automation Adapter V1 + V1.1 certification addendum are **ARCHITECTURE-CERTIFIED**.
- A-6 Pipeline Plan / Stage Contracts V1 + V1.1 certification addendum are **ARCHITECTURE-CERTIFIED**.
- A-6 review evidence: `docs/implementation/A06_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md`.
- ADR-0001 establishes TDLA canonical automation identity and a replaceable orchestration runtime.
- ADR-0002 establishes the Sport Automation Adapter as a transport-neutral protocol boundary.
- ADR-0003 establishes immutable separately owned plan fragments, explicit typed composition, and `ResolvedAutomationPlan` as executable plan authority.
- No production implementation milestone is certified.
- No TDLA automation is production-authoritative.
- Daily-MLB remains manual-first; later automation must prove equivalence after its final manual production pipeline is certified.

## Certified nested architecture through A-6

```text
sport-owned scope/discovery/plan fragment
        +
TDLA generic platform fragment(s)
        |
        v
explicit PlanAssembly + typed port bindings
        |
        v
immutable ResolvedAutomationPlan
        |
        v
StageDefinition / StageMaterialization
        |
        v
TDLA StageRun / RunAttempt
        |
        v
versioned Sport Automation Adapter
        |
        v
sport child job/service operation
        |
        v
DDC acquisition run(s) where used
        |
        v
provider evidence/attempts
```

## Important locked A-5 rules

1. TDLA never copies sport readiness/model/settlement logic into generic orchestration code.
2. Adapter integration is transport-neutral; HTTP, CLI/container, queue, RPC, etc. are implementation choices under A-10.
3. Sport scope identity/revision remains sport-owned and opaque to TDLA except for neutral orchestration metadata.
4. Adapter protocol/capability incompatibility fails closed.
5. Capability support does not equal production authorization.
6. Physical retry `attempt_id` is not child deduplication identity.
7. The logical idempotency identity remains stable across retries of the same logical operation.
8. Async production integration must reconcile by child ref and by logical idempotency/equivalent durable handle for the lost-acknowledgement case.
9. Unknown child state is not permission to duplicate dispatch.
10. Shadow mode must disable uncontrolled production-visible side effects.
11. Supervised mode must preserve an explicit production side-effect/operator gate.
12. Sport semantic success does not automatically equal TDLA stage success; declared generic result/artifact requirements must also validate.
13. Terminal result/artifact evidence is immutable/versioned.
14. Settlement/evaluation use the same generic invocation boundary while remaining sport-owned in meaning.

## Important locked A-6 rules

1. V1 executable plans are declarative directed acyclic graphs (DAGs).
2. The executable authority is an immutable `ResolvedAutomationPlan`, not a Prefect flow/runtime object.
3. Sport and TDLA platform stages live in separately owned immutable `PlanFragment` objects.
4. `PlanAssembly` uses explicit typed cross-fragment port bindings; there is no stage-name/filename guessing and no `TDLA wins`/`sport wins`/`last writer wins` precedence.
5. Duplicate/conflicting stage definitions or incompatible ports fail closed.
6. `StageRef` is namespaced + versioned. Stage meaning remains opaque to generic TDLA.
7. `StageDefinition`, `StageMaterialization`, logical StageRun, and physical RunAttempt are distinct identity layers.
8. Dynamic fan-out child membership originates from sport-owned A-5 scope refs. `ScopeSetBinding` is only a neutral exact membership/revision/digest container.
9. Fan-in binds to the exact expansion membership revision/digest; TDLA never parses sport IDs to guess a slate's games.
10. Zero-member fan-out can be a valid declared empty/no-op/not-applicable result.
11. Repeated snapshots use stable logical `ScheduleSlotRef` identities; resolved clock timestamps are not snapshot identity.
12. A readiness change from `WAITING` to `READY` does not create a duplicate logical stage materialization.
13. `OPTIONAL` does not mean downstream ignores a stage; explicit edge/input contracts determine dependency satisfaction.
14. `NOT_APPLICABLE` is retained as a plan-resolution/materialization disposition and does not masquerade as failure/cancellation.
15. `NO_OP` can be successful only when the stage contract allows it and cannot satisfy an output dependency for an output it did not produce.
16. `SUCCEEDED_DEGRADED` satisfies only validated outputs/dependencies permitted by the declared failure/degradation policy.
17. Production resolved stages use immutable execution targets; mutable branches/`latest` tags fail closed.
18. Production resolved plans pin immutable versions/digests for execution-affecting policies; mutable aliases may be used only during resolution.
19. Side-effect classes are explicit (`NONE`, `INTERNAL_EVIDENCE`, `EXTERNAL_OPERATIONAL`, `CUSTOMER_VISIBLE`, `DESTRUCTIVE_EXTERNAL`) and must be compatible with shadow/supervised/production mode.
20. Shadow cannot hide a customer-visible/destructive effect inside a compute/internal stage.
21. Semantic plan identity uses schema-controlled canonical normalization + SHA-256. Presentation-only/audit metadata is excluded only when the versioned schema explicitly classifies it that way.
22. Plan/scope/membership revisions create new authority; completed evidence remains attached to the exact old plan/stage/scope/target/policy digests.
23. A-6 defines timing/readiness/policy declarations but intentionally defers trigger/scheduler/readiness/retry/failure/database algorithms to later architecture sections.

## Daily-MLB compatibility note that must not be forgotten

The current Daily-MLB starter service shape is useful but is **not** the automation target authority.

Future M13 work must target the **certified final manual MLB pipeline** and wrap/expose it through A-5/A-6 contracts.

The eventual MLB integration must prove at minimum:

- caller-stable idempotent async dispatch/reconciliation from A-5;
- sport-owned event/slate/schedule references;
- sport-owned stage meaning/readiness;
- stable A-6 logical input/output/manifests rather than TDLA filename guessing;
- immutable release/target binding;
- explicit side-effect separation for shadow/supervised/production;
- exact plan/stage/scope/policy/target provenance.

Do not restructure current MLB internals merely to resemble A-6 before the manual pipeline architecture is certified. An adapter/wrapper may expose the certified contract later.

## Exact next step — A-7 Trigger Architecture

Design the generic durable trigger/event boundary by which TDLA learns that one or more plan/stage eligibility states may need reevaluation.

The critical A-7 rule should be:

> **A trigger is evidence that TDLA should reevaluate eligibility. A trigger does not directly grant permission to dispatch, bypass dependencies/readiness, override timing/deadlines, or bypass side-effect/authorization policy.**

### A-7 must define at minimum

1. **Trigger source identity / capability**
   - stable source namespace;
   - source/adapter implementation version;
   - source kind;
   - delivery guarantees declared (`at-least-once`, etc.);
   - ordering/sequence capability;
   - replay capability;
   - trust/authentication class declaration while deferring implementation to A-20.

2. **Semantic TriggerEvent identity**
   - TDLA trigger-event ID;
   - source namespace;
   - stable source event/occurrence ID where available;
   - source event revision/version;
   - trigger kind;
   - scope/plan/stage references or generic correlation references when applicable;
   - `occurred_at` / source effective time when known;
   - `observed_at` / `received_at` TDLA time;
   - payload contract/version/digest;
   - correlation/trace context;
   - correction/retraction/supersession lineage.

3. **Delivery identity vs event identity**
   - every transport delivery can have its own `TriggerDelivery` record;
   - redelivery of the same semantic source event must not become a new logical event merely because the message/webhook was delivered twice;
   - duplicate delivery evidence is retained;
   - corrected/revised events are new revisions linked to the earlier event, not silent mutation.

4. **Trigger families**
   Define generic categories without sport meaning, likely including:
   - time-due/timer occurrence;
   - sport-adapter event/change notification;
   - plan/scope revision notification;
   - dependency-state change;
   - readiness-change hint;
   - operator/manual request;
   - external system callback/receipt;
   - system recovery/reconciliation event.

   Exact names may change during A-7 review, but categories must remain generic.

5. **Time-trigger boundary with A-8**
   - A-8 calculates/recalculates event-relative due times and schedule occurrences;
   - A-7 represents the resulting due occurrence as a durable trigger/evaluation cause;
   - a duplicate timer fire must not create duplicate logical sport work;
   - a stale timer after an event-time revision cannot silently revive superseded work.

6. **Sport-trigger boundary with A-5**
   - MLB/NFL/NCAAF/provider meaning remains inside the sport system;
   - a sport event such as "relevant pregame state changed" may request reevaluation;
   - TDLA must not hardcode `LINEUP_POSTED`, `INACTIVES_FINAL`, pitcher names, etc. as generic decision logic;
   - if readiness matters, TDLA still consumes the A-5 readiness contract before dispatch.

7. **TriggerSubscription / TriggerBinding contract**
   - immutable/versioned binding identity;
   - which resolved plan/stage/materialization can be reevaluated;
   - accepted trigger source/kind;
   - generic matching/filter fields only;
   - scope binding rules;
   - debounce/coalescing policy reference;
   - validity/effective interval;
   - environment/execution-mode restrictions.

8. **Durable ingestion before action**
   - accepted trigger evidence must be durably recorded before it can cause irreversible dispatch/side effects;
   - exact PostgreSQL DDL/transaction mechanics remain A-13;
   - after restart, unprocessed/partially processed trigger evidence can be safely reevaluated.

9. **Trigger evaluation record**
   Define an auditable result such as:
   - accepted/rejected delivery;
   - duplicate delivery;
   - no matching subscription;
   - stale/superseded event;
   - matched bindings;
   - eligibility reevaluation requested;
   - no action because stage already terminal/superseded/not applicable;
   - failure/diagnostic state.

10. **Duplicate handling / dedup boundary**
    - redelivered source events are deduplicated at trigger-event level when source identity permits;
    - final prevention of duplicate logical stage dispatch still relies on A-11 logical idempotency;
    - trigger dedup and stage idempotency are separate defenses and identities;
    - a source with no stable event identity must use a certified deterministic ingress identity strategy or fail closed for high-authority production use.

11. **Ordering / out-of-order events**
    - no global ordering assumption;
    - retain source sequence/revision metadata when available;
    - older/stale revision arriving after newer revision cannot silently replace newer known state;
    - out-of-order events remain audit evidence;
    - exact state reconciliation policy may reference A-9/A-12.

12. **Corrections / retractions / supersession**
    - source correction/retraction is a new durable event linked to prior event;
    - it may cause reevaluation/supersession but never rewrites historical trigger/StageRun evidence;
    - if work already executed, later correction requires explicit recovery/reprocess policy rather than pretending the old trigger never happened.

13. **Debounce / burst coalescing**
    - high-frequency trigger events may be coalesced through a versioned generic policy;
    - raw trigger events/deliveries remain retained;
    - coalescing may reduce reevaluations but cannot erase provenance;
    - exact algorithm/cadence can remain policy-defined.

14. **Late triggers / timing boundaries**
    - arrival after a stage deadline does not grant permission to run;
    - trigger causes reevaluation against A-6 timing declaration + A-8 scheduler/missed-window policy + A-9 readiness/dependencies;
    - a late legitimate data update can be recorded even when no pregame action is still permissible.

15. **Operator/manual triggers**
    - authenticated operator identity/reason required for authoritative manual events;
    - a manual trigger requests reevaluation by default and does not silently bypass dependencies/approval/side-effect policy;
    - explicit override behavior, if allowed, belongs to A-19 and must be separately audited.

16. **External callbacks / publication receipts**
    - callbacks can be triggers for follow-up workflow stages but remain typed/versioned external evidence;
    - callback redelivery must be safe;
    - publication-specific meaning remains under A-18 contract.

17. **Security / payload hygiene**
    - trigger payload contracts must be safe to persist;
    - raw secrets/tokens/passwords cannot become trigger event data;
    - authentication/signature verification implementation belongs to A-20;
    - invalid/untrusted payloads fail closed and are retained only in sanitized diagnostic form according to policy.

18. **Replay / backfill / test delivery**
    - a replayed trigger is not mislabeled as the original live receipt;
    - retain original source occurrence time and actual replay/ingestion time;
    - environment/mode restrictions prevent historical replay from causing accidental production side effects;
    - trigger replay and StageRun replay/reprocess remain distinct concepts.

19. **Source outage / degraded trigger source**
    - absence of an event cannot automatically prove nothing changed;
    - plans may still rely on timer/poll/readiness fallback policies declared elsewhere;
    - trigger-source health is operational evidence, not sport truth;
    - alerting/incident behavior remains A-17.

20. **No direct trigger-to-side-effect path**
    - every trigger-derived action must pass through resolved-plan identity, stage applicability, dependencies, timing, readiness, execution mode, immutable target, and side-effect policy checks;
    - receiving a webhook/event can never by itself publish a pick or run a destructive operation.

### A-7 stress cases before certification

1. Same timer occurrence delivered/fired twice.
2. Same external webhook delivered multiple times with one stable source event ID.
3. Production source has no stable event ID and ingress cannot derive a safe deterministic occurrence identity.
4. Older schedule/scope revision arrives after a newer revision.
5. Source sends a corrected event revision.
6. Source retracts an earlier event after TDLA recorded it.
7. MLB sport event says relevant pregame state changed; TDLA reevaluates readiness without learning lineup/pitcher semantics.
8. NFL/NCAAF pregame state-change event does the same without football-specific branches.
9. Readiness-change hint arrives but A-5 readiness still returns `WAITING`.
10. Trigger arrives after the stage deadline.
11. Dependency-completion event is delivered twice.
12. Trigger arrives for a stage already `SUCCEEDED`.
13. Trigger arrives for a superseded old plan/stage revision.
14. Trigger arrives for a conditional stage already resolved `NOT_APPLICABLE`.
15. No-games discovery generates an empty-scope change/plan reevaluation without fake event work.
16. High-frequency burst of 100 equivalent/relevant events is coalesced while every raw event remains auditable.
17. TDLA crashes after trigger persistence but before evaluation; restart reprocesses safely.
18. TDLA crashes after evaluation but before/around dispatch; trigger handling + A-11 logical idempotency prevent duplicate logical work.
19. Two different source namespaces report related real-world change; they are not silently deduplicated as one source event unless an explicit correlation/coalescing rule says so.
20. Source clock is skewed and `occurred_at` is later than TDLA `received_at`; ordering does not depend blindly on source wall clock.
21. Trigger payload digest/schema mismatch.
22. Unauthenticated/invalid-signature external trigger attempt.
23. Trigger payload contains secret-like credential data; sanitized rejection/no secret persistence policy.
24. Authorized operator trigger requests reevaluation but cannot bypass required approval/dependency/timing policy.
25. Explicit future operator override (A-19) remains a separate auditable action from ordinary trigger delivery.
26. Publication callback/receipt is redelivered.
27. Event-time move causes A-8 to issue a new timer occurrence while a stale old timer later fires; old trigger cannot revive superseded work.
28. Trigger source is down for hours; absence of events does not become proof of readiness/no-change.
29. Replay a historical trigger into staging; it retains original occurrence time plus replay time and cannot reach production side effects.
30. Trigger matches no subscription; valid `NO_MATCH` result rather than system failure.
31. Trigger matches multiple declared bindings; each reevaluation is deterministic and remains independently idempotent.
32. Trigger correction arrives after downstream work already executed; original evidence remains and recovery/reprocess policy handles consequences.

## Expected A-7 outputs

Create at minimum:

- `docs/architecture/A07_TRIGGER_ARCHITECTURE_V1.md`;
- A-7 conformance/certification review after stress testing;
- ADR(s) if trigger event-vs-delivery identity, source authority, or durable ingestion introduces a durable tradeoff;
- `CHANGE_JOURNAL.md` entry;
- updated `ARCHITECTURE_CERTIFICATION_LOG.md`;
- updated architecture index/root README as needed;
- updated current resume point.

## Do not do yet

Until A-7 is certified:

- do not implement final webhook/event/timer schemas as if frozen;
- do not wire real provider/sport webhooks directly to production sport work;
- do not build production Prefect schedules/triggers as canonical trigger identity;
- do not let timer fires or webhooks bypass A-6 stage/dependency/side-effect validation;
- do not design final trigger PostgreSQL DDL ahead of A-13;
- do not implement the final event-relative scheduling algorithm ahead of A-8;
- do not implement exact readiness/dependency state transitions ahead of A-9;
- do not implement final logical idempotency/retry mechanics ahead of A-11;
- do not enable production publishing.

## Required reading for next session

1. `README.md`
2. `AGENTS.md`
3. this file
4. `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`
5. `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md`
6. `docs/architecture/A00-A04_FOUNDATION_ADDENDUM_V1_1.md`
7. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_V1.md`
8. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md`
9. `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`
10. `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md`
11. `docs/implementation/A06_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md`
12. `docs/adr/ADR-0001_CONTROL_PLANE_AND_VENDOR_NEUTRAL_IDENTITY.md`
13. `docs/adr/ADR-0002_TRANSPORT_NEUTRAL_SPORT_ADAPTER_PROTOCOL.md`
14. `docs/adr/ADR-0003_IMMUTABLE_PLAN_FRAGMENTS_AND_EXPLICIT_COMPOSITION.md`
15. relevant current DDC / Daily-MLB / Daily-NFL governing contracts while designing A-7.
