# AGENTS.md — The Daily Line Automation Operating Constitution

This document governs all human, ChatGPT, Codex, agent, CI, and automation changes to this repository.

## 1. Mission

The-Daily-Line-Automation (TDLA) is the orchestration/control-plane layer for The Daily Line. It coordinates certified sport pipelines and shared infrastructure without absorbing their domain logic.

## 2. Authority boundaries

### TDLA may own
- schedules and event-relative timing;
- triggers and dependency evaluation;
- workflow/stage execution plans;
- dispatch and worker selection;
- timeout/retry/idempotency policy enforcement;
- orchestration state and authoritative TDLA execution audit;
- configuration selection and immutable execution-envelope capture;
- generic resource/concurrency controls;
- observability/alerting/incident coordination;
- publication/distribution coordination;
- operator/manual approval controls;
- replay/backfill/reprocess orchestration;
- automation certification evidence.

### TDLA must not own
- sport-specific canonical player/team/game identity;
- sport-specific state reconstruction;
- sport-specific feature engineering;
- model training/inference logic;
- sport simulation logic;
- fair-price/value/EV reasoning;
- Recommendation Gate semantics;
- sport-specific settlement logic;
- sport-specific interpretation of weather, injuries, travel, lineups, etc.;
- generic shared provider/fact infrastructure already owned by Daily-Data-Core;
- website product/database internals.

When ownership is unclear, stop implementation at the boundary and record the unresolved decision. Do not silently duplicate logic.

## 3. Architecture-first rule

Architecture contracts are written and reviewed before implementation of a new major capability. Implementation must conform to the current certified contract or explicitly version/replace it through an ADR and architecture update.

A temporary prototype may exist only when clearly marked non-authoritative and isolated from production authority.

## 4. Manual-first certification rule

Automation must not become authoritative for a sport workflow until:

1. the equivalent manual pipeline is architecture-certified;
2. its invocation/output contract is stable enough to automate;
3. shadow automation reproduces expected manual behavior;
4. failure/recovery/idempotency tests pass;
5. supervised automation passes defined acceptance evidence;
6. production authority is explicitly recorded in the certification log.

Automation must wrap certified behavior; it must not mask unfinished manual architecture.

## 5. Mandatory change documentation policy

**Every material change must leave a durable human-readable note.**

A material change includes, at minimum:
- source-code changes;
- schema/migration changes;
- contract/model changes;
- architecture changes;
- dependency/version changes;
- CI/CD changes;
- environment/configuration changes;
- secrets/service-identity policy changes;
- worker/deployment changes;
- scheduling/trigger changes;
- provider/resource policy changes;
- observability/alert changes;
- tests or certification-gate changes;
- production/manual procedures;
- data/artifact path or retention changes;
- bug fixes whose cause is non-obvious;
- operational incidents and their corrective actions.

### Required record fields

Each material change must add/update a record containing:

- **Timestamp:** ISO-8601 date/time, preferably UTC; local date may be included.
- **Change ID:** stable identifier when available (commit/PR/milestone/ADR).
- **Area:** architecture, code, schema, config, dependency, deployment, test, incident, documentation, etc.
- **Summary:** exactly what changed.
- **Reason:** why the change was necessary.
- **Files/components affected:** paths/services/contracts.
- **Authority/contract impact:** whether architecture or ownership changed.
- **Data/migration impact:** schemas, persisted state, artifacts, compatibility.
- **Operational impact:** scheduling, retries, deployment, monitoring, publication, manual steps.
- **Validation/evidence:** tests, commands, audits, comparisons, screenshots/logs/artifact hashes where applicable.
- **Risks/open questions:** known limitations or unresolved points.
- **Rollback/recovery note:** when relevant.
- **Next exact step:** concrete continuation point.

Do not write vague entries such as "updated automation" or "fixed tests." A future maintainer must be able to reconstruct the decision and resume work without rediscovering the same information.

### Where records go

- Chronological material-change record: `docs/implementation/CHANGE_JOURNAL.md`.
- Current single authoritative continuation point: `docs/implementation/CURRENT_RESUME_POINT.md`.
- Architecture/milestone authority status: `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`.
- Durable architecture decisions/tradeoffs: `docs/adr/ADR-*.md`.
- Checkpoint-specific running work may receive its own progress log, but it must be linked from `CURRENT_RESUME_POINT.md` and may not silently override the certification log.

### Documentation timing

Documentation is part of the change, not optional cleanup. Update it in the same logical work unit whenever practical. If implementation and documentation are split across commits, the work is not considered complete until the documentation commit lands.

## 6. Resume-point discipline

At the end of every meaningful work session/checkpoint:

1. update `CHANGE_JOURNAL.md`;
2. update `CURRENT_RESUME_POINT.md` with the exact next task;
3. update certification status if authority changed;
4. link any new ADR, audit, validation report, or progress log;
5. record blocking conditions and the evidence needed to clear them.

Never require the next session to infer status from Git history or chat history.

## 7. Immutable execution and provenance rules

Production TDLA runs must eventually retain sufficient evidence to identify:
- logical run identity;
- attempt identity;
- parent/replay/reprocess lineage;
- sport/event/slate identity supplied by the sport contract;
- workflow/stage/plan version and digest;
- requested/scheduled/started/finished timestamps;
- event start and prediction/cutoff times when applicable;
- repository release/commit and immutable execution image digest;
- Daily-Data-Core release used by the sport runtime where applicable;
- model/configuration identities supplied by the sport runtime;
- input/output manifests and hashes;
- worker/executor identity;
- trigger and operator identity;
- status/degradation/failure classification;
- publication receipts and external side-effect identities.

TDLA must not silently mutate completed execution evidence.

## 8. Idempotency rule

Retries are new attempts of the same logical operation unless an explicit replay/reprocess is requested. External side effects must use stable idempotency identities wherever supported. Duplicate publication, duplicate notification, or duplicate persisted business effect caused by retry behavior is a production defect.

## 9. Replay / backfill / reprocess terminology

- **Replay:** repeat a prior logical production run from recorded equivalent inputs/releases to verify reproducibility.
- **Backfill:** execute a historical range using the historical/PIT workflow intended for that purpose.
- **Reprocess:** intentionally evaluate an old event with changed code/model/configuration while preserving historical cutoff semantics.

These terms must not be used interchangeably in code, docs, tables, APIs, or UI.

## 10. Time semantics

- Canonical internal timestamps: UTC.
- Retain meaningful IANA timezone identifiers for leagues/events/operator presentation.
- Never compare naive datetimes in production domain logic.
- Event-relative plans must be recalculable when authoritative event times change.
- Superseded planned work remains auditable rather than deleted.

## 11. Configuration rule

Configuration is versioned input, not invisible environment magic. Non-secret production-effective configuration should be schema-validated and hashable. Secrets are referenced by stable logical names but their secret values must never enter Git, logs, manifests, hashes intended for public diagnostics, or execution records.

## 12. Dependency/release rule

Production consumers/executors must use immutable releases/digests. Do not run production by `git pull` of a moving branch or by relying on a mutable container `latest` tag.

## 13. Quality gates

The intended engineering baseline is Python 3.12 with:
- pytest;
- Ruff;
- strict mypy;
- reproducible dependency locks;
- migration validation;
- contract tests;
- failure/retry/idempotency tests;
- replay tests;
- integration tests;
- end-to-end automation equivalence tests for sport onboarding.

Milestone-specific gates may add requirements but must not silently weaken already-certified gates.

## 14. Database and migration discipline

- PostgreSQL is planned as authoritative TDLA production persistence.
- Schema changes require explicit versioned migrations.
- Never edit previously-applied migration meaning in place.
- Migrations require forward validation and a documented recovery/rollback strategy appropriate to the change.
- Operational history tables must preserve append-only/immutable semantics where defined by architecture.

## 15. Orchestration-engine abstraction

Prefect 3 is the planned initial orchestration runtime. TDLA domain identity, execution audit, contracts, and business state must not become Prefect-specific. Prefect IDs may be cross-references, not permanent TDLA identity authority.

## 16. Worker/executor abstraction

Execution backends must be replaceable. Initial local/Docker execution may later expand to dedicated CPU, heavy-CPU, GPU, research, publication, or Kubernetes workers without changing canonical TDLA workflow identity.

## 17. Security

- Never commit `.env`, tokens, passwords, API keys, private certificates, or provider secrets.
- Sanitize exception/log output.
- Use least-privilege service identities.
- Production publication/destructive/operator actions must be authenticated and auditable.
- Any credential exposure requires a documented incident note and credential rotation.

## 18. Agent execution hierarchy

Default execution preference:

1. make scoped repository changes directly when the available tooling safely supports them;
2. ask the user to run exact local commands only when local runtime/state is required;
3. reserve Codex or other long-running execution agents for explicitly scoped work that benefits from them.

Agents must read this file and the current resume point before making changes.

## 19. Before beginning work

Read, in order:
1. `README.md`
2. `AGENTS.md`
3. `docs/implementation/CURRENT_RESUME_POINT.md`
4. `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`
5. relevant architecture/ADR/progress documents.

## 20. Definition of done

A change is not done merely because code runs. It is done when applicable:
- implementation matches the governing contract;
- tests/quality gates pass;
- migrations/contracts are validated;
- operational/recovery behavior is understood;
- documentation/change journal is current;
- resume point is current;
- certification status is updated when warranted;
- no unresolved ownership ambiguity was hidden.
