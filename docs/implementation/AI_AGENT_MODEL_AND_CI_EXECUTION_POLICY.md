# AI Agent Model and CI Execution Policy

Status: **AUTHORITATIVE OPERATING POLICY**  
Effective: 2026-09-09T00:56:00-07:00 (America/Los_Angeles)  
Scope: The Daily Line engineering work across TDLA and the Daily-* repositories, including Daily-MLB, Daily-Data-Core, Daily-NFL, Daily-NCAAF, website integration, and later automation/video implementation.

## 1. Purpose

The Daily Line uses multiple agent/model capability tiers. High-capability models are scarce engineering compute and must be spent on work that benefits from their reasoning quality: authority reconstruction, architecture, difficult implementation, scientific/PIT reasoning, migration semantics, hard debugging, and cross-repository integration.

They must **not** be used as expensive CI waiters.

The standard production-development loop is therefore:

```text
HIGH-CAPABILITY ENGINEERING MODEL
  -> implement / debug / locally validate / commit / prepare PR
  -> produce exact CI handoff
LOWER-COST VALIDATION MODEL
  -> mirror/push as required
  -> run remote PR/CI checks
  -> wait/poll
  -> collect evidence
  -> classify failures
  -> return only substantive failures to the higher model
```

This policy changes **execution allocation only**. It does not lower architecture, scientific, testing, security, or release requirements.

## 2. Core rule

> **Higher-capability models must not spend their limited compute running routine remote PR checks and waiting/polling for GitHub Actions or equivalent CI to finish when a lower-cost model can perform the same operational work safely.**

The high-capability model should normally stop at:

> **code complete + locally proven as far as practical + documented + authoritative private commit/PR prepared + exact CI handoff produced.**

The lower-cost validation model then owns routine remote validation and waiting.

## 3. What the high-capability engineering model should own

Use the strongest model available when the work materially benefits from deeper reasoning, including:

- reconstructing branch, PR, freeze, handoff, and authority topology;
- determining the correct implementation/execution anchor;
- architecture and contract decisions;
- PIT / temporal-leakage reasoning;
- evidence/provenance semantics;
- database/schema and non-trivial migration design;
- scientific/model lifecycle and promotion-gate reasoning;
- registry/permission semantics;
- difficult production implementation;
- cross-repository interface reconciliation;
- ambiguous or high-risk test failures;
- difficult debugging where several plausible root causes exist;
- security-sensitive architectural changes;
- code changes where an incorrect first pass would create substantial rework;
- final diff/architecture review before handoff.

The high-capability model should also run local/focused tests while it is actively using those results to implement or debug. This policy does **not** prohibit local testing by the engineering model.

## 4. High-capability model stop boundary

Once the coherent coding unit is complete, the high-capability model should:

1. run locally efficient validation required to establish that the implementation is ready for remote CI;
2. inspect the final diff;
3. verify no unrelated user work was overwritten;
4. verify no secrets/private/licensed artifacts are about to cross an inappropriate boundary;
5. update the authoritative documentation/handoff;
6. create the authoritative private commit;
7. prepare the PR or merge candidate when appropriate;
8. produce the CI handoff defined below;
9. **stop** if the remaining work is primarily remote execution or waiting.

The high-capability model should not remain active merely to:

- push a sanitized CI mirror;
- click/run GitHub Actions;
- wait for runners;
- poll workflow status;
- wait for Docker CI;
- repeatedly refresh PR checks;
- collect routine job IDs/log links;
- record a straightforward pass result.

Those are validation-operator duties.

## 5. Lower-cost validation model responsibilities

The lower-cost validation model/operator owns routine CI operations after receiving a complete handoff:

- verify the exact authoritative private SHA;
- verify PR/branch identity;
- read the repository-specific CI/public-mirror contract;
- prepare/push the permitted sanitized mirror when required;
- preserve the exact private-SHA -> public-SHA mapping;
- confirm tested-code equivalence and document exclusions;
- trigger required GitHub Actions/workflows;
- execute Docker CI where the established workflow supports it;
- wait/poll for workflow completion;
- collect workflow IDs, run IDs, job results, and relevant logs;
- classify failures;
- retry clearly transient infrastructure failures when policy permits;
- update the evidence ledger/handoff with exact results;
- return substantive failures to the high-capability model.

A lower-cost validation model must not silently alter scientific or production semantics simply to make CI green.

## 6. Public CI mirror rule

Where a repository has an authorized public CI mirror because private Actions are unavailable or constrained, the public repository is **supplemental validation infrastructure only**.

The flow must remain:

```text
PRIVATE AUTHORITATIVE SHA
  -> policy-controlled sanitization/mirroring
  -> PUBLIC CI SHA
  -> REMOTE CI EVIDENCE
```

Never allow the flow to become:

```text
public CI copy
  -> independent source edits
  -> green build
  -> accidental new authority
```

Any real source-code fix belongs in the authoritative private repository first. A new permitted mirror is then produced from that new private SHA.

Every public-CI evidence record must identify, at minimum:

- private repository;
- private branch;
- exact private SHA;
- public mirror repository;
- public branch;
- exact public SHA;
- sanitization/exclusion rules applied;
- equivalence status for code under test;
- workflow name;
- workflow/run/job IDs;
- result;
- Docker result when required;
- validations not executed;
- whether private exact-head certification is still required later.

Secrets, credentials, licensed/private data, proprietary evidence, and other disallowed material must never be copied merely to obtain public CI capacity.

## 7. Mandatory CI handoff from the high-capability model

Before stopping, the engineering model must leave a durable handoff containing:

- workstream/task ID;
- repository;
- authoritative branch;
- exact authoritative private SHA;
- parent/base SHA when relevant;
- PR number/status when relevant;
- governing CI/mirror contract;
- required workflows/checks;
- required Docker validation;
- expected test suites;
- any permitted skips and why;
- mirror exclusions/sanitization requirements;
- scientific permissions that must remain unchanged;
- PIT/evidence/registry/security invariants that must not be weakened;
- locally executed validation and exact result;
- expected success condition;
- explicit failure-routing instructions.

The lower-cost validation model should not have to reconstruct architecture merely to run CI.

## 8. Failure-routing policy

Remote CI failures are routed by complexity rather than by whichever model happens to be active.

### Lower-cost model may handle

- GitHub runner/transient infrastructure failure;
- retryable network/service failure;
- workflow dispatch/polling issue;
- public-mirror mechanics that do not change source semantics;
- straightforward formatting failure;
- straightforward lint failure;
- clearly mechanical type error;
- obviously stale generated metadata when authority explicitly defines regeneration;
- routine evidence-ledger updates.

### Prefer a mid/high engineering model for

- non-trivial implementation defects;
- unclear regression failures;
- cross-module integration bugs;
- schema or migration behavior changes;
- evidence/checksum/provenance integrity failures;
- replay/idempotency semantic failures;
- PIT or temporal-leakage failures;
- model-quality/scientific failures;
- calibration failures with semantic implications;
- model registry or promotion-authority failures;
- Recommendation Gate semantic failures;
- security-boundary failures;
- cross-repository contract failures;
- architectural ambiguity;
- any case where the proposed "fix" would weaken an existing invariant.

If failure classification is ambiguous, escalate rather than guessing.

## 9. High-capability model return rule

The high-capability model should return to a completed coding workstream only when the validation model provides a concrete failure package containing:

- exact private SHA;
- exact mirror SHA if applicable;
- workflow/run/job ID;
- failing command/test;
- relevant log excerpt;
- failure classification attempted;
- reproduction information;
- what was already ruled out.

The high-capability model should not be asked to spend compute rediscovering CI state that a lower-cost validation model can summarize precisely.

## 10. Parallel execution

When account/tool limits and repository dependencies permit, validation and development may proceed in parallel.

Example:

```text
TDL-01 implementation complete
  -> lower-cost model runs TDL-01-CI

while

higher-capability model begins TDL-02 on a clearly documented provisional descendant
```

This is permitted only when:

- the dependency on the provisional parent is explicit;
- the parent is not falsely called certified;
- the descendant can be safely rebased/reconciled if parent CI finds a substantive defect;
- repository merge/owner-approval rules remain respected.

## 11. Exceptions

A higher-capability model may interact directly with remote CI when doing so is part of active diagnosis and materially reduces uncertainty, for example when a difficult environment-specific failure only appears in CI and the model must inspect one immediate rerun after a targeted repair.

This is an exception, not the default operating mode.

Even then, prolonged waiting/polling should be handed back to the validation model whenever practical.

## 12. Model naming and future-proofing

This policy is capability-based, not tied permanently to specific product names.

Current examples may include a highest-capability engineering model such as Astra and lower-cost models such as Sol/Terra for validation/operator work, but model names, prices, and limits may change.

The durable rule is:

> Spend premium reasoning compute on reasoning-intensive engineering. Spend lower-cost compute on deterministic CI operations and waiting.

## 13. Relationship to quality gates

This policy does not authorize skipping CI.

It does not change:

- exact-head requirements;
- private/public source authority;
- Docker requirements;
- test requirements;
- security checks;
- scientific promotion gates;
- PIT/leakage protections;
- migration checks;
- owner merge approvals;
- documentation requirements.

It only assigns those tasks to the most cost-effective capable agent.

## 14. Standard workstream pattern

Use this pattern for future bounded Daily Line implementation jobs:

```text
A. HIGH-CAPABILITY IMPLEMENTATION PASS
   authority -> implementation -> local validation -> documentation -> commit/PR -> CI handoff -> STOP

B. LOWER-COST CI PASS
   verify SHA -> mirror if authorized -> push -> remote CI/Docker -> wait -> evidence -> classify

C1. PASS
   record evidence -> advance/certify according to authority

C2. MECHANICAL FAILURE
   lower-cost repair if clearly authorized -> rerun

C3. SUBSTANTIVE FAILURE
   exact failure handoff -> high-capability engineering model
```

This pattern should be included in future Work prompts unless the task has no remote CI component.
