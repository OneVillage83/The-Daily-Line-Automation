# Daily Line Agent Development System

Status: **DL-AGENT-0 baseline**  
Established: 2026-09-15  
Home repository: `OneVillage83/The-Daily-Line-Automation`

## Purpose

The Daily Line Agent Development System (DLADS) is the cross-repository **Codex supervision and continuity layer** for The Daily Line.

It solves one specific problem: a future session must be able to receive a short instruction such as **"Continue Daily Line development"**, determine the correct next bounded task from durable repository state, supervise Codex's output, and prepare the next precise Codex instruction without reconstructing months of chat history.

DLADS does **not** transfer domain authority into this repository. Each sport, shared core, website, and automation repository remains authoritative for its own contracts and implementation.

## Non-negotiable coding rule

> **Codex is the sole code-changing executor.**

DLADS bots/agents do not implement code. They may inspect, summarize, monitor, review, classify, update coordination state, and draft the next Codex prompt. They must not edit source code, tests, migrations, model code, or production configuration.

ChatGPT Pro remains the primary high-reasoning reviewer/architect. Grok Bot or another inexpensive persistent bot may act as a liaison/monitor, but not as a programmer.

See [`CODEX_SUPERVISION_LOOP.md`](CODEX_SUPERVISION_LOOP.md).

## Operating model

```text
User / program goal
        |
        v
ChatGPT Pro / Daily Line Supervisor
        |
        | precise bounded prompt
        v
      CODEX
   sole coding executor
        |
        | code + tests + repo-local handoff
        v
  Codex handoff/result
        |
        v
Liaison / QA / Monitor bots
  - summarize
  - compare to plan
  - monitor checks
  - classify next step
  - draft next Codex prompt
  - never edit code
        |
        +---- mechanical continuation ----> next Codex prompt
        |
        +---- architecture/science issue --> ChatGPT Pro review
        |
        +---- owner decision --------------> user
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
5. create the exact bounded Codex prompt;
6. send/queue the coding task to Codex;
7. consume Codex's handoff and compare it to the assignment;
8. classify the result as `SAFE_CONTINUE`, `REVIEW_REQUIRED`, `OWNER_DECISION_REQUIRED`, or `BLOCKED`;
9. use ChatGPT Pro for architecture/science/ambiguous review when needed;
10. draft the next Codex prompt or exact stop condition;
11. update DLADS coordination state after repo-local evidence exists.

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

## Codex vs supervisory bots

- **Codex:** all source/test/migration/model/config code changes and focused engineering proof.
- **ChatGPT Pro:** primary architecture/reasoning reviewer and prompt author for difficult or consequential decisions.
- **Grok Bot / other liaison bot:** optional persistent monitoring, handoff summarization, repo-state reconciliation, CI watching, and next-prompt drafting.
- **DLADS manifests:** define non-coding supervisory roles and future runtime mapping.
- **OpenAI Agents API publication is not required to use DLADS.** Runtime publication remains optional and provider-neutral.

## Key files

- `CODEX_SUPERVISION_LOOP.md` — exact Codex-only coding and handoff model.
- `ACTIVE_EXECUTION_PLAN.md` — exact program-level continuation point.
- `PROGRAM_ROADMAP.md` — full ordered development plan.
- `REPOSITORY_REGISTRY.md` — ownership and start documents for every repository.
- `WORKFLOW.md` — supervisor state machine and cross-repo rules.
- `AGENT_ROLES.md` — non-coding supervisory/liaison responsibilities.
- `EVALUATION_GATES.md` — minimum proof before stronger status claims.
- `HANDOFF_CONTRACT.md` — required bounded-work handoff format.
- `MULTI_PROVIDER_EXECUTION_STRATEGY.md` — subscription/API/provider allocation.
- `OPENAI_RUNTIME_ADAPTER.md` — optional future API mapping.
- `state/program_state.json` — machine-readable program state.
- `/agents/` — version-controlled non-coding supervisory definitions.
- `/codex/skills/` — reusable Codex workflows.

## Safety rule

No supervisory bot may silently widen scientific, production, publication, financial, or destructive authority. If a bot discovers a needed implementation change, it must produce a Codex prompt or escalation—not a code patch.

## Sport build boundary pack

Before creating/registering a new sport repository or directing Bridge/Codex work that expands sport scope, read:

1. `docs/agent-system/sport-build-boundaries/README.md`;
2. `docs/agent-system/sport-build-boundaries/SHARED_SPORT_BUILD_CONSTITUTION_V1.md`;
3. the exact sport boundary file;
4. then the target repository's local authority documents if it already exists.

These program-level files constrain scope but never supersede certified local sport architecture. Their existence does not authorize a future repository for Bridge execution.
