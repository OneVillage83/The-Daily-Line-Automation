# A-0 through A-4 — Automation Foundation Architecture V1

Status: **DOCUMENTED — certification review pending**  
Repository: `OneVillage83/The-Daily-Line-Automation`  
Architecture family: TDLA A-0 through A-24  
Version: 1.0  
Initial documentation date: 2026-09-02

This document is the governing architecture contract for A-0 through A-4. Implementation must not contradict it without an explicitly documented architecture revision and ADR.

---

# A-0 — Mission, Principles, and System Boundary

## A-0.1 Mission

The-Daily-Line-Automation (TDLA) exists to provide a durable, auditable, recoverable, multi-sport control plane for The Daily Line production ecosystem.

TDLA answers operational questions such as:

- What work is expected to run?
- What caused it to become eligible?
- When should it run relative to an event or operational deadline?
- Which immutable release/configuration should execute?
- Which prerequisites must be satisfied first?
- Which worker/resource class should execute it?
- What attempt is currently active?
- What failed, and is failure retryable?
- What outputs constitute success?
- Which external side effects occurred?
- What was superseded, replayed, backfilled, or reprocessed?
- What is the exact next operational action?

TDLA is not a sports modeling repository.

## A-0.2 Primary design goals

1. **Multi-sport from first principles.** Adding a sport must not require editing generic orchestration logic with sport-specific branches.
2. **Durable operational history.** Production decisions and actions must be reconstructable after code, staff, providers, and infrastructure change.
3. **Deterministic logical identity.** Retries, duplicate triggers, worker restarts, and reschedules must not create uncontrolled duplicate work.
4. **Immutable release execution.** Production must identify exactly which code/config/model/dependency artifact executed.
5. **Failure as a designed state.** Timeouts, provider degradation, process death, network faults, delayed sport inputs, and publication failures must have explicit behavior.
6. **Manual-to-automated equivalence.** Automation earns authority after a certified manual pipeline exists and equivalence is demonstrated.
7. **Replaceable infrastructure.** Prefect, Docker/Kubernetes, object storage, observability, and alert providers are implementation mechanisms, not TDLA domain identity.
8. **Detailed project memory.** Every material change leaves durable human-readable documentation and an exact resume point.

## A-0.3 Non-goals

TDLA does not:

- become a shared feature store;
- become the source of truth for sport team/player/game ontology;
- implement sport models or simulations;
- determine sport-specific prediction correctness;
- implement generic odds/weather/provider acquisition already owned by DDC;
- directly own website presentation schema;
- treat scheduler/orchestrator vendor state as sufficient long-term audit authority.

## A-0.4 Control-plane / worker-plane separation

TDLA is conceptually separated into:

### Control Plane
Owns planning, trigger evaluation, scheduling, dependency/readiness state, dispatch, authoritative TDLA run state, retries, operator controls, audits, publication coordination, and operational APIs.

### Worker Plane
Executes immutable workloads selected by the control plane. Worker classes may include:

- IO-light;
- model CPU;
- heavy CPU/simulation;
- GPU;
- research/historical;
- publication;
- maintenance.

Physical deployment may initially combine these roles on one host, but contracts must preserve logical separation so scaling does not require redesign.

## A-0.5 Manual-first transition states

A sport workflow progresses through:

1. `MANUAL_UNCERTIFIED`
2. `MANUAL_CERTIFIED`
3. `AUTOMATION_SHADOW`
4. `AUTOMATION_SUPERVISED`
5. `AUTOMATION_PRODUCTION`

Promotion requires explicit certification evidence. TDLA may automate an uncertified workflow for experimentation only when clearly non-authoritative and prevented from production side effects.

---

# A-1 — Ownership and Cross-Repository Authority

## A-1.1 Repository authority matrix

### Daily-Data-Core owns

- generic HTTP transport/retry diagnostics;
- generic provider capability/provenance contracts;
- immutable shared provider raw evidence;
- generic sportsbook acquisition and market mathematics;
- normalized meteorological facts;
- venue/geospatial primitives;
- neutral travel/timezone/rest primitives;
- other explicitly certified sport-agnostic facts.

### Daily-* sport repositories own

- permanent sport-specific identities;
- sport schedule interpretation and event identity mapping;
- sport state and historical PIT semantics;
- sport features;
- training/inference;
- simulation;
- predictions and fair probabilities;
- Recommendation Gate semantics;
- sport-specific readiness conditions;
- required/optional input definitions;
- sport-specific degradation/failure interpretation;
- sport-specific settlement interpretation;
- sport-specific report/content generation.

### TDLA owns

- logical automation plan identity;
- workflow/stage orchestration state;
- trigger/schedule eligibility;
- generic dependency graph execution;
- worker/resource selection;
- generic timeout/retry/idempotency enforcement;
- authoritative automation attempt history;
- immutable execution envelope capture;
- generic alert/incident routing;
- generic publication distribution orchestration;
- operator intervention records;
- automation equivalence/certification evidence.

### Website/app owns

- customer-facing presentation state;
- application/business schema;
- user entitlements/subscriptions;
- content rendering behavior;
- API semantics exposed to product clients.

TDLA integrates through an explicit publication contract and does not reach through boundaries to mutate arbitrary website tables.

## A-1.2 The anti-duplication rule

If TDLA code needs to understand a condition such as `probable_pitcher_confirmed`, `NFL_inactive_list_final`, or `roof_state_relevant_to_model`, the sport adapter must expose an abstract readiness/result contract. TDLA may store the sport-provided reason code but must not calculate the sport meaning itself.

## A-1.3 Cross-repository version references

TDLA execution records may reference:

- sport repository release/version/commit;
- OCI image digest;
- DDC version supplied by the executed sport package;
- sport model identity/version supplied in result metadata;
- publication contract version.

References are evidence; TDLA does not become authority for the internal meaning of those versions.

## A-1.4 Boundary-change governance

Any movement of responsibility between TDLA, DDC, a sport repo, or website/app requires:

1. ADR;
2. update to ownership documentation;
3. compatibility/migration plan;
4. change-journal entry;
5. certification-log update if authority changes.

---

# A-2 — Canonical Automation Domain Model

## A-2.1 Domain entities

The minimum canonical TDLA domain includes:

### `AutomationPlan`
A versioned declaration of intended workflow structure/policy for a scoped unit of sport work.

Key conceptual fields:
- `plan_id`
- `plan_version`
- `plan_digest`
- `sport`
- `scope_type` (`event`, `slate`, `daily`, `seasonal`, `maintenance`, etc.)
- `scope_reference`
- `effective_from`
- `effective_until`
- stages/dependencies
- timing rules
- policy references

### `WorkflowRun`
A logical execution of a plan for a concrete scope.

### `StageRun`
A logical execution of one plan stage.

### `RunAttempt`
A physical attempt to execute a logical run/stage. Retries create attempts without changing the logical identity.

### `TriggerEvent`
A durable fact that may cause plan/run eligibility: time, dependency completion, readiness signal, schedule change, manual action, publication callback, etc.

### `DependencyState`
The current evaluated state of a declared dependency for a logical run.

### `ExecutionEnvelope`
Immutable metadata identifying the exact effective code/config/runtime/input/output environment for an attempt.

### `ArtifactManifest`
Content-addressed description of outputs and required metadata.

### `PublicationRequest`
A request to distribute a validated package through a versioned publication contract.

### `PublicationReceipt`
Durable proof/result of one publication side effect.

### `OperatorAction`
Authenticated human intervention such as approve, reject, cancel, retry, supersede, replay, or reprocess.

### `Incident`
Aggregated operational fault/degradation entity that may affect multiple runs.

## A-2.2 Scope model

TDLA must support work scoped to more than a single game. Valid scope categories include at least:

- event/game;
- slate;
- sport-day;
- league-day;
- batch;
- historical range;
- publication package;
- settlement/evaluation cycle;
- system maintenance.

The sport adapter supplies sport-specific reference identity. TDLA stores that reference without redefining sport ontology.

## A-2.3 Plan immutability

A plan version/digest that has produced production history is immutable. Changes produce a new version/digest. Past runs continue to reference the old plan.

## A-2.4 Required output contract

A successful logical stage must define required outputs. `process_exit_code == 0` cannot alone produce `SUCCEEDED`.

Success evaluation may require:

- artifact manifest exists;
- declared schema version validates;
- required files/records exist;
- checksums match;
- sport adapter declares semantic success;
- required publication receipt exists for publication stages.

## A-2.5 Generic status taxonomy

Initial canonical logical statuses:

- `PLANNED`
- `WAITING`
- `BLOCKED`
- `READY`
- `QUEUED`
- `DISPATCHED`
- `RUNNING`
- `SUCCEEDED`
- `SUCCEEDED_DEGRADED`
- `FAILED_RETRYABLE`
- `RETRY_SCHEDULED`
- `FAILED_TERMINAL`
- `CANCELLED`
- `SUPERSEDED`

Physical attempts separately record attempt-specific states such as queued/started/exited/timed-out/lost.

Status transitions must be explicit, validated, and auditable.

## A-2.6 Degradation is not failure

`SUCCEEDED_DEGRADED` means the sport-defined/plan-defined minimum success contract was satisfied while one or more declared optional capabilities were unavailable or below preferred freshness/quality. The reason and missing capability must be retained.

TDLA does not unilaterally decide that a sport input is optional.

---

# A-3 — Run Identity and Execution Lifecycle

## A-3.1 Identity layers

TDLA separates:

### Logical identity
What operation should conceptually happen once.

### Attempt identity
Which physical execution try performed that logical operation.

### Lineage identity
Relationships between original runs and explicit replay/reprocess/backfill/supersession operations.

This separation is mandatory.

## A-3.2 Logical idempotency key

Logical identity must be deterministic or otherwise uniqueness-enforced from stable canonical fields. The exact algorithm is finalized in A-11, but it must include enough scope to prevent duplicate production effects while permitting intentional replay/reprocess.

Conceptual identity inputs include:

- environment;
- sport;
- plan identity/version;
- scope type/reference;
- stage;
- logical execution/effective time boundary;
- release-policy discriminator where needed.

Mutable prices/provider timestamps must not accidentally change logical identity unless the plan explicitly defines them as a new operation.

## A-3.3 Retry semantics

A transient failure retry:

- preserves logical run identity;
- increments attempt number;
- records retry reason/policy;
- retains every prior attempt;
- must not duplicate prior committed external side effects.

## A-3.4 Replay semantics

Replay is an explicitly requested derivative run intended to reproduce prior behavior from recorded equivalent inputs/releases. It receives a new logical run identity but records `replay_of_run_id` and a replay reason.

Expected properties can include identical artifact hashes where deterministic behavior is promised.

## A-3.5 Reprocess semantics

Reprocess intentionally changes one or more release/model/configuration elements while evaluating an old scope under a preserved historical/PIT boundary. It records lineage to the original run and which dimensions changed.

## A-3.6 Backfill semantics

Backfill executes one or more historical scopes using a declared backfill plan. It is not falsely labeled as original production-time execution and must retain the actual backfill execution time separately from the historical effective time.

## A-3.7 Supersession semantics

When event timing, authoritative schedule identity, configuration, or plan requirements change before execution, pending work may be superseded. Superseded records remain immutable/auditable and identify the replacement run when known.

## A-3.8 Minimum execution envelope

Production attempts must eventually persist at least:

- TDLA logical run ID;
- stage/logical operation ID;
- attempt ID/number;
- parent/lineage IDs;
- environment;
- sport;
- scope type/reference;
- plan ID/version/digest;
- trigger ID/type/reason;
- requested/scheduled/eligible/queued/started/finished timestamps;
- event start and prediction/cutoff timestamps when supplied;
- sport repo/release/commit;
- immutable container/executable digest;
- effective configuration identity/digest;
- worker/execution-backend identity;
- input manifest identity/hashes;
- output manifest identity/hashes;
- terminal status/degradation reason/failure classification;
- operator identity when applicable;
- publication receipts/external idempotency references when applicable.

Secrets must never be embedded in the envelope.

## A-3.9 Lifecycle authority

TDLA's authoritative lifecycle state resides in TDLA persistence, not solely in Prefect. Prefect run IDs and states may be retained as runtime cross-references. If Prefect is replaced, TDLA identity/history remains valid.

---

# A-4 — Configuration and Environment Architecture

## A-4.1 Environments

TDLA recognizes at minimum:

- `development`
- `test`
- `staging`
- `production`

Additional isolated research/shadow environments may be introduced through explicit configuration.

Environment identity is part of run uniqueness and audit context. Production and staging must never accidentally share side-effect destinations solely because a local environment variable was omitted.

## A-4.2 Configuration classes

Configuration is partitioned conceptually into:

### Static repository defaults
Safe defaults committed to Git and versioned with code.

### Environment configuration
Environment-specific non-secret values such as endpoints, resource limits, alert channels, storage namespaces, worker routing, and feature-policy toggles.

### Plan/sport configuration
Versioned configuration supplied or referenced by the sport adapter/automation plan.

### Secrets
Credentials/tokens/keys obtained through a secrets provider and referenced by logical name.

### Runtime overrides
Explicit, authorized one-run overrides captured in the execution envelope and operator audit. Hidden ad-hoc overrides are prohibited.

## A-4.3 Schema validation

All non-trivial effective configuration must validate through typed/versioned schemas before dispatch. Invalid configuration blocks work before executing sport logic.

## A-4.4 Effective configuration digest

TDLA must be able to compute a stable digest over the normalized **non-secret effective configuration** relevant to a logical/physical execution.

The digest must not include raw secret values. Where secret-version awareness is operationally necessary, store a safe secret reference/version identifier supplied by the secrets backend without exposing the secret.

## A-4.5 Precedence

Configuration precedence must be explicit, deterministic, and documented. A tentative order for later implementation is:

1. repository schema defaults;
2. environment configuration;
3. plan/sport configuration;
4. authorized runtime override.

Secrets are resolved independently by logical references and do not override ordinary values implicitly.

## A-4.6 No invisible production behavior

Production-critical behavior must not depend on an undocumented environment variable or workstation-local file. Every supported production variable requires:

- typed contract;
- description;
- safe default or required marker;
- environment ownership;
- documentation;
- change record when changed materially.

## A-4.7 Configuration changes and scheduling

A changed future-effective configuration may generate new/superseding planned work when the plan defines that the change affects logical operation identity. Completed historical runs remain associated with the configuration digest they actually used.

## A-4.8 Secrets policy

Secrets:

- are never committed;
- are never included in public diagnostics;
- are never included in ordinary configuration hashes;
- are resolved as late as reasonably possible;
- use least-privilege service identities;
- require rotation/documented incident response when exposed;
- should support backend replacement through an abstraction.

## A-4.9 Initial infrastructure selection

The current planned implementation baseline is:

- Python 3.12
- Prefect 3 orchestration runtime
- FastAPI control API
- PostgreSQL TDLA authoritative DB
- SQLAlchemy 2 + Alembic
- Pydantic configuration/contracts
- Docker/OCI immutable workloads

This is an implementation choice, not a permanent domain requirement. Technology replacement must preserve the A-0 through A-4 contracts.

---

# Cross-cutting architecture invariants from A-0 through A-4

1. TDLA orchestrates sport logic; it does not absorb sport logic.
2. DDC remains the shared sport-agnostic facts/acquisition layer.
3. Manual certification precedes production automation authority.
4. Logical runs and physical attempts are distinct identities.
5. Retries preserve logical identity; replay/reprocess/backfill are explicit derivative operations.
6. Completed history is never silently rewritten.
7. Plan/config/release identity is versioned and captured.
8. Prefect IDs are cross-references, not TDLA canonical identity.
9. Successful execution requires validated outputs, not only successful process exit.
10. UTC is canonical internally; meaningful source/event timezone context is retained.
11. Secret values never enter Git or ordinary execution manifests.
12. Every material repository change is documented with detailed rationale/evidence/resume information.

---

# A-0 through A-4 certification criteria

These sections may be marked architecture-certified after review confirms:

- ownership is unambiguous enough to prevent implementation duplication;
- domain identities do not depend on Prefect/vendor-specific objects;
- run/attempt/replay/backfill/reprocess distinctions are explicit;
- configuration/secrets boundaries are implementable;
- manual-first production authority is explicit;
- immutable audit requirements are sufficient to constrain implementation;
- documentation/change-memory rules are established;
- no known contradiction exists with certified DDC or sport-repository architecture.

No runtime implementation is required to certify these architecture contracts, but later milestones must produce conformance evidence.

---

# Next architecture checkpoint

**A-5 — Sport Automation Adapter Contract** is next.

A-5 must define the precise provider-neutral interface by which Daily-MLB, Daily-NFL, Daily-NCAAF, and future Daily-* repositories expose planning, readiness, execution, result inspection, artifact, settlement/evaluation, and policy metadata to TDLA without TDLA acquiring sport-specific logic.

Before A-5 is frozen, it should be tested conceptually against at least:

- MLB game-day variable lineup/probable-pitcher timing;
- NFL/NCAAF event-relative injury/inactive/weather refreshes;
- slate-level work;
- rescheduled/postponed events;
- sport workflows that have optional vs required stages;
- manual, shadow, supervised, and production execution modes.
