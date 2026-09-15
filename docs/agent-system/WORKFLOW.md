# DLADS Supervisor Workflow

## State machine

```text
INTAKE
  -> LOAD_PROGRAM_STATE
  -> RECONCILE_REPO_TRUTH
  -> SELECT_TARGET
  -> AUTHORIZE_SCOPE
  -> PLAN_BOUNDED_WORK
  -> IMPLEMENT
  -> FOCUSED_VALIDATE
  -> QA_AUDIT
  -> EXHAUSTIVE_VALIDATION_OR_HANDOFF
  -> DOCUMENT
  -> UPDATE_PROGRAM_STATE
  -> COMPLETE / BLOCKED / ESCALATED
```

## 1. Intake

Classify the request as one of:

- `CONTINUE_PROGRAM`
- `CONTINUE_REPOSITORY`
- `IMPLEMENT_SPECIFIC_TASK`
- `AUDIT`
- `VALIDATE`
- `ARCHITECTURE`
- `INCIDENT/REPAIR`

Explicit user scope wins over automatic priority selection.

## 2. Load program state

Read:

1. root `AGENTS.md`;
2. `docs/agent-system/README.md`;
3. `ACTIVE_EXECUTION_PLAN.md`;
4. `state/program_state.json`;
5. `REPOSITORY_REGISTRY.md`;
6. relevant program roadmap/evaluation docs.

## 3. Reconcile target repository truth

Before any write, inspect the target repository's:

- default branch HEAD;
- `AGENTS.md` / local instruction hierarchy;
- start/resume/status/certification documents;
- relevant open PR/branch evidence;
- current tests/CI evidence where material.

Never infer current state only from DLADS state.

## 4. Select target

For `CONTINUE_PROGRAM`, choose the highest-priority **unblocked** task under `ACTIVE_EXECUTION_PLAN.md`.

Selection must record:

- target repository;
- exact entry branch/SHA;
- governing documents;
- task ID;
- why this task is next;
- non-goals;
- dependencies;
- acceptance criteria;
- validation owner.

## 5. Authorize scope

Determine which specialist roles are required. Grant only the minimum conceptual capability needed. A specialist does not inherit the supervisor's entire authority.

Examples:

- contract/schema change -> Engineering + QA/Audit + Documentation;
- statistical model work -> Modeling + QA/Audit + Validation/CI;
- status-only reconciliation -> Supervisor + QA/Audit/Documentation, no implementation writer.

## 6. Plan bounded work

Write a short task plan before implementation when work is non-trivial. Prefer small independently reviewable milestones over giant prompts.

The task plan must identify what **will not** be changed.

## 7. Implement

Codex or the engineering specialist works inside the target repository and obeys that repository's local instructions. Cross-repo edits require separate bounded scopes unless an atomic contract migration genuinely requires coordinated changes.

## 8. Focused validation

Premium/high-reasoning engineering compute should run tests needed to answer active implementation/debugging questions. Do not spend it merely waiting for exhaustive deterministic suites once the implementation is frozen.

## 9. QA/Audit

An independent audit checks:

- contract/authority conformity;
- temporal/PIT correctness;
- leakage risks;
- migration/replay behavior where relevant;
- failure/degradation behavior;
- changed tests vs real behavior;
- evidence and documentation consistency;
- accidental scope widening.

QA may return `PASS`, `PASS_WITH_LIMITS`, or `BLOCKED` with exact evidence.

## 10. Exhaustive validation / CI handoff

Use the repository's existing validation policy. When remaining work is deterministic long-running proof, produce an exact handoff to the Validation/CI role rather than keeping a premium engineering agent alive to poll/wait.

## 11. Documentation

A completed material change must update the target repository's required change journal/status/resume/certification docs. Program-level status is then updated only after target-repo evidence exists.

## 12. Program-state update

Update `state/program_state.json` when any of these change:

- repository exact head used as a frozen/program checkpoint;
- milestone state;
- blocker;
- exact next task;
- cross-repo dependency;
- program phase/priority.

Do not copy every implementation detail into program state. Link to the authoritative target document.

## Stop conditions

Stop and mark `BLOCKED` or `ESCALATED` when:

- target repository truth cannot be resolved;
- required user/owner authorization is absent;
- science/architecture conflict is unresolved;
- an external dependency prevents valid proof;
- requested work would bypass a certified authority boundary;
- evidence is insufficient to claim the requested completion state.

A blocked result must still leave an exact next step.