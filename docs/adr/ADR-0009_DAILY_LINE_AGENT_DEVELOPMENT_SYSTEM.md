# ADR-0009 — Daily Line Agent Development System

- Status: **ACCEPTED**
- Date: 2026-09-15
- Clarification: **Codex-only coding authority**

## Context

The Daily Line is a multi-repository production program with independently governed sport pipelines, shared data/model cores, website, validation, automation, and publication systems. Long-running development has accumulated detailed repo-local continuation documents, but cross-project continuation still depends too much on manually carrying Codex output back to ChatGPT, deciding what to tell Codex next, and reconstructing state across chats and repositories.

The user already pays for ChatGPT Pro and wants Codex to remain the engineering executor. The automation problem is therefore **not how to add more coding agents**. It is how to automate the supervisory back-and-forth around Codex while preserving ChatGPT Pro for high-value architecture/reasoning review.

## Decision

Create the **Daily Line Agent Development System (DLADS)** in `The-Daily-Line-Automation` as a program-coordination and Codex-supervision layer.

1. Git/repository documentation remains authoritative.
2. **Codex is the sole code-changing executor.** Source code, test code, migrations, model/training/calibration/ensemble code, refactors, bug fixes, and implementation configuration changes are performed by Codex under the target repository's local rules.
3. The Daily Line Supervisor selects the next task and drafts the exact bounded Codex instruction, but does not implement it.
4. Supervisory bots/agents may read repos, inspect Codex handoffs/diffs/PRs, reconcile state, summarize evidence, monitor existing validation, update coordination-only records, classify next steps, and draft the next Codex prompt.
5. If a supervisory bot finds a defect, its output is a **Codex repair prompt**, not a patch.
6. ChatGPT Pro is the primary high-reasoning review surface for architecture, scientific/modeling semantics, cross-repository contracts, unexpected failures, milestone decisions, and difficult Codex prompt design.
7. Reusable `SKILL.md` workflows define continuation, repo audit, and validation handoff behavior.
8. Version-controlled manifests define non-coding Supervisor, Codex Liaison, Engineering Review, Modeling Review, QA/Audit, Documentation/State, and Validation/CI Monitor responsibilities.
9. Grok Bot may be used as a low-cost persistent liaison/monitor; OpenAI/xAI APIs remain optional programmatic supervision layers rather than duplicate coding capacity.
10. Runtime publication to external agent platforms is a later governed step; provider IDs are metadata only.
11. Program state is machine-readable but coordination-only. When it conflicts with target repo truth, target repo truth wins and program state must be repaired.
12. Existing repo-local resume/certification documents continue to govern their repositories.
13. The first post-baseline milestone is a cross-repository truth reconciliation before automatic task selection is trusted.

## Consequences

Positive:
- a one-line continuation request can become deterministic;
- repetitive Codex/ChatGPT steering can be automated without paying for duplicate coding agents;
- current status becomes auditable and machine-readable;
- compact Codex handoffs can be reviewed cheaply;
- cross-repo dependencies become explicit;
- ChatGPT Pro is reserved for the decisions where high reasoning adds the most value;
- Grok Bot or low-cost API models can handle monitoring/clerical coordination;
- stale chat memory is no longer required to resume.

Tradeoffs:
- program state must be actively reconciled;
- Codex must produce reliable handoff artifacts;
- fully hands-off continuation requires a supported trigger/relay mechanism between handoff detection and Codex task submission;
- supervisory automation still needs stop gates for architecture/science/owner decisions.

## Non-goals

DLADS is not:
- a second coding system beside Codex;
- a replacement for TDLA production orchestration;
- a sport-model authority;
- a substitute for repository CI/certification;
- a production publishing bot;
- a hidden autonomous permission layer.

## References

- `docs/agent-system/README.md`
- `docs/agent-system/CODEX_SUPERVISION_LOOP.md`
- `docs/agent-system/ACTIVE_EXECUTION_PLAN.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/EVALUATION_GATES.md`
- `docs/agent-system/MULTI_PROVIDER_EXECUTION_STRATEGY.md`
- `docs/implementation/AI_AGENT_MODEL_AND_CI_EXECUTION_POLICY.md`
