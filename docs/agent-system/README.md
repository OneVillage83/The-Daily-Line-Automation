# Daily Line Agent Development System

Status: **DL-AGENT-0 baseline**  
Established: 2026-09-15  
Home repository: `OneVillage83/The-Daily-Line-Automation`

## Purpose

The Daily Line Agent Development System (DLADS) is the cross-repository engineering control layer for continuing The Daily Line as a long-horizon production program with Codex today and reusable OpenAI agents later.

It solves one specific problem: a future session must be able to receive a short instruction such as **"Continue Daily Line development"** and determine the correct next bounded task from durable repository state instead of reconstructing months of chat history.

DLADS does **not** transfer domain authority into this repository. Each sport, shared core, website, and automation repository remains authoritative for its own contracts and implementation.

## Operating model

```text
User / scheduled development task
              |
              v
     Daily Line Supervisor
              |
       program state + roadmap
              |
    +---------+----------+----------+----------+
    v         v          v          v          v
Engineering Modeling  QA/Audit Documentation Validation/CI
    |         |          |          |          |
    +---------+----------+----------+----------+
              |
              v
     target repository Codex work
              |
              v
 local AGENTS.md / CODEX_START_HERE / repo docs
              |
              v
 implementation -> focused proof -> audit -> docs -> handoff
              |
              v
      program state updated
```

## Source-of-truth precedence

For development decisions, use this order:

1. explicit current user instruction;
2. target repository `AGENTS.md` / `AGENTS.override.md`;
3. target repository exact resume/status/certification documents;
4. immutable Git/PR/CI evidence;
5. `docs/agent-system/ACTIVE_EXECUTION_PLAN.md` and machine-readable program state;
6. `PROGRAM_ROADMAP.md`;
7. old chat summaries or memory.

If program state conflicts with target-repository truth, **the repository wins** and the supervisor must repair program state before continuing.

## Standard command

When the user says **"Continue Daily Line development"**, the supervisor must:

1. read this index, the active execution plan, repository registry, and program state;
2. inspect the candidate target repository's current default-branch head and local continuation documents;
3. reconcile stale status before selecting work;
4. choose the highest-priority unblocked task consistent with the roadmap and repository authority;
5. delegate bounded work to the appropriate specialist role;
6. run focused validation needed to answer engineering questions;
7. invoke QA/Audit before claiming completion;
8. hand long deterministic/exhaustive validation to Validation/CI when appropriate;
9. update target-repository documentation and exact resume point;
10. update DLADS program state and active plan when program-level status changed.

## Macro build order

The governing program sequence is:

```text
Data authority / shared contracts
        -> MLB / NFL / NCAAF production sport pipelines
        -> Daily-Model-Core reusable model families
        -> sport model integration
        -> calibration
        -> learned ensemble / Unified Line
        -> market intelligence and market comparison
        -> recommendation/report/publication outputs
        -> website product integration
        -> automation
        -> social/video automation
        -> One Village Command integration
```

Do not jump to a later phase merely because it is easier or more visible.

## Codex vs runtime agents

- **Codex** remains the primary engineering implementer. Repository-local `AGENTS.md` and Codex skills govern how work is performed.
- **DLADS agent manifests** define roles, capability boundaries, evaluation requirements, and future runtime mapping.
- **OpenAI Agents API publication is not yet active.** No provider agent IDs or API credentials are stored here.
- Runtime publication must remain provider-neutral and must not create a second source of project truth outside Git.

## Key files

- `ACTIVE_EXECUTION_PLAN.md` — exact program-level continuation point.
- `PROGRAM_ROADMAP.md` — full ordered development plan.
- `REPOSITORY_REGISTRY.md` — ownership and start documents for every repository.
- `WORKFLOW.md` — supervisor state machine and cross-repo rules.
- `AGENT_ROLES.md` — specialist responsibilities and handoffs.
- `EVALUATION_GATES.md` — minimum proof before promotion/completion.
- `HANDOFF_CONTRACT.md` — required bounded-work handoff format.
- `OPENAI_RUNTIME_ADAPTER.md` — future Agents API / Skills publication mapping.
- `state/program_state.json` — machine-readable program state.
- `schemas/` — contracts for state and agent manifests.
- `/agents/` — version-controlled specialist definitions.
- `/codex/skills/` — reusable Codex workflows.

## Safety rule

No development agent may silently widen scientific, production, publication, financial, or destructive authority. An engineering implementation can propose such a change, but activation requires the target repository's existing governance and owner approval rules.