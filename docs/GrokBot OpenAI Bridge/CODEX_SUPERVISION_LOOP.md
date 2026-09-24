# DLADS Codex Supervision Loop

Established: 2026-09-15

## Core rule

**Codex is the sole code-changing executor for Daily Line development.**

DLADS agents/bots are supervisory and clerical. They may read repositories, inspect Codex outputs, summarize progress, compare work to the plan, monitor validation, update coordination records, and draft the next Codex instruction. They may not modify source code, test code, migrations, model code, or production configuration.

ChatGPT Pro is the primary high-reasoning reviewer/architect. Grok Bot or another low-cost bot may act as a persistent liaison/monitor, but not as a programmer.

## Intended loop

```text
YOU
 |
 v
ChatGPT Pro / DLADS Supervisor
 |
 | precise bounded instruction
 v
CODEX  <----- sole coding executor
 |
 | code + tests + repo-local docs + handoff
 v
CODEX HANDOFF
 |
 v
Liaison / Monitor Bot
 |  - reads handoff and Git/PR state
 |  - summarizes what changed
 |  - checks whether the task is complete/blocked
 |  - drafts questions and the next Codex prompt
 |  - never edits code
 v
ChatGPT Pro review when required
 |
 | approve / redirect / refine prompt
 v
NEXT CODEX PROMPT
 |
 v
CODEX
```

## Handoff artifacts

The loop should use durable artifacts rather than copying whole chat transcripts.

A Codex work unit should end with a compact handoff containing:

- task ID;
- target repository;
- entry SHA/branch;
- files changed;
- implementation summary;
- tests/checks run;
- failures or blockers;
- questions/decisions needed;
- exact suggested next step.

The liaison converts that into a **review packet** for ChatGPT Pro and/or a **next Codex prompt**.

## Automatic-continuation classes

The liaison may classify a handoff as:

### `SAFE_CONTINUE`
Mechanical continuation already authorized by the existing plan, with no architecture/scientific/authority ambiguity. The liaison may draft the next Codex prompt from the governing plan.

### `REVIEW_REQUIRED`
Requires ChatGPT Pro review before continuing because the handoff contains architecture changes, scientific/modeling decisions, cross-repo contract changes, failed gates, unclear scope, or a material deviation from plan.

### `OWNER_DECISION_REQUIRED`
Requires the user's explicit decision because it changes product priorities, budget, production authority, release/merge authority, or other owner-only choices.

### `BLOCKED`
External dependency, missing evidence, failed validation, or unresolved authority prevents safe continuation.

## What the liaison/bots may do

- monitor Codex completion/handoff files;
- read GitHub branches, PRs, commits, checks, and logs;
- read repo-local `AGENTS.md`, resume, roadmap, and certification docs;
- compare Codex's result with its assigned task;
- generate concise review packets;
- draft the next Codex prompt;
- update DLADS coordination state and non-authoritative tracking docs;
- notify the user when review/decision is needed;
- run read-only repository audits;
- monitor deterministic validation/CI and report results.

## What the liaison/bots may not do

- edit source code;
- edit tests to make a failure disappear;
- edit database migrations;
- edit model/training/calibration/ensemble code;
- perform refactors;
- implement bug fixes;
- create production configuration changes;
- activate/publish/deploy/merge without separate authorization;
- silently make scientific or architecture decisions on ChatGPT/user's behalf.

If a bot discovers a needed code change, its output is a **Codex repair prompt**, not a patch.

## Best-cost initial deployment

Use existing subscriptions first:

1. **ChatGPT Pro / Codex:** all coding and high-reasoning review.
2. **Grok Bot (optional):** persistent liaison, monitoring, review-packet preparation, status reconciliation, and next-prompt drafting.
3. **OpenAI API (optional later):** only if a fully programmatic supervisor/relay is worth the convenience.

Because coding stays in Codex, any future API supervisor sees compact handoff packets rather than entire repositories, keeping token cost low.

## Review frequency

ChatGPT Pro does not need to review every mechanical Codex turn.

Recommended pattern:

- auto-draft/continue routine work;
- ChatGPT review at milestone boundaries, blockers, architecture/science decisions, unexpected failures, and before stronger status/merge/release claims;
- user review for owner-only decisions.

This automates the repetitive back-and-forth without removing the high-value human/ChatGPT judgment that has been guiding Daily Line development.