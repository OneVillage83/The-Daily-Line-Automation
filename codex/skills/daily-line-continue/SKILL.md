---
name: daily-line-continue
description: Continue The Daily Line from verified GitHub repository truth, select the highest-priority authorized task, and carry it through bounded implementation, QA, documentation, and handoff.
---

# Daily Line Continue

## Inputs

- optional user-selected track/repository/task;
- otherwise use the DLADS active program plan.

## Workflow

1. Read repository root `AGENTS.md` and `docs/agent-system/README.md`.
2. Read `ACTIVE_EXECUTION_PLAN.md`, `state/program_state.json`, and `REPOSITORY_REGISTRY.md`.
3. If the user did not choose a task, resolve the highest-priority unblocked candidate.
4. Fetch/inspect that repository's actual default head and local AGENTS/start/resume/certification documents.
5. If DLADS state is stale, reconcile it before implementation.
6. Produce a bounded task charter: repo, entry SHA/branch, governing docs, objective, non-goals, dependencies, acceptance criteria, validation lane.
7. Execute only the authorized scope under target-repo rules.
8. Run focused validation needed to answer implementation questions.
9. Perform independent QA/Audit.
10. Delegate long exhaustive proof according to validation policy when appropriate.
11. Update target-repo durable docs, then program state.
12. Return the exact completion status and next step.

## Final checks

- No status claim comes only from chat memory.
- No post-event information entered a pre-event prediction path.
- No repository authority boundary was silently moved.
- No production side effect occurred without separate authorization.
- The next session can resume from Git alone.