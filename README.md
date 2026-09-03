# The Daily Line Automation

The Daily Line Automation is the production orchestration and operations platform for **The Daily Line** multi-sport prediction ecosystem.

It does **not** own sport intelligence and it does **not** replace Daily-Data-Core. Its responsibility is to determine what work should run, when it should run, what dependencies and policies apply, which immutable release executes, what happened during execution, whether required outputs were produced, what should happen next, and how approved artifacts are distributed.

## System ownership model

- **Daily-Data-Core (DDC)** owns sport-agnostic shared acquisition/facts and generic provider/provenance infrastructure.
- **Daily-MLB, Daily-NFL, Daily-NCAAF, and future Daily-* repositories** own sport-specific identity, state, features, models, simulation, prediction, recommendation, settlement interpretation, and sport-specific report content.
- **The-Daily-Line-Automation (TDLA)** owns the **outer automation/orchestration lifecycle**: planning, scheduling, trigger evaluation, workflow/stage state, worker dispatch, retries, idempotency, operational audit, publication coordination, and operator-facing automation state.
- **Sport services and DDC may retain nested child job/acquisition lifecycles** under their own certified contracts. TDLA links those identities through provenance rather than replacing them.
- **The Daily Line website/app** owns presentation/product state and receives publication packages through explicit versioned contracts rather than direct automation writes into application tables.

## Non-negotiable architecture rules

1. The automation platform may coordinate sport intelligence but may never reimplement sport intelligence.
2. Automation may not become authoritative for a workflow until the equivalent manual workflow is certified and automation equivalence has been demonstrated.
3. A process exit code of zero is not sufficient evidence of success; required validated versioned output contracts must exist.
4. Completed execution history is immutable. Rescheduled, superseded, retried, cancelled, replayed, or reprocessed work remains traceable.
5. Production execution must identify immutable code/model/configuration/dependency artifacts rather than moving branches or mutable `latest` tags.
6. Retries must be idempotent at the logical-operation level; duplicate user-visible side effects are defects.
7. Backfill, replay, and reprocess are distinct operations and must remain separately identifiable.
8. UTC is the canonical internal time basis; source/event IANA timezone context must be retained where meaningful.
9. Sport repositories declare sport-specific readiness, required/optional inputs, failure/degradation policies, and event-relative stage plans. Automation enforces those contracts without inventing sports meaning.
10. Every material repository change must create or update durable documentation explaining what changed, why, validation performed, architecture/operational impact, and the exact resume point.
11. TDLA canonical identity is independent of Prefect or any future orchestration runtime.
12. TDLA outer run/attempt identity must never silently replace child sport-job, DDC-acquisition, or provider-attempt identity.
13. The Sport Automation Adapter is a versioned **transport-neutral protocol boundary**; TDLA does not canonically import sport-domain packages or depend on HTTP/Prefect semantics.
14. Retry `attempt_id` is not child deduplication identity. The stable logical idempotency identity remains constant across attempts of the same logical operation.
15. Adapter capability support does not grant production authorization; certification/environment/plan/release/side-effect policy must all permit the operation.
16. Unknown async child state or lost acknowledgement is not permission for blind redispatch.
17. V1 automation plans are declarative DAGs; repeated readiness checks/retries/rescheduling are evaluations/attempts, not graph cycles.
18. Sport and TDLA platform stages remain in immutable separately owned plan fragments; cross-fragment connections use explicit typed bindings and conflicts fail closed.
19. The immutable `ResolvedAutomationPlan` is canonical executable plan authority; runtime flow objects are implementation cross-references only.
20. Dynamic fan-out membership remains sport-owned and revision/digest-bound; TDLA cannot infer game membership from names, dates, or provider IDs.
21. Stage definitions, stage materializations, logical StageRuns, and physical RunAttempts are distinct identity layers.
22. `OPTIONAL`, `NO_OP`, `NOT_APPLICABLE`, and degraded outcomes satisfy only dependency/output contracts that explicitly permit them.
23. Production resolved plans pin immutable execution targets and execution-affecting policy versions/digests.
24. Plan identity is deterministic from schema-controlled semantic canonicalization and SHA-256; presentation-only metadata does not silently alter execution identity.

## Current status

- Repository created and architecture-first policy established.
- A-0 through A-4 architecture foundation: **ARCHITECTURE-CERTIFIED**.
- A-5 Sport Automation Adapter contract: **ARCHITECTURE-CERTIFIED**.
- A-6 Pipeline Plan / Stage Contracts: **ARCHITECTURE-CERTIFIED**.
- A-6 certification evidence: `docs/implementation/A06_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md`.
- A-7 Trigger Architecture: **NEXT**.
- No production automation implementation is authoritative yet.
- Daily-MLB remains manual-first until its production pipeline is certified and later proves automation equivalence in shadow/supervised modes.
- The existing Daily-MLB starter job-service shape is compatible in principle with A-5/A-6 wrapping, but it is not assumed production-conforming; future onboarding targets the certified final manual MLB pipeline and must prove stable idempotent async dispatch/reconciliation plus A-6 plan/output contracts.

## Governing documents

- `AGENTS.md` — repository operating constitution and mandatory documentation/change-record rules.
- `docs/architecture/README.md` — architecture index and status.
- `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md` — A-0 through A-4 base architecture contract.
- `docs/architecture/A00-A04_FOUNDATION_ADDENDUM_V1_1.md` — certified nested lifecycle/cross-repository clarification.
- `docs/implementation/A00-A04_ARCHITECTURE_CONFORMANCE_REVIEW_20260902.md` — A-0 through A-4 certification review/evidence.
- `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_V1.md` — A-5 base adapter architecture.
- `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md` — A-5 certification clarifications.
- `docs/implementation/A05_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md` — A-5 certification review/evidence.
- `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md` — A-6 base plan/stage graph architecture.
- `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md` — A-6 certification clarifications for scope-set binding, digest participation, schedule-slot identity, and immutable policy binding.
- `docs/implementation/A06_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md` — A-6 certification review/evidence and 30-case stress matrix.
- `docs/implementation/IMPLEMENTATION_ROADMAP_V1.md` — milestone implementation/certification sequence.
- `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md` — authoritative architecture/milestone status.
- `docs/implementation/CHANGE_JOURNAL.md` — chronological durable change record and resume history.
- `docs/implementation/CURRENT_RESUME_POINT.md` — exact current continuation point.
- `docs/adr/README.md` — Architecture Decision Record policy/index.
- `docs/adr/ADR-0001_CONTROL_PLANE_AND_VENDOR_NEUTRAL_IDENTITY.md` — TDLA canonical identity / replaceable orchestrator decision.
- `docs/adr/ADR-0002_TRANSPORT_NEUTRAL_SPORT_ADAPTER_PROTOCOL.md` — transport-neutral sport adapter protocol decision.
- `docs/adr/ADR-0003_IMMUTABLE_PLAN_FRAGMENTS_AND_EXPLICIT_COMPOSITION.md` — immutable fragment, explicit composition, resolved-plan authority decision.

## Planned technical baseline

The initial intended production baseline is:

- Python 3.12
- Prefect 3 as the orchestration runtime behind TDLA-owned contracts
- FastAPI control/operations API
- PostgreSQL authoritative TDLA persistence
- SQLAlchemy 2 + Alembic
- Pydantic contracts
- OCI/Docker immutable execution artifacts
- object-storage abstraction for generated artifacts
- OpenTelemetry-compatible tracing
- Prometheus-compatible metrics and Grafana-compatible dashboards
- JSON structured logging
- GitHub Actions CI/CD
- pytest, Ruff, and strict mypy

These technology choices remain subordinate to TDLA's own contracts. Prefect, databases, deployment backends, transport mechanisms, or telemetry vendors must be replaceable without invalidating TDLA execution identity or audit history.

## Architecture sequence

The architecture is planned as A-0 through A-24:

- A-0 Mission, principles, and system boundary
- A-1 Ownership and cross-repository authority
- A-2 Canonical automation domain model
- A-3 Run identity and execution lifecycle
- A-4 Configuration and environment model
- A-5 Sport Automation Adapter contract
- A-6 Pipeline-plan and stage contracts
- A-7 Trigger architecture
- A-8 Event-relative scheduling engine
- A-9 Dependency/readiness engine
- A-10 Worker and execution-backend architecture
- A-11 Retry, timeout, and idempotency architecture
- A-12 Failure, degradation, and recovery model
- A-13 Persistence, immutable audit, and provenance
- A-14 Artifact, replay, backfill, and reprocess architecture
- A-15 Resource/concurrency/provider budgeting
- A-16 Observability, tracing, and metrics
- A-17 Alerting and incident architecture
- A-18 Publication/distribution architecture
- A-19 Human approval and operator controls
- A-20 Security, secrets, and service identity
- A-21 Deployment, high availability, backup, and disaster recovery
- A-22 CI/CD and immutable release execution
- A-23 Multi-sport scaling and isolation
- A-24 Future adaptive/intelligent automation extensions

## Documentation rule

Git history is useful but is **not** the only project memory. Any material change must leave a human-readable durable note. See `AGENTS.md` and `docs/implementation/CHANGE_JOURNAL.md` for the exact required record format.
