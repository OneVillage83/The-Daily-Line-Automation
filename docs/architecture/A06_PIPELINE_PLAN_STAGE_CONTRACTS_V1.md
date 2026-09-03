# A-6 — Pipeline Plan / Stage Contracts V1

Status: **DOCUMENTED — REVIEW PENDING**  
Repository: `OneVillage83/The-Daily-Line-Automation`  
Architecture section: A-6  
Version: 1.0  
Initial documentation date: 2026-09-03

This document defines the generic, versioned plan and stage graph that The-Daily-Line-Automation (TDLA) may validate, materialize, schedule, execute, and audit without learning sport-specific meaning.

A-6 builds on the certified A-0 through A-5 contracts. A-5 defines the Sport Automation Adapter boundary and allows a sport adapter to return or validate a sport-owned plan fragment. A-6 defines the canonical structure, composition, graph semantics, stage contracts, and deterministic identity of the resulting automation plan.

A-6 does **not** define the final trigger engine, event-relative rescheduling algorithm, readiness engine, worker scheduler, retry algorithm, failure-recovery algorithm, persistence DDL, artifact-retention implementation, alert engine, or operator UI. Those remain owned by A-7 through A-19 as identified below.

---

# A-6.0 — Governing intent

The central rule is:

> **A plan tells TDLA what generic work relationships, contracts, timing declarations, and side-effect boundaries exist. It must never require TDLA to understand why a baseball lineup, football inactive list, weather state, model snapshot, settlement rule, or other sport-native concept matters.**

The V1 plan model is a **declarative directed acyclic graph (DAG)** assembled from immutable, versioned fragments. Sport-owned stages remain sport-owned. TDLA may add platform-owned operational stages only through explicit composition and typed bindings; it may not mutate a sport fragment in place or inject sport meaning.

Repeated readiness checks, trigger reevaluation, retries, and event-time recalculation do not create cycles in the plan graph. They are repeated evaluations/attempts of the same logical declaration under later architecture sections.

---

# A-6.1 — Core plan objects and identity layers

A-6 distinguishes four related objects.

## A-6.1.1 `PlanFragment`

An immutable declaration contributed by one authority namespace.

A fragment may be:

- `SPORT` — returned/validated through the A-5 sport adapter; or
- `TDLA_PLATFORM` — generic operational stages owned by TDLA, such as an explicit operator-approval boundary or generic distribution operation.

A fragment cannot contain stages owned by another authority namespace.

Conceptual fields:

```text
PlanFragment
- fragment_namespace
- fragment_kind                  # SPORT | TDLA_PLATFORM
- schema_version
- fragment_id
- fragment_version
- effective_from / effective_until
- allowed_environments
- allowed_execution_modes
- required_adapter_capabilities[]
- stage_definitions[]
- dependency_definitions[]
- exported_ports[]
- imported_ports[]
- policy_references[]
- canonical_fragment_digest
```

## A-6.1.2 `PlanAssembly`

An immutable composition specification that identifies the fragments to combine and the explicit cross-fragment bindings between their exported/imported ports.

Conceptual fields:

```text
PlanAssembly
- schema_version
- assembly_id
- assembly_version
- fragment_refs[]                # exact IDs/versions/digests
- explicit_port_bindings[]
- environment
- execution_mode
- scope_binding_refs[]
- adapter_descriptor_ref/digest
- assembly_policy_refs[]
- canonical_assembly_digest
```

There is no implicit name matching and no "last writer wins" precedence.

## A-6.1.3 `ResolvedAutomationPlan`

The immutable, executable generic graph resulting from successful fragment validation, explicit composition, scope binding, target resolution, and capability checks.

Conceptual fields:

```text
ResolvedAutomationPlan
- schema_version
- plan_namespace
- plan_id
- plan_version
- source_fragment_refs/digests[]
- assembly_ref/digest
- adapter_descriptor_ref/digest
- bound_scope_refs/revisions[]
- environment
- execution_mode
- effective/valid interval
- resolved_stage_definitions[]
- resolved_dependencies[]
- resolved_port_bindings[]
- resolved_execution_targets[]
- resolved_policy_refs[]
- canonical_plan_digest
```

A `ResolvedAutomationPlan` is the authority used to materialize logical work. It is immutable once it has produced execution history.

## A-6.1.4 `StageMaterialization`

A deterministic binding of a stage definition/template to one concrete scope and logical schedule slot/group.

This distinction prevents a single authored stage definition such as "run per event in the slate" from becoming an ambiguous identity for many game-level executions.

Conceptual identity inputs include:

- resolved plan digest;
- canonical stage reference;
- concrete A-5 `SportScopeRef` + revision;
- expansion group/membership revision where applicable;
- logical schedule slot/reference where the plan declares repeated snapshots;
- execution mode/environment.

The exact TDLA logical idempotency key construction remains A-11, but A-6 requires stage materialization identity to be deterministic and stable across physical retries.

---

# A-6.2 — Plan versioning and immutability

## A-6.2.1 Version rules

- Changing the meaning of an existing plan or fragment creates a new version.
- Changing the meaning, required inputs, required outputs, side-effect classification, or semantic contract of a stage creates a new stage contract version and therefore a new fragment/plan digest.
- Additive optional fields may evolve under compatible schema-version rules, but existing field meaning cannot silently change.
- A plan/fragment version that has production history is immutable.
- Completed execution evidence always retains the exact plan/fragment/stage versions and digests actually used.

## A-6.2.2 Plan identity vs resolved execution identity

A reusable authored fragment may reference an execution-target policy/selector, but production dispatch requires an immutable resolved execution target.

Therefore:

```text
authored fragment identity
    !=
resolved executable plan identity when release/target binding differs
```

The `ResolvedAutomationPlan` digest includes the resolved immutable target references required for execution. Promoting a different sport release may produce a different resolved plan digest even if the higher-level graph topology is otherwise unchanged.

---

# A-6.3 — Stage identity and ownership

## A-6.3.1 Canonical stage reference

A stage reference is structured rather than a globally guessed string:

```text
StageRef
- owner_namespace
- local_stage_id
- stage_contract_version
```

`owner_namespace` prevents collisions between a sport fragment and TDLA platform stages.

Examples are illustrative only:

```text
owner_namespace = "daily-mlb"
local_stage_id   = "prediction_snapshot_final"

owner_namespace = "tdla"
local_stage_id   = "operator_approval"
```

TDLA generic logic may compare exact declared `StageRef` values for graph identity but cannot derive sport behavior from the local name.

## A-6.3.2 Owner rule

- A `SPORT` fragment may define only sport-owned stages.
- A `TDLA_PLATFORM` fragment may define only generic TDLA operational stages.
- TDLA cannot replace, modify, or shadow a sport stage definition with the same identity.
- Duplicate canonical `StageRef` values across the resolved plan fail validation.

## A-6.3.3 Stage contract version

`stage_contract_version` changes when the stage's semantic output contract changes in a way that a downstream consumer must distinguish.

A code release may change without a stage-contract change if the external semantic contract remains compatible; the immutable execution target still records the release difference in the resolved plan/execution envelope.

---

# A-6.4 — V1 graph model: DAG only

## A-6.4.1 Directed acyclic graph

The V1 resolved plan is a DAG.

A plan fails before dispatch if it contains:

- a direct cycle;
- an indirect cycle;
- a self-dependency;
- a dangling dependency;
- an ambiguous stage/port reference.

Loops are not represented by graph cycles.

Examples that **do not** require cycles:

- repeated readiness polling -> A-9 reevaluates one stage's readiness;
- retry -> A-11 creates another physical attempt of the same logical operation;
- recurring daily execution -> A-7/A-8 create new logical plan/run instances;
- multiple pregame snapshots -> the sport plan declares separate logical stage/schedule slots or a repeated-stage template with deterministic materializations.

A future requirement for true cyclic workflow semantics requires a new architecture version/ADR rather than silently weakening V1 DAG guarantees.

## A-6.4.2 Dependency edges

Every edge is explicit and carries a generic satisfaction requirement.

Conceptually:

```text
DependencyEdge
- upstream_stage_ref or expansion_group_ref
- downstream_stage_ref
- requirement_kind
- required_output_port_ref (when applicable)
- allow_empty_expansion (when applicable)
- allow_upstream_not_applicable (when applicable)
- edge_policy_ref (optional)
```

Initial generic `requirement_kind` families are:

- `SUCCESS` — upstream logical work must satisfy its generic success contract;
- `OUTPUT` — a declared output contract/port must validate and be available;
- `TERMINAL` — upstream must reach an allowed terminal outcome; used only where a downstream operation intentionally runs after completion regardless of business success;
- `EXPANSION_BARRIER` — a fan-in condition over a declared materialized child set.

A downstream stage does not become eligible merely because its upstream stage is marked "optional." Dependency satisfaction is determined by the edge contract and required input/output availability.

---

# A-6.5 — Stage classification

Each stage declares generic properties without encoding sport meaning.

Conceptual fields:

```text
StageDefinition
- stage_ref
- display_label (safe/non-authoritative)
- owner_kind / owner_namespace
- scope_binding
- requiredness
- applicability
- timing_declaration
- readiness_declaration
- input_specs[]
- output_specs[]
- execution_target_declaration
- required_adapter_capabilities[]
- side_effect_declaration
- policy_refs
- expansion_spec (optional)
- aggregation_spec (optional)
```

## A-6.5.1 Requiredness

Initial values:

- `REQUIRED`
- `OPTIONAL`
- `CONDITIONAL`

`OPTIONAL` means failure/absence may be permitted by the plan; it does **not** mean every downstream dependency ignores it.

`CONDITIONAL` means applicability must be resolved through a declared generic or adapter-evaluated rule before dispatch.

## A-6.5.2 Applicability

V1 permits only declarative applicability mechanisms:

- `ALWAYS`;
- `ADAPTER_EVALUATED` — the A-5 readiness/applicability boundary determines applicability without TDLA sport logic;
- `GENERIC_CONTRACT_PREDICATE` — a strictly generic predicate over declared contract metadata, such as presence of an optional upstream port.

Arbitrary executable expressions embedded in plan text are prohibited in V1.

When an adapter returns `NOT_APPLICABLE`, TDLA records a **stage resolution/materialization disposition** of `NOT_APPLICABLE` and does not dispatch a sport child operation. This is not misreported as failure or cancellation.

`NOT_APPLICABLE` is a plan-resolution disposition, not a new A-2 execution terminal status. Downstream behavior is determined explicitly by dependency/input contracts.

---

# A-6.6 — Scope binding and stage materialization

A stage does not parse sport IDs. It binds to A-5 sport-owned scope references.

## A-6.6.1 Single-scope binding

A stage may bind directly to one declared `SportScopeRef` such as one event, slate, evaluation cycle, or historical range.

## A-6.6.2 Scope-set binding

A stage template may bind to each member of a sport-owned scope set.

Conceptually:

```text
ExpansionSpec
- mode = FOR_EACH_SCOPE
- scope_set_ref
- scope_set_revision/digest
- member_scope_kind constraint (optional)
- empty_set_policy
- expansion_group_id
```

The sport system owns scope-set membership and identity. TDLA may materialize one stage per returned member reference but cannot infer, merge, split, or rename sport members.

## A-6.6.3 Membership freeze

For one resolved plan materialization, the fan-out member set is bound to a specific membership revision/digest.

If the sport later changes the authoritative set—for example because of postponement, a newly identified doubleheader event, or schedule correction—the new scope-set revision triggers plan reevaluation/supersession under A-8. Existing completed child evidence is not silently attached to the new member set.

## A-6.6.4 Empty set policy

Zero members is not automatically an error.

Every fan-out declares one of:

- `ALLOW_EMPTY_NO_OP` — zero materialized children is a valid empty result;
- `ALLOW_EMPTY_NOT_APPLICABLE` — the group resolves not applicable;
- `REQUIRE_NON_EMPTY` — zero members fails plan/materialization validation for that operation.

This permits a certified no-games day without inventing fake game stages.

---

# A-6.7 — Fan-in and aggregation barriers

A fan-in stage can depend on an explicit expansion group without parsing sport identities.

Conceptual declaration:

```text
AggregationSpec / ExpansionBarrier
- expansion_group_ref
- membership_revision/digest
- completion_requirement
- required_output_port (optional)
- empty_set_behavior
```

Initial generic completion requirements include:

- `ALL_REQUIRED_SUCCESS` — every materialized child that is required by the source template satisfies success/output requirements;
- `ALL_TERMINAL` — every materialized child reaches an allowed terminal state; used only by workflows intentionally aggregating terminal evidence;
- `QUORUM` — an explicitly numeric count/ratio threshold when a plan legitimately permits partial completion.

`QUORUM` thresholds are plan data, not sport-specific TDLA code.

An aggregate stage must bind to the exact expansion membership revision/digest it is aggregating. A changing slate cannot silently change the population underneath a running aggregate.

---

# A-6.8 — Timing declaration boundary

A-6 defines **timing declarations**. A-8 owns evaluation, recalculation, scheduling, missed-window behavior execution, and event-reschedule algorithms.

Every production stage with timing constraints declares a typed timing structure.

## A-6.8.1 Absolute timing

Conceptually:

```text
AbsoluteTiming
- not_before_utc (optional)
- target_at_utc (optional)
- deadline_at_utc (optional)
- validity_until_utc (optional)
- missed_window_policy_ref
```

All timestamps are timezone-aware and normalized for canonical identity. Naive datetimes are invalid.

## A-6.8.2 Relative timing

Conceptually:

```text
RelativeTiming
- anchor_ref
- offset
- earliest_offset/window
- target_offset
- deadline_offset/window
- validity_offset/window
- schedule_revision_binding
- missed_window_policy_ref
```

Allowed anchor references are generic orchestration anchors supplied through the bound scope/plan contract, such as:

- scope `event_start_time`;
- scope effective start/end;
- a named opaque sport-provided anchor whose resolved timestamp is supplied as contract data.

TDLA may perform timestamp arithmetic. It may not interpret why an anchor is significant to the sport.

## A-6.8.3 Impossible windows

A resolved stage fails validation if declared timing constraints are internally impossible, for example:

```text
not_before > deadline
validity_until < target
```

Exact tolerance/missed-window actions are deferred to A-8/A-12 but contradictions fail closed before dispatch.

---

# A-6.9 — Readiness declaration

A stage declares whether A-5 readiness evaluation is required before dispatch.

Conceptually:

```text
ReadinessDeclaration
- required: bool
- adapter_stage_context
- maximum_readiness_age (optional)
- must_bind_scope_revision: bool
- freshness_policy_ref (optional)
- reevaluation_policy_ref (A-9)
```

The plan may require a fresh readiness result before every relevant dispatch window.

TDLA never converts stage names such as lineup, inactive, pitcher, or injury into hardcoded readiness logic. It passes the declared stage/scope context to the adapter and consumes the generic A-5 readiness disposition.

---

# A-6.10 — Input contract

Inputs are logical, typed contract dependencies, not guessed filenames or database tables.

Conceptual input specification:

```text
InputSpec
- input_name
- requiredness
- source_kind
- source_stage_ref / source_output_port_ref (when internal)
- external_input_ref/schema_ref (when external)
- schema_name/version
- expected_digest/reference rules
- freshness/cutoff policy ref
- provenance requirement
```

Initial source families:

- upstream stage output;
- explicitly bound external/sport input reference;
- TDLA platform input/reference;
- resolved configuration reference.

A sport artifact remains sport-owned in meaning. TDLA validates generic schema/hash/provenance requirements declared by contract.

## A-6.10.1 No filename guessing

A stage cannot declare "read `predictions.json` if present" as its canonical input contract without a corresponding logical output/manifest binding.

Paths may exist inside artifact manifests, but dependency identity is the declared logical port/artifact reference.

---

# A-6.11 — Output and generic success contract

Conceptual output specification:

```text
OutputSpec
- output_name / port_ref
- requiredness
- output_kind
- schema_name/version
- manifest_requirement
- content_digest_requirement
- provenance_requirement
- retention_policy_ref
- externally_consumable flag
```

A stage's generic TDLA success contract is satisfied only when:

1. the sport/platform execution returns an allowed semantic result;
2. all required declared outputs validate;
3. required manifests/hashes/provenance references validate;
4. execution-mode/side-effect constraints were respected.

## A-6.11.1 `SUCCEEDED_DEGRADED`

A `SUCCEEDED_DEGRADED` execution can satisfy downstream dependencies only if every output required by those dependencies is valid and the plan's failure/degradation policy allows the degraded condition.

Optional missing outputs remain explicitly missing; they are not invented.

## A-6.11.2 `NO_OP`

A sport/platform result may declare semantic outcome `NO_OP` while the TDLA logical stage resolves as successful **only when the stage contract allows a no-op and does not require absent outputs**.

A no-op cannot satisfy an `OUTPUT` dependency for an output it did not produce.

This permits valid no-games/no-change operations without adding a misleading execution failure.

---

# A-6.12 — Execution target binding

## A-6.12.1 Authored target declaration

An authored fragment may identify:

- an immutable target directly; or
- a versioned target-selection policy/reference that must resolve before the executable plan is accepted.

## A-6.12.2 Resolved target

Before production dispatch, each executable stage has an immutable target reference appropriate to its owner, for example:

- OCI image digest;
- immutable released wheel/application digest;
- versioned remote sport-service release identity whose deployed instance can prove that release;
- TDLA platform worker image digest.

A moving branch or mutable `latest` tag is not a production resolved target.

## A-6.12.3 Capability binding

Every stage lists required adapter/runtime capabilities. Resolution fails closed if the negotiated A-5 descriptor does not provide them.

Execution target release identity and adapter implementation identity are both retained; neither substitutes for the other.

---

# A-6.13 — Generic resource and worker hints

A stage may declare generic execution requirements/hints such as:

- worker class;
- CPU/heavy-CPU/GPU requirement;
- memory class;
- expected concurrency group;
- provider/resource budget class;
- network/data-locality capability.

These are declarations only.

A-10 owns worker/execution-backend dispatch semantics. A-15 owns concurrency/provider/resource budgeting. A-6 does not freeze the scheduling algorithm.

---

# A-6.14 — Side-effect classification and execution-mode safety

Every stage declares its generic side-effect class.

Initial V1 classes:

- `NONE` — read/compute only; no durable external mutation beyond ordinary logs/ephemeral execution evidence;
- `INTERNAL_EVIDENCE` — writes only to explicitly isolated internal evidence/artifact state;
- `EXTERNAL_OPERATIONAL` — changes an external system but is not customer-visible product publication;
- `CUSTOMER_VISIBLE` — publishes/sends/mutates user-facing content or subscriber-visible state;
- `DESTRUCTIVE_EXTERNAL` — deletes/revokes/destructively changes external state.

A stage also declares allowed execution modes.

## A-6.14.1 No hidden side effects

A stage declared `NONE` or `INTERNAL_EVIDENCE` cannot bind to an execution target known/declared to perform uncontrolled external/customer-visible effects.

If target capability/contract evidence conflicts with the stage declaration, resolution fails closed.

## A-6.14.2 Shadow

A resolved `AUTOMATION_SHADOW` plan cannot include an enabled uncontrolled `CUSTOMER_VISIBLE` or `DESTRUCTIVE_EXTERNAL` stage.

A customer-visible stage may remain structurally present only if it is explicitly disabled/not materialized under a deterministic mode rule and that fact is represented in the plan resolution evidence.

## A-6.14.3 Supervised

A supervised plan may perform compute/internal work but any declared production side-effect path that requires operator approval must depend on an explicit approval contract/stage/port owned by TDLA under A-19.

## A-6.14.4 Production

Production-side-effect stages require plan permission, environment permission, certified integration authority, immutable approved target, and applicable policy satisfaction. Plan structure alone never grants production authority.

---

# A-6.15 — Policy references, not premature algorithms

Stages/plans may reference versioned policy identities for behavior whose exact mechanics are defined later.

At minimum:

- trigger policy -> A-7;
- event-relative scheduling/missed-window policy -> A-8;
- readiness reevaluation/dependency policy -> A-9;
- worker/execution policy -> A-10;
- retry/timeout/idempotency policy -> A-11;
- failure/degradation/recovery policy -> A-12;
- persistence/audit policy -> A-13;
- artifact/retention/replay policy -> A-14;
- resource/concurrency/provider-budget policy -> A-15;
- observability policy -> A-16;
- alert/incident policy -> A-17;
- publication/distribution policy -> A-18;
- approval/operator policy -> A-19;
- security/service-identity policy -> A-20.

A policy reference is versioned input to resolution/execution. TDLA must not invent a default production-critical algorithm because a reference is missing.

---

# A-6.16 — Cross-fragment ports and deterministic composition

## A-6.16.1 Explicit ports

A fragment may expose typed logical outputs as `exported_ports` and declare required typed `imported_ports`.

Conceptually:

```text
PlanPort
- port_ref
- owner_namespace
- direction                  # IMPORT | EXPORT
- schema/output contract ref
- requiredness
- producing/consuming stage ref
```

## A-6.16.2 Explicit binding only

Cross-fragment dependency is legal only through an explicit binding in `PlanAssembly`.

Example conceptually:

```text
sport fragment exports: sport_report_package
TDLA publication fragment imports: publication_package
PlanAssembly explicitly binds the two compatible ports
```

TDLA does not scan stage names or output filenames to guess that two ports should connect.

## A-6.16.3 No silent overrides

Composition has **no generic precedence rule** such as "TDLA wins" or "sport wins."

Conflicts fail closed, including:

- duplicate stage refs;
- incompatible port schemas;
- two bindings to a single-consumer port when not explicitly multi-valued;
- incompatible environment/mode restrictions;
- contradictory immutable target bindings;
- contradictory policy constraints.

## A-6.16.4 Generic TDLA wrappers cannot inject sport meaning

TDLA platform fragments may add generic operational boundaries such as approval, distribution, archival, or system-level evidence handling.

They may not add a stage whose correctness depends on interpreting sport-specific content unless that logic belongs in and is invoked through the sport adapter.

---

# A-6.17 — Deterministic canonicalization and digests

Plan identity must not depend on incidental serialization order.

## A-6.17.1 Canonical semantic normalization

Before hashing, the plan/fragment/assembly is normalized so that:

- object/map keys are ordered deterministically;
- collections that are semantically sets (stages, edges, ports, capability refs, policy refs) are sorted by stable canonical identity;
- collections whose order is declared semantically meaningful preserve that order;
- timestamps use a normalized timezone-aware RFC-3339/UTC representation;
- durations use one exact representation defined by the contract schema, not binary floating-point;
- null/omitted-field handling is schema-defined;
- unknown extension fields are either included deterministically under the schema or rejected according to compatibility rules;
- resolved immutable target refs and bound scope/membership revisions are included in the resolved plan identity.

## A-6.17.2 Digest

V1 uses SHA-256 over the canonical UTF-8 serialization of the normalized semantic object.

Implementation must freeze one concrete canonical serializer/profile in M1 contract code and prove test vectors. A different serializer may be adopted only if it produces the same canonical bytes/digest or through an explicit versioned schema/digest-algorithm change.

## A-6.17.3 Digest hierarchy

Separate digests are retained for:

- each source fragment;
- plan assembly;
- resolved plan;
- relevant stage definitions/materializations where useful.

The resolved plan digest does not erase its component digests.

---

# A-6.18 — Plan revision, scope revision, and supersession boundary

A-6 defines identity and immutability. A-8 owns the exact scheduler/reschedule algorithm.

Rules:

1. A changed fragment version/digest is new plan authority, not mutation.
2. A changed scope/schedule/membership revision can cause a new resolved plan/materialization.
3. Completed StageRuns remain associated with the exact old plan/stage/scope revision used.
4. Pending/unstarted work may be reevaluated or superseded under A-8/A-12 policy.
5. A new plan cannot silently claim prior completed work unless compatibility/reuse rules are explicitly declared and validated.
6. Supersession records lineage between old and replacement planned/materialized work when a replacement exists.
7. Event-time price/data changes do not automatically create new stage identity unless the plan/scheduler contract declares a new logical snapshot/materialization.

---

# A-6.19 — Stage applicability and dependency resolution

Conditional/not-applicable behavior must remain deterministic.

## A-6.19.1 Applicability resolution record

Before dispatch, TDLA retains the result of applicability resolution sufficient to explain why a stage was materialized or not materialized.

Generic dispositions include:

- `MATERIALIZED`;
- `NOT_APPLICABLE`;
- `EMPTY_EXPANSION`;
- `SUPERSEDED_BEFORE_MATERIALIZATION`.

These are plan-resolution records, not physical execution attempt states.

## A-6.19.2 Downstream behavior

A downstream edge/input must explicitly state whether it accepts:

- an upstream stage that was not applicable;
- an empty expansion;
- a no-op result;
- degraded success;
- terminal failure for intentionally terminal-evidence workflows.

There is no universal rule that "optional means satisfied." Ambiguous dependency semantics fail validation.

---

# A-6.20 — Validation and fail-closed rules

A resolved plan cannot dispatch if any applicable validation fails.

Mandatory V1 validation includes at least:

1. schema version supported;
2. fragment/assembly/plan digest recomputes correctly;
3. exact source fragment digests available;
4. duplicate `StageRef` absent;
5. graph acyclic;
6. all dependency refs resolve;
7. all cross-fragment bindings explicit;
8. port schemas compatible;
9. scope refs/revisions structurally valid under A-5;
10. scope-set membership revision/digest bound for fan-out/fan-in;
11. stage requiredness/applicability declared;
12. timing declaration structurally valid and timezone-aware;
13. timing window not internally impossible;
14. readiness requirements structurally valid;
15. every required input has a resolvable source/binding;
16. required output schemas/manifests declared where needed;
17. every production executable stage resolves to an immutable execution target;
18. required adapter capabilities present;
19. allowed environment includes current environment;
20. allowed execution mode includes current mode;
21. side-effect classification is present and compatible with mode;
22. target capability/behavior does not contradict declared side-effect class;
23. required policy refs exist where the plan declares no safe default;
24. fan-in references the exact declared expansion group/membership revision;
25. empty-set behavior declared for dynamic fan-out;
26. conditional-stage downstream semantics are unambiguous.

A validation failure is retained as plan-resolution evidence. TDLA does not partially execute a plan that failed structural validation.

---

# A-6.21 — Required behavior for key workflow patterns

## A-6.21.1 No-games day

A sport discovery result may return zero event scopes. A fan-out bound to that set follows its declared empty-set policy. No fake event stages are created.

## A-6.21.2 Multiple games / doubleheader

Each sport-owned event scope is opaque and distinct. Fan-out materializes one stage per scope reference. TDLA does not infer game numbering or merge events by team/date.

## A-6.21.3 Late readiness

A stage may remain unresolved/not dispatchable while A-5 readiness is `WAITING`. A later `READY` result allows the **same logical stage materialization** to proceed; TDLA does not create a duplicate logical stage merely because readiness changed.

## A-6.21.4 Optional enrichment failure

An optional stage may fail without killing the full plan only when downstream dependency/input contracts do not require its unavailable output and the declared A-12 degradation/failure policy permits continuation.

## A-6.21.5 Required upstream failure

A downstream `SUCCESS` or `OUTPUT` dependency is not satisfied by a failed required upstream stage. Prediction/publication cannot continue through an unsatisfied required edge.

## A-6.21.6 Multiple pre-event snapshots

A sport may declare multiple snapshot stages or deterministic schedule slots. TDLA treats each declared logical materialization separately while remaining ignorant of football/baseball meaning.

## A-6.21.7 Rescheduled event

A changed A-5 schedule/scope revision causes A-8 to reevaluate future materializations. Completed evidence remains attached to the old revision; pending stages may be superseded according to policy.

## A-6.21.8 Slate aggregation

An aggregate stage waits on an explicit expansion barrier bound to the exact member-set revision. It never parses sport IDs to guess which games belong to the slate.

## A-6.21.9 Shadow/supervised/production

The same sport fragment may participate in different assemblies/resolved plans for different certified modes, but side-effect declarations and explicit platform gates must make the difference machine-verifiable.

## A-6.21.10 Post-event settlement/evaluation

Settlement/evaluation stages use the same graph/adapter contracts and may bind to post-event timing/dependency declarations. Sport meaning remains inside the sport adapter/system.

---

# A-6.22 — Deferred details and ownership map

A-6 intentionally defers:

- trigger-source/event schema -> A-7;
- exact event-relative scheduling, reschedule, missed-window algorithm -> A-8;
- dependency state machine/readiness polling cadence -> A-9;
- worker/execution backend selection -> A-10;
- exact idempotency-key construction, retries, timeouts -> A-11;
- failure propagation/degradation/recovery algorithm -> A-12;
- PostgreSQL tables/immutability enforcement -> A-13;
- artifact storage/retention/replay implementation -> A-14;
- concurrency/provider budgets -> A-15;
- metrics/tracing/log schema -> A-16;
- alerts/incidents -> A-17;
- distribution/publication transport -> A-18;
- operator approval implementation -> A-19;
- service identity/signing/secrets -> A-20;
- deployment/HA -> A-21;
- release pipeline -> A-22.

Implementation must not use these deferrals as permission to invent conflicting behavior early.

---

# A-6.23 — Architecture invariants

1. V1 plans are DAGs.
2. Sport meaning remains behind the A-5 adapter boundary.
3. The canonical executable object is an immutable `ResolvedAutomationPlan` built from immutable fragments + explicit assembly bindings.
4. TDLA platform fragments may add generic operational stages but cannot mutate sport stages or inject sport meaning.
5. Cross-fragment connections require explicit typed port bindings; there is no filename/stage-name guessing.
6. Stage identity is namespaced and versioned.
7. Stage materialization is distinct from stage definition and is bound deterministically to concrete scope/revision/schedule context.
8. Fan-out membership is sport-owned and revision-bound; TDLA never invents child event identity.
9. Fan-in binds to the exact expansion member-set revision.
10. Zero members can be a valid declared no-op/not-applicable result.
11. Optional/conditional stages do not automatically satisfy downstream dependencies.
12. Readiness changes do not create duplicate logical stage identity.
13. Required outputs/manifests, not exit code alone, determine generic success.
14. `NO_OP` and degraded success satisfy only explicitly compatible dependencies/contracts.
15. Production dispatch resolves immutable execution targets.
16. Side-effect class and execution mode are machine-verifiable plan data.
17. Shadow cannot hide customer-visible side effects inside compute stages.
18. Plan composition has no silent override precedence; conflicts fail closed.
19. Canonical semantic serialization + SHA-256 produces deterministic plan identity.
20. Completed evidence remains bound to the exact plan/stage/scope revision used.
21. Plan/scope revisions create new authority and may supersede pending work; they never rewrite completed history.
22. Policy references remain versioned inputs and defer algorithm ownership to the appropriate later architecture section.

---

# A-6.24 — Certification stress-test checklist

A-6 cannot be certified until the review explicitly evaluates at least:

1. MLB daily slate with zero games.
2. MLB normal slate with many game child scopes.
3. MLB doubleheader with two distinct event scopes.
4. MLB stage waits for probable-pitcher/lineup readiness, later becomes ready, and retains one logical stage materialization.
5. Optional enrichment failure with required prediction path still valid.
6. Required upstream failure blocks dependent prediction/publication.
7. NFL/NCAAF multiple event-relative snapshots without TDLA football branches.
8. Authoritative event time changes after future stages were planned.
9. Slate-level aggregation waits on the exact declared child set without parsing sport IDs.
10. Conditional stage resolves `NOT_APPLICABLE` with deterministic downstream handling.
11. Shadow plan produces comparison artifacts with no production-visible publication effect.
12. Supervised plan stops at explicit approval boundary.
13. Production plan auto-continues only under explicit certified side-effect policy.
14. Post-event settlement/evaluation activates only after declared timing/dependencies.
15. Plan revision arrives with completed + pending stages; completed evidence remains immutable and pending work is reevaluated/superseded.
16. Dependency cycle fails before dispatch.
17. Duplicate stage refs/dangling dependency fail before dispatch.
18. Missing required adapter capability fails before dispatch.
19. Stage claims compute-only but execution target can perform uncontrolled external side effects; fail closed.
20. Same semantic plan with different incidental serialization order produces identical canonical digest.
21. Lost/empty fan-out membership revision cannot be aggregated silently.
22. Optional stage is still required by a downstream `OUTPUT` dependency; downstream correctly blocks when output is missing.
23. A `NO_OP` stage cannot satisfy an output dependency for an output it did not create.
24. A degraded-success stage can satisfy only outputs actually validated.
25. Two fragments attempt to define the same `StageRef`; composition fails rather than applying precedence.
26. Cross-fragment output/import schemas mismatch; composition fails.
27. Target selector resolves to mutable `latest` in production; plan fails before dispatch.
28. Plan contains a naive timestamp; plan fails validation.
29. Fan-out member set changes after some child stages completed; new membership revision does not silently absorb old children.
30. Reordering semantically unordered stages/edges/ports does not change the resolved plan digest.

---

# A-6.25 — Certification boundary

A-6 certification, when granted, certifies the **architecture contract only**.

It does not certify:

- Pydantic models;
- canonical serializer implementation;
- Prefect flows;
- PostgreSQL DDL;
- a Daily-MLB/NFL/NCAAF adapter;
- scheduling/retry/recovery algorithms;
- publication authority.

Those require their own implementation and architecture-conformance evidence under the roadmap.
