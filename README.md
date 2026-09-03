# The Daily Line Automation

The Daily Line Automation is the production orchestration and operations platform for **The Daily Line** multi-sport prediction ecosystem.

It does **not** own sport intelligence and it does **not** replace Daily-Data-Core. Its responsibility is to determine what work should run, when it should run, what dependencies and policies apply, which immutable release executes, what happened during execution, whether required outputs were produced, what should happen next, and how approved artifacts are distributed.

## System ownership model

- **Daily-Data-Core (DDC)** owns sport-agnostic shared acquisition/facts and generic provider/provenance infrastructure.
- **Daily-MLB, Daily-NFL, Daily-NCAAF, and future Daily-* repositories** own sport-specific identity, state, features, models, simulation, prediction, recommendation, settlement interpretation, and sport-specific report content.
- **The-Daily-Line-Automation (TDLA)** owns orchestration, scheduling, trigger evaluation, execution lifecycle, retries, idempotency, operational audit, worker/resource coordination, publication coordination, and operator-facing automation state.
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

## Current status

- Repository created and architecture-first policy established.
- A-0 through A-4 architecture foundation: **DOCUMENTED — certification pending implementation-independent review**.
- A-5 Sport Automation Adapter contract: **NEXT**.
- No production automation implementation is authoritative yet.
- Daily-MLB remains manual-first until its production pipeline is certified and later proves automation equivalence in shadow/supervised modes.

## Governing documents

- `AGENTS.md` — repository operating constitution and mandatory documentation/change-record rules.
- `docs/architecture/README.md` — architecture index and status.
- `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md` — A-0 through A-4 architecture contract.
- `docs/implementation/IMPLEMENTATION_ROADMAP_V1.md` — milestone implementation/certification sequence.
- `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md` — authoritative architecture/milestone status.
- `docs/implementation/CHANGE_JOURNAL.md` — chronological durable change record and resume history.
- `docs/implementation/CURRENT_RESUME_POINT.md` — exact current continuation point.
- `docs/adr/README.md` — Architecture Decision Record policy/index.

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

These technology choices remain subordinate to TDLA's own contracts. Prefect, databases, deployment backends, or telemetry vendors must be replaceable without invalidating TDLA execution identity or audit history.

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
