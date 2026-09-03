# The Daily Line Automation — Implementation Roadmap V1

Initial date: 2026-09-02  
Status: planning authority for implementation sequencing; architecture contracts remain authoritative for behavior.

## Purpose

This roadmap defines the intended milestone sequence after A-0 through A-24 architecture is sufficiently frozen. Milestones are certification checkpoints, not vague phases.

A milestone is complete only when its implementation, tests, local/hosted validation as applicable, architecture-conformance audit, documentation, and certification log entry are complete.

## Milestone sequence

### M0 — Repository Bootstrap / Engineering Constitution

Scope:
- repository structure;
- Python 3.12 baseline;
- dependency input/lock policy;
- pytest/Ruff/strict-mypy baseline;
- `AGENTS.md` enforcement expectations;
- documentation/change-journal/resume-point discipline;
- architecture/ADR/implementation/runbook directory conventions;
- safe `.gitignore` / secret exclusions;
- CI skeleton.

Exit evidence:
- clean bootstrap from documented instructions;
- quality gates execute;
- no secret-bearing defaults;
- change-documentation policy demonstrated by M0 itself.

### M1 — Canonical Automation Domain Contracts

Scope:
- typed plan/run/stage/attempt/trigger/dependency/operator/publication/artifact/incident contracts;
- canonical enums and versioning;
- state-transition validation;
- serialization compatibility tests.

### M2 — PostgreSQL Persistence & Migration Foundation

Scope:
- SQLAlchemy 2 persistence;
- Alembic migrations;
- database bootstrap/check tooling;
- immutable/append-only history constraints where required;
- schema version authority;
- backup/recovery/migration test policy.

### M3 — Prefect Runtime Foundation

Scope:
- Prefect integration behind TDLA abstractions;
- TDLA IDs mapped to Prefect references;
- orchestration runtime configuration;
- local/development deployment;
- proof that canonical run history remains TDLA-owned.

### M4 — Scheduling / Trigger Engine

Scope:
- exact/recurring/event-relative time triggers;
- dependency triggers;
- manual triggers;
- schedule-change/supersession handling;
- trigger deduplication.

### M5 — Worker / Execution Backend

Scope:
- execution-backend interface;
- local + Docker implementation;
- worker classes/resource routing;
- immutable executable/container digest capture;
- process timeout/cancellation/lost-worker behavior.

### M6 — Sport Automation Adapter Framework

Scope:
- A-5/A-6 interfaces;
- adapter registration/version compatibility;
- readiness/plan/result/artifact contracts;
- sport-neutral test adapter;
- explicit guardrails preventing sport logic inside TDLA.

### M7 — Idempotency / Retry / Recovery

Scope:
- logical idempotency keys;
- attempt numbering;
- retry policy engine;
- duplicate-trigger handling;
- restart reconciliation;
- external side-effect idempotency abstraction;
- failure-injection tests.

### M8 — Provenance / Immutable Run Ledger

Scope:
- execution envelope;
- plan/config/release/input/output hashes;
- operator/trigger lineage;
- append-only lifecycle history;
- provenance query API.

### M9 — Artifact / Replay / Backfill / Reprocess

Scope:
- artifact manifests;
- object-storage abstraction;
- replay lineage and deterministic checks;
- backfill planning;
- reprocess comparison metadata;
- retention policy hooks.

### M10 — Observability / Alerts / Incidents

Scope:
- structured logs;
- traces;
- metrics;
- alert severity/deduplication;
- incident aggregation;
- operational dashboards/health endpoints.

### M11 — Publication Subsystem

Scope:
- versioned publication request/receipt contract;
- destination adapters;
- idempotent publication;
- partial publication failure/retry;
- pre-publication validation;
- no direct writes into arbitrary website internals.

### M12 — Security / Service Identity

Scope:
- secrets abstraction;
- service identity and least privilege;
- operator authentication/authorization;
- audit logs;
- credential safety tests;
- production environment separation.

### M13 — Daily-MLB Adapter

Prerequisite: certified Daily-MLB manual production interface.

Scope:
- wrap certified Daily-MLB pipeline;
- no MLB intelligence copied into TDLA;
- plan/readiness/result integration;
- event/slate mapping;
- artifact/publication integration.

### M14 — Daily-MLB Shadow Automation

Scope:
- run automation without production authority/side effects;
- compare against manual execution;
- prove scheduling/readiness/result equivalence;
- collect failure/recovery evidence.

### M15 — Daily-MLB Production Automation Certification

Scope:
- supervised mode;
- publication safety;
- restart/failure/provider-degradation drills;
- production acceptance criteria;
- explicit authority promotion to `AUTOMATION_PRODUCTION`.

### M16 — Daily-NFL Integration

Scope:
- integrate certified NFL workflow;
- prove adapter architecture accommodates different timing/readiness structure without generic sport branches.

### M17 — Daily-NCAAF Integration

Scope:
- integrate certified NCAAF workflow;
- stress event volume and Saturday slate behavior;
- validate multi-league/multi-sport resource planning.

### M18 — Multi-Sport Concurrency / Resource Governance

Scope:
- resource pools;
- sport isolation;
- provider budgets;
- priority/deadline policy;
- overload/backpressure behavior;
- no starvation of time-critical final prediction/publication stages.

### M19 — Production HA / Backup / Disaster Recovery

Scope:
- control-plane failure recovery;
- PostgreSQL backup/restore;
- object artifact recovery;
- orchestration runtime recovery;
- worker loss;
- restore drills and RPO/RTO targets.

### M20 — TDL Operations Dashboard

Scope:
- sport/slate/run health;
- blocked/readiness states;
- incidents;
- publication status;
- operator actions;
- audit/provenance drill-down.

## Milestone certification template

Each milestone should produce, where applicable:

- `M##_ARCHITECTURE_CONFORMANCE_AUDIT.md`
- `M##_LOCAL_VALIDATION_YYYYMMDD.md`
- optional hosted/staging validation evidence;
- checkpoint-specific progress log during long-running work;
- `CHANGE_JOURNAL.md` entries for material changes;
- updated `CURRENT_RESUME_POINT.md`;
- final status in `ARCHITECTURE_CERTIFICATION_LOG.md`.

## Status rules

Allowed high-level status language:
- `PLANNED`
- `IN PROGRESS`
- `BLOCKED`
- `IMPLEMENTED — CERTIFICATION PENDING`
- `ARCHITECTURE-CERTIFIED`
- `SUPERSEDED`

Do not label a milestone certified solely because tests pass.

## Current implementation position

No implementation milestone is currently certified. The project is still in architecture definition. A-5 is the next architecture checkpoint after the A-0 through A-4 foundation review.
