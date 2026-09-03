# ADR-0001 — TDLA Control Plane Owns Canonical Identity; Orchestrator Runtime Is Replaceable

Date: 2026-09-02  
Status: **ACCEPTED as foundation direction; subject to A-0 through A-4 certification review**

## Context

The Daily Line needs durable multi-sport orchestration for Daily-MLB, Daily-NFL, Daily-NCAAF, and future sports. A workflow runtime such as Prefect provides valuable execution, scheduling, retry, and operational capabilities, but making vendor-native flow/run IDs the permanent business identity would couple historical audit and recovery to one orchestration product.

The platform also needs to answer long-lived questions after infrastructure changes: exactly what logical operation ran, which physical attempt executed it, which release/configuration/input/output artifacts were used, what triggered it, whether it was retried/replayed/reprocessed/backfilled, and which publication side effects occurred.

## Decision

1. **The-Daily-Line-Automation (TDLA) is the canonical automation control-plane domain.**
2. TDLA defines and persists its own logical plan/run/stage/attempt/trigger/operator/publication identities and lifecycle history.
3. **Prefect 3 is the intended initial orchestration runtime**, selected for Python-native workflow orchestration and operational capabilities.
4. Prefect flow/deployment/run/task IDs may be stored as execution-runtime cross-references but are not canonical TDLA identity.
5. TDLA persistence—not Prefect's internal database alone—is the authoritative long-lived business/audit record for TDLA execution state.
6. A later migration to another orchestrator must be possible without renumbering/redefining historical TDLA runs or losing their lineage.
7. Runtime-specific status must be translated into TDLA's canonical lifecycle rather than leaking vendor state throughout sport adapters and product integrations.

## Alternatives considered

### Alternative A — Make Prefect the full system of record

Advantages:
- lower initial implementation effort;
- less duplicate persistence/state machinery;
- built-in UI/state model can be used directly.

Rejected because:
- vendor state becomes permanent business identity;
- historical audit semantics become constrained by runtime implementation details;
- future runtime migration becomes a data/identity migration rather than an execution-backend migration;
- TDLA needs domain concepts such as replay vs reprocess vs backfill, publication receipts, sport plan versions, and automation certification states that should remain product-owned.

### Alternative B — Use only cron / GitHub Actions schedules

Advantages:
- extremely simple bootstrap;
- minimal infrastructure.

Rejected because:
- weak event-relative scheduling and dependency semantics;
- poor durable state/recovery model;
- retries and duplicate side effects become difficult to govern;
- inadequate for multi-sport resource/deadline coordination and operator workflows.

### Alternative C — Build a fully custom orchestrator immediately

Advantages:
- complete control;
- no external runtime dependency.

Rejected because:
- unnecessary recreation of mature execution/scheduling functionality;
- larger correctness and operations burden;
- distracts from TDL-specific domain contracts.

TDLA should own the domain/control contract while delegating generic workflow execution machinery to a replaceable runtime.

## Consequences

### Positive

- long-lived audit/replay identity is under TDL control;
- Prefect can evolve or be replaced independently;
- sport adapters integrate with stable TDLA contracts;
- operator/product APIs do not depend directly on Prefect object models;
- history can preserve domain semantics richer than runtime-native state.

### Costs

- TDLA must maintain a persistence/state synchronization layer;
- runtime reconciliation is required after crashes/network partitions;
- developers must understand canonical vs runtime identity;
- tests must verify mapping and recovery behavior.

These costs are accepted because automation history and production reproducibility are core platform requirements.

## Compatibility / migration impact

No existing TDLA production system exists, so there is no migration cost at adoption time.

Future orchestration-runtime replacement must:
- preserve TDLA primary IDs;
- preserve existing execution envelopes/history;
- add new runtime cross-reference types rather than mutating old records;
- prove state/retry/recovery equivalence before production cutover.

## Security / operational impact

TDLA's own control API/database becomes security-sensitive because it contains authoritative execution/operator/publication state. Service identity, least privilege, audit logging, backup/recovery, and environment isolation must be designed in later architecture sections.

## Validation required

During A-0 through A-4 review and later M3 implementation, prove that:

- no canonical TDLA key requires a Prefect ID;
- a TDLA run can be reconstructed from TDLA state plus referenced immutable artifacts;
- runtime state reconciliation does not silently overwrite immutable TDLA history;
- replacing/mocking the Prefect integration does not change sport adapter contracts.

## Related architecture

- A-0 Mission / replaceable infrastructure
- A-2 Canonical automation domain
- A-3 Run identity and lifecycle
- future A-10 Worker/execution architecture
- future A-13 Persistence/audit/provenance
- future A-21 Deployment/recovery

## Supersession

Supersedes: none.  
Superseded by: none.
