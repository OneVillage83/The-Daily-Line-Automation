# A-6 Architecture Conformance Review — Pipeline Plan / Stage Contracts

Review date: 2026-09-03  
Repository: `OneVillage83/The-Daily-Line-Automation`  
Reviewed architecture:

- `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`
- `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md`
- `docs/adr/ADR-0003_IMMUTABLE_PLAN_FRAGMENTS_AND_EXPLICIT_COMPOSITION.md`

Foundation dependencies reviewed for consistency:

- A-0 through A-4 Foundation V1 + V1.1 addendum;
- A-5 Sport Automation Adapter V1 + V1.1 addendum;
- ADR-0001 canonical TDLA identity / replaceable orchestrator;
- ADR-0002 transport-neutral sport adapter protocol;
- current Daily-Data-Core ownership/integration boundaries;
- current Daily-MLB asynchronous service/job shape;
- current Daily-NFL architecture direction and PIT/pregame monitoring requirements.

## Review purpose

A-6 must establish a sufficiently precise generic plan/stage graph so later implementation can build typed contracts without forcing TDLA to understand sport meaning or prematurely inventing trigger/scheduler/retry/database behavior.

The review therefore tests:

1. ownership isolation;
2. graph identity and validity;
3. stage definition vs concrete materialization identity;
4. sport-owned dynamic scope membership;
5. fan-out/fan-in behavior;
6. timing/readiness declaration boundaries;
7. typed input/output/success contracts;
8. side-effect/mode safety;
9. fragment composition authority;
10. plan revision/immutability;
11. deterministic canonical digest requirements;
12. compatibility with MLB/NFL/NCAAF workflow shapes;
13. explicit deferral boundaries for A-7 onward.

---

# Summary result

**PASS after four V1.1 certification clarifications.**

No blocking contradiction was found after applying `A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md`.

The review identified four places where the V1 base was directionally correct but insufficiently explicit for a future implementation contract:

1. A-5 supplies individual sport scope references but A-6 fan-out/fan-in needs an exact child-set binding. V1.1 defines neutral `ScopeSetBinding` without granting TDLA sport identity authority.
2. Deterministic hashing needed an explicit distinction between execution-semantic fields and presentation/audit metadata. V1.1 makes digest participation schema-controlled.
3. Repeated pre-event snapshots needed a stable logical schedule-slot identity independent of the wall-clock timestamp. V1.1 defines `ScheduleSlotRef`.
4. Execution-affecting policy references needed to resolve to immutable version/digest bindings before production dispatch. V1.1 defines `ResolvedPolicyBinding` requirements.

With these clarifications, A-6 is suitable for architecture certification.

---

# Ownership-boundary review

## TDLA vs sport repositories — PASS

A-6 preserves the A-5 rule that TDLA does not calculate sport meaning.

Sport systems retain authority over:

- sport scope identity/membership;
- stage meaning;
- applicability/readiness meaning;
- sport inputs/outputs semantics;
- report/model/settlement/evaluation semantics.

TDLA owns only generic plan validation/composition/materialization semantics.

The plan may contain a stage name such as a future MLB final-prediction stage or NFL late-snapshot stage, but TDLA cannot branch on that name. It uses only declared contracts, scope bindings, timing, dependencies, outputs, and policies.

## TDLA vs Daily-Data-Core — PASS

A-6 does not introduce odds/weather/provider acquisition logic. A stage may depend on sport-produced or DDC-backed provenance/output references, but DDC remains the shared acquisition/fact layer and the sport remains responsible for interpreting those facts.

## TDLA platform stages — PASS after ADR-0003

Generic TDLA-owned stages can be composed around sport work only through explicit typed ports and immutable fragments.

There is no plan-merge precedence that allows TDLA to overwrite a sport stage.

---

# Identity review

## Stage definition vs StageMaterialization — PASS

A single stage template can legitimately produce many concrete event-level operations.

The architecture distinguishes:

```text
StageDefinition
    -> StageMaterialization(scope + revision + slot/group)
        -> StageRun / logical operation
            -> RunAttempt(s)
```

Physical retries do not create new stage materialization identity.

## Repeated snapshot identity — PASS after V1.1

A resolved wall-clock timestamp is not used as the semantic snapshot identity. A stable `ScheduleSlotRef` identifies the intended logical snapshot.

This avoids accidental duplicate logical operations when a kickoff/game time moves.

## Dynamic scope-set identity — PASS after V1.1

`ScopeSetBinding` preserves exact sport-supplied member references and a membership digest while remaining a neutral orchestration object.

TDLA cannot invent or repair membership based on sport knowledge.

---

# Graph-model review

## DAG-only V1 — PASS

V1 uses a directed acyclic graph and rejects cycles before dispatch.

The design correctly keeps these behaviors outside graph cycles:

- readiness reevaluation;
- retries;
- recurring daily execution;
- event-time recalculation;
- repeated declared snapshots.

This simplifies validation and reproducibility without preventing the required workflows.

## Dependency semantics — PASS

Dependency satisfaction is explicit rather than implied by stage requiredness.

Important locked behavior:

- an `OPTIONAL` stage can still be a hard requirement if a downstream `OUTPUT` edge requires its output;
- a `NO_OP` cannot satisfy an output dependency for an output it did not create;
- degraded success satisfies only the outputs actually validated;
- terminal-failure dependencies are allowed only when the downstream stage intentionally consumes terminal evidence.

---

# Fragment composition review

## Explicit fragment authority — PASS

A resolved plan is constructed from immutable source fragments and an immutable `PlanAssembly`.

Sport stages and TDLA platform stages retain separate owner namespaces.

## Cross-fragment binding — PASS

Imports/exports require explicit typed port bindings.

No connection can be inferred from a filename, stage name, database path, or sport reason code.

## Conflict handling — PASS

There is no `last writer wins`, `TDLA wins`, or `sport wins` behavior.

Conflicts fail closed.

## Executable authority — PASS

The `ResolvedAutomationPlan`, not a sport fragment and not a Prefect flow object, is the canonical executable plan authority.

This is consistent with ADR-0001 and ADR-0003.

---

# Timing and readiness boundary review

## Timing declaration vs scheduler algorithm — PASS

A-6 defines typed absolute/relative timing declarations but explicitly defers:

- recalculation;
- rescheduling;
- missed-window mechanics;
- scheduler state transitions;

to A-8.

This is the correct boundary.

## Readiness declaration vs readiness engine — PASS

A-6 declares whether readiness is required and its freshness constraints, while A-5 supplies the generic readiness result and A-9 will own reevaluation/dependency state.

No sport readiness logic is duplicated.

---

# Input/output contract review

## Logical ports instead of filenames — PASS

Dependencies bind to typed logical inputs/outputs/manifests rather than guessed paths.

This allows sport implementations to change internal file layouts without changing generic TDLA graph semantics when external contracts remain compatible.

## Success criteria — PASS

Exit code/HTTP success alone is insufficient.

Required output schemas, manifests, digests, provenance, and declared semantic result must validate.

## No-op behavior — PASS

A no-op can be a valid successful operation only when the stage contract permits it and absent outputs are not required.

---

# Side-effect and execution-mode review

## Side-effect classification — PASS

V1 provides generic classes:

- `NONE`;
- `INTERNAL_EVIDENCE`;
- `EXTERNAL_OPERATIONAL`;
- `CUSTOMER_VISIBLE`;
- `DESTRUCTIVE_EXTERNAL`.

## Shadow mode — PASS

A shadow plan cannot contain an enabled uncontrolled customer-visible/destructive stage.

A structurally present publication stage must be deterministically disabled/not materialized in shadow.

## Supervised mode — PASS

Production-visible side effects that require approval must pass through an explicit TDLA approval boundary rather than being hidden in a sport compute command.

## Production mode — PASS

Plan permission does not equal production authorization. Certification/environment/immutable target/policy controls still apply.

---

# Canonical digest review

## Semantic canonicalization — PASS after V1.1

The architecture requires deterministic normalization and SHA-256 identity.

Semantically unordered collections are sorted by stable identity. Meaningful order is preserved only when the schema declares it meaningful.

## Presentation-only metadata — PASS after V1.1

Display labels/documentation metadata do not accidentally change execution-semantic plan identity.

Digest participation is controlled by the versioned schema.

## Immutable execution-affecting policies — PASS after V1.1

Mutable aliases may be used during resolution only. Production executable plans retain immutable policy version/digest bindings.

---

# Stress-test matrix

| # | Scenario | Result | Review notes |
|---|---|---|---|
| 1 | MLB daily slate with zero games | PASS | Empty sport-supplied `ScopeSetBinding` follows explicit empty-set policy; no fake events created. |
| 2 | MLB normal slate with many game scopes | PASS | `FOR_EACH_SCOPE` materializes one stage per exact sport-owned member ref. |
| 3 | MLB doubleheader with two event scopes | PASS | TDLA sees two opaque refs; no team/date/game-number inference. |
| 4 | MLB readiness waits then becomes ready | PASS | Same `StageMaterialization` proceeds after later readiness; no duplicate logical stage. |
| 5 | Optional enrichment fails; prediction still valid | PASS | Continuation allowed only when downstream does not require missing output and A-12 policy permits it. |
| 6 | Required upstream fails | PASS | `SUCCESS`/`OUTPUT` edges remain unsatisfied; dependent prediction/publication blocked. |
| 7 | NFL/NCAAF multiple pre-kickoff snapshots | PASS | Distinct stable `ScheduleSlotRef` values; no football conditionals in TDLA. |
| 8 | Event time moves after planning | PASS | Scope/schedule revision drives A-8 reevaluation; completed history stays on old revision. |
| 9 | Slate aggregate waits on exact child set | PASS | Fan-in binds exact membership digest; no sport-ID parsing. |
| 10 | Conditional stage becomes NOT_APPLICABLE | PASS | Resolution disposition recorded without dispatch; downstream edge explicitly declares accepted behavior. |
| 11 | Shadow plan with comparison artifacts | PASS | Internal evidence allowed; customer-visible path disabled/not materialized. |
| 12 | Supervised approval boundary | PASS | Generic TDLA approval stage/port can gate side effects without sport meaning. |
| 13 | Production auto-continuation | PASS | Requires explicit mode/side-effect/policy/certification authority. |
| 14 | Post-event settlement/evaluation | PASS | Same graph/adapter model; timing/dependencies generic, meaning sport-owned. |
| 15 | Plan revision after partial completion | PASS | New immutable resolved plan; completed evidence remains old, pending work reevaluated/superseded. |
| 16 | Dependency cycle | PASS | Structural validation rejects before dispatch. |
| 17 | Duplicate stage ID or dangling dependency | PASS | Namespaced `StageRef` uniqueness and reference validation fail closed. |
| 18 | Missing adapter capability | PASS | Plan resolution fails before dispatch. |
| 19 | Compute-only stage target has uncontrolled side effects | PASS | Side-effect/target contradiction fails closed. |
| 20 | Same semantic plan, different incidental serialization order | PASS | Semantic set sorting + canonical serializer requirement yields same digest. |
| 21 | Fan-out missing/unknown membership revision | PASS | Cannot materialize/aggregate silently; exact binding required. |
| 22 | Optional stage required by downstream output dependency | PASS | Downstream blocks if output missing; optionality does not override edge. |
| 23 | NO_OP with missing required output | PASS | Does not satisfy output dependency. |
| 24 | SUCCEEDED_DEGRADED with partial outputs | PASS | Only validated outputs can satisfy downstream requirements. |
| 25 | Two fragments define same StageRef | PASS | Composition conflict; no precedence. |
| 26 | Cross-fragment port schema mismatch | PASS | Composition fails before resolved plan exists. |
| 27 | Target resolves to mutable `latest` in production | PASS | Production resolved target validation fails. |
| 28 | Naive timestamp | PASS | Timing schema rejects before dispatch. |
| 29 | Scope membership changes after some child completion | PASS | New binding/revision does not absorb old member evidence silently. |
| 30 | Reordered stages/edges/ports | PASS | Semantically unordered collections canonicalize to the same plan digest. |

---

# Additional failure-path review

## Fragment digest mismatch

Result: **PASS**.

A source fragment whose recomputed digest differs from its claimed digest cannot participate in a resolved plan.

## Policy alias changes after plan resolution

Result: **PASS after V1.1**.

Resolved plan pins immutable policy version/digest, so later alias movement cannot alter historical behavior.

## Cosmetic stage-label change

Result: **PASS after V1.1**.

Presentation-only metadata does not change the semantic plan digest when the schema classifies it as non-semantic.

## Empty fan-out plus aggregate

Result: **PASS**.

Both fan-out empty-set behavior and aggregate empty-set behavior must be explicit; there is no accidental vacuous-success default.

## Retry after readiness change

Result: **PASS**.

Readiness is eligibility evidence. Retry attempt identity remains governed by A-11 and does not create a new schedule slot/materialization.

---

# Daily-MLB compatibility note

A-6 does not require the existing Daily-MLB manual pipeline to be rewritten now.

The eventual M13 adapter may expose a sport fragment around the **certified final manual MLB interface**, mapping its existing logical stages/results/artifacts into A-6 contracts.

Important constraints for that future work:

- event/slate membership must come from MLB-owned canonical scope references;
- the adapter must not make TDLA interpret pitcher/lineup meaning;
- internal MLB filenames can remain implementation details if exported manifests/ports are stable;
- publication must be separable from shadow compute if production-visible side effects exist;
- A-5 async idempotency/reconciliation requirements remain mandatory.

No A-6 certification implies that the current starter MLB stage decomposition is final.

---

# Daily-NFL / NCAAF compatibility note

A-6 supports multiple pregame snapshots through stable logical schedule slots and sport-owned readiness checks.

This is compatible with the existing football architecture direction where new legitimate pre-kickoff information can update later prediction snapshots without a blanket exclusion of game-day information.

TDLA does not need football-specific branches to support this pattern.

---

# Deferred-architecture review

A-6 does not improperly freeze later algorithms.

The following remain explicitly unresolved by design:

- A-7 exact trigger events/subscriptions/deduplication;
- A-8 scheduling/reschedule/missed-window algorithms;
- A-9 dependency/readiness state machine;
- A-10 execution backends;
- A-11 exact logical idempotency keys/retries/timeouts;
- A-12 failure propagation/recovery;
- A-13 DDL;
- A-14 artifact storage/retention;
- A-15 resource/concurrency budgets;
- A-16 observability;
- A-17 alerts/incidents;
- A-18 publication transport;
- A-19 operator approval implementation;
- A-20 security/service identity.

This deferral is intentional and does not block A-6 certification.

---

# Certification recommendation

**Recommend A-6 as `ARCHITECTURE-CERTIFIED` governed by:**

- `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`;
- `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md`;
- `docs/adr/ADR-0003_IMMUTABLE_PLAN_FRAGMENTS_AND_EXPLICIT_COMPOSITION.md`.

Certification grants architecture authority only. It does not certify runtime Pydantic models, canonical serializer code, Prefect flows, database tables, or a real sport adapter.

The next architecture checkpoint should be **A-7 Trigger Architecture**.
