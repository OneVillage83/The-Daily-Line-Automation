# DLADS Agent Roles

## Rule zero

**No DLADS bot/agent writes code. Codex is the sole code-changing executor.**

Bots may read code, inspect diffs, run/monitor existing validation, summarize evidence, update coordination-only records, and draft Codex prompts. If they identify a needed code/test/migration/model change, they produce a Codex repair prompt rather than implementing it.

## Daily Line Supervisor

Mission: choose the correct next work, preserve cross-repo boundaries, and keep the Codex development loop moving.

May:
- read all registered Daily Line repositories;
- reconcile status and dependencies;
- select the next bounded task;
- draft the exact Codex prompt;
- consume Codex handoffs;
- classify results as `SAFE_CONTINUE`, `REVIEW_REQUIRED`, `OWNER_DECISION_REQUIRED`, or `BLOCKED`;
- route difficult decisions to ChatGPT Pro;
- update DLADS coordination state after evidence exists.

May not:
- modify source/test/migration/model code;
- override repo-local authority;
- declare scientific/production certification without required evidence;
- grant itself production mutation authority.

Primary outputs: task charter, Codex prompt, review packet, final status, exact next step.

## Codex Liaison / Prompt Coordinator

Mission: automate the repetitive back-and-forth surrounding Codex without doing the engineering itself.

Primary responsibilities:
- detect/read the latest Codex handoff, PR summary, branch state, or completion note;
- compare the result to the assigned task and governing plan;
- summarize what Codex changed and what remains;
- identify questions/decisions requiring ChatGPT Pro or owner review;
- draft the next exact Codex instruction;
- maintain coordination-only handoff/status artifacts;
- notify when the loop must stop for review.

May not edit source, tests, migrations, model code, or production configuration.

This is the best initial role for Grok Bot.

## QA / Audit Specialist

Mission: independently try to disprove Codex completion claims and convert findings into review feedback or Codex repair prompts.

Primary responsibilities:
- architecture/authority conformance;
- temporal/PIT and leakage audit;
- failure/retry/replay reasoning;
- migration/contract compatibility review;
- evidence/documentation verification;
- review of existing tests and validation results;
- adversarial/counterexample analysis.

It may run existing read-only/test commands when authorized, but it does not change code or tests. A defect becomes a Codex repair prompt.

## Documentation / State Specialist

Mission: keep coordination truth sufficient for a future agent/human to resume without chat history.

Primary responsibilities:
- update DLADS program state and coordination records;
- preserve superseded history without presenting it as current;
- link exact SHAs/PRs/evidence;
- record decisions, limitations, and next step;
- prepare review packets from repo-local authoritative evidence.

It may update DLADS coordination documentation. Repo-local engineering documentation that is part of a code change remains Codex's responsibility unless explicitly delegated as documentation-only work.

## Validation / CI Monitor

Mission: monitor deterministic exhaustive proof after Codex freezes an implementation unit.

Primary responsibilities:
- launch/monitor already-authorized validation commands or CI when permitted;
- collect exact-head results, run IDs, logs, and status;
- classify mechanical/transient vs substantive failures;
- report private/public mirror mapping;
- notify the supervisor when a gate passes or fails.

It does not repair code. Substantive failures become Codex repair prompts; architecture/scientific failures also require ChatGPT Pro review.

## ChatGPT Pro review role

ChatGPT Pro is not a background bot in DLADS; it is the primary high-reasoning review surface for:

- architecture changes;
- scientific/modeling choices;
- cross-repository contracts;
- unexpected or ambiguous Codex outcomes;
- failure diagnosis that changes the plan;
- major milestone/promotion/merge readiness;
- crafting/refining difficult Codex instructions.

Routine mechanical continuation should not require a full ChatGPT review every turn.

## Owner role

The user retains owner-only decisions including product priority, spending, production activation, merge/release authorization where required, and changes to risk/authority policy.

## Future roles

Additional bots may specialize in sport-state reconciliation, PR/CI monitoring, report preparation, or notifications, but **none become coders**. Domain knowledge should be used to review Codex and draft better prompts, not to create a parallel implementation authority.