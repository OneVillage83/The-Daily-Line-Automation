# ADR-0009 — Daily Line Agent Development System

- Status: **ACCEPTED**
- Date: 2026-09-15

## Context

The Daily Line is a multi-repository production program with independently governed sport pipelines, shared data/model cores, website, validation, automation, and publication systems. Long-running development has accumulated detailed repo-local continuation documents, but cross-project continuation still depends too much on reconstructing context across chats and repositories.

OpenAI Codex now supports multi-agent engineering and reusable Skills, while the Agents API supports reusable agents and coordinated subagents. The project needs a durable development-control layer that can use these capabilities without creating a second source of truth or weakening repository authority.

## Decision

Create the **Daily Line Agent Development System (DLADS)** in `The-Daily-Line-Automation` as a program-coordination layer.

1. Git/repository documentation remains authoritative.
2. The Daily Line Supervisor selects/delegates work but cannot override target-repo authority.
3. Codex remains the primary implementation surface initially.
4. Reusable `SKILL.md` workflows define continuation, audit, and validation handoff behavior.
5. Version-controlled agent manifests/instructions define Supervisor, Engineering, Modeling, QA/Audit, Documentation, and Validation/CI roles.
6. Runtime publication to OpenAI Agents/Skills remains a later governed step; provider IDs are metadata only.
7. Program state is machine-readable but coordination-only. When it conflicts with target repo truth, target repo truth wins and program state must be repaired.
8. Development agents do not receive implicit production side-effect authority.
9. Existing repo-local resume/certification documents continue to govern their repositories.
10. The first post-baseline milestone is a cross-repository truth reconciliation before automatic task selection is trusted.

## Consequences

Positive:
- a one-line continuation request can become deterministic;
- work can be delegated by specialist role;
- current status becomes auditable and machine-readable;
- cross-repo dependencies become explicit;
- Codex and future runtime agents share the same Git-controlled operating model;
- stale chat memory is no longer required to resume.

Tradeoffs:
- program state must be actively reconciled;
- another documentation layer exists, but it intentionally stores only coordination state and links to domain truth;
- runtime agent publication requires additional eval, permission, and cost controls.

## Non-goals

DLADS is not:
- a replacement for TDLA production orchestration;
- a sport-model authority;
- a substitute for repository CI/certification;
- a production publishing bot;
- a hidden autonomous permission layer.

## References

- `docs/agent-system/README.md`
- `docs/agent-system/ACTIVE_EXECUTION_PLAN.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/EVALUATION_GATES.md`
- `docs/implementation/AI_AGENT_MODEL_AND_CI_EXECUTION_POLICY.md`
