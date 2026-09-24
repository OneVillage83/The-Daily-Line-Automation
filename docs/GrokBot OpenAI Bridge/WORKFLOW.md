# DLADS Supervisor Workflow

## State machine

```text
INTAKE
  -> LOAD_PROGRAM_STATE
  -> RECONCILE_REPO_TRUTH
  -> SELECT_TARGET
  -> BUILD_CODEX_PROMPT
  -> CODEX_EXECUTES
  -> INGEST_CODEX_HANDOFF
  -> CLASSIFY_RESULT
       |-> SAFE_CONTINUE ---------> BUILD_NEXT_CODEX_PROMPT
       |-> REVIEW_REQUIRED -------> CHATGPT_PRO_REVIEW
       |-> OWNER_DECISION_REQUIRED -> USER_DECISION
       `-> BLOCKED ---------------> FAILURE/DEPENDENCY HANDOFF
  -> MONITOR_VALIDATION_IF_NEEDED
  -> UPDATE_COORDINATION_STATE
  -> COMPLETE / CONTINUE / BLOCKED
```

## Rule zero

Codex is the only component in this loop that changes source code, tests, migrations, model code, or production configuration.

DLADS agents/bots supervise Codex. They do not become alternate programmers.

## 1. Intake

Classify the request as one of:

- `CONTINUE_PROGRAM`
- `CONTINUE_REPOSITORY`
- `IMPLEMENT_SPECIFIC_TASK`
- `AUDIT_CODEX_RESULT`
- `MONITOR_VALIDATION`
- `ARCHITECTURE_REVIEW`
- `INCIDENT/REPAIR_PROMPT`

Explicit user scope wins over automatic priority selection.

## 2. Load program state

Read:

1. root `AGENTS.md`;
2. `docs/GrokBot OpenAI Bridge/README.md`;
3. `CODEX_SUPERVISION_LOOP.md`;
4. `ACTIVE_EXECUTION_PLAN.md`;
5. `state/program_state.json`;
6. `REPOSITORY_REGISTRY.md`;
7. relevant roadmap/evaluation docs.

## 3. Reconcile target repository truth

Before drafting a Codex instruction, inspect the target repository's:

- default branch HEAD;
- `AGENTS.md` / local instruction hierarchy;
- start/resume/status/certification documents;
- relevant open PR/branch evidence;
- current tests/CI evidence where material.

Never infer current state only from DLADS state or chat memory.

## 4. Select target

For `CONTINUE_PROGRAM`, choose the highest-priority **unblocked** task under `ACTIVE_EXECUTION_PLAN.md`.

Selection records:

- target repository;
- exact entry branch/SHA;
- governing documents;
- task ID;
- why this task is next;
- non-goals;
- dependencies;
- acceptance criteria;
- review/validation lane.

## 5. Build the Codex prompt

The supervisor/liaison produces an exact bounded Codex instruction containing:

- target repository and entry state;
- documents Codex must read first;
- objective;
- allowed scope;
- explicit non-goals;
- architectural/scientific constraints;
- acceptance criteria;
- focused validation expectations;
- required handoff fields;
- stop/escalation conditions.

This prompt is the principal automation output.

## 6. Codex executes

Codex performs all implementation work under the target repository's local rules.

Codex should:

- edit implementation/test/migration/model/config files as authorized;
- run focused engineering validation;
- update repo-local engineering documentation required by that repository;
- produce a compact handoff when the bounded unit ends or blocks.

## 7. Ingest the Codex handoff

The liaison reads Codex's handoff, Git diff/PR state, and relevant test/CI evidence.

It prepares a review packet containing:

- assignment vs delivered result;
- files/components changed;
- proof run;
- unresolved failures/questions;
- deviations from scope/plan;
- recommended classification;
- draft next Codex prompt.

The liaison does not modify implementation to repair what it finds.

## 8. Classify the result

### `SAFE_CONTINUE`
Use when the next action is a mechanical continuation already authorized by the governing plan and no architecture/scientific/authority ambiguity exists. Draft/queue the next Codex prompt.

### `REVIEW_REQUIRED`
Use when architecture, scientific/modeling semantics, cross-repo contracts, unexpected failures, plan deviations, or stronger completion claims need ChatGPT Pro review.

### `OWNER_DECISION_REQUIRED`
Use for product-priority, spend, production/release/merge authority, policy/risk, or other owner-only choices.

### `BLOCKED`
Use for unresolved dependencies, failed gates, missing evidence, unavailable systems, or authority conflicts.

## 9. ChatGPT Pro review

When `REVIEW_REQUIRED`, ChatGPT Pro reviews the compact handoff/evidence rather than recreating the entire coding session.

ChatGPT Pro returns one of:

- approved next Codex prompt;
- revised Codex prompt;
- additional evidence request;
- architecture/science decision;
- escalation to owner;
- stop/block disposition.

This is the automated version of the prior manual back-and-forth: Codex does work, the supervisory layer packages it, ChatGPT decides how to steer Codex next.

## 10. Validation monitoring

After Codex freezes an implementation unit, a non-coding monitor may run or watch already-authorized deterministic validation/CI and collect evidence.

It may not repair failures. Mechanical failures are reported as retry candidates; substantive failures return to ChatGPT/Codex as repair prompts.

## 11. Documentation and coordination state

Codex owns repo-local engineering documentation that is part of its implementation task.

The supervisory layer may update DLADS coordination-only artifacts:

- program state;
- active execution pointer;
- review packets;
- cross-repo dependency/status records.

Program-level status changes only after authoritative target-repo evidence exists.

## Stop conditions

Stop and mark `BLOCKED`/`REVIEW_REQUIRED`/`OWNER_DECISION_REQUIRED` when:

- target repository truth cannot be resolved;
- required authorization is absent;
- science/architecture conflict is unresolved;
- external dependency prevents valid proof;
- continuing would bypass a certified authority boundary;
- evidence is insufficient to support the next status claim.

A stop result must still include an exact next Codex prompt or exact human decision/evidence needed.