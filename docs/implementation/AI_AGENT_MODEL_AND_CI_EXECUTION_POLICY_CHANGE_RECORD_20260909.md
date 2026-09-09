# AI Agent Model / CI Execution Policy — Change Record

Timestamp: 2026-09-09T00:56:00-07:00 (America/Los_Angeles)  
Refined: 2026-09-09T08:24:19-07:00 (America/Los_Angeles)  
Area: documentation / agent operations / CI cost control

## Summary

Added a durable project-wide operating policy that separates reasoning-intensive engineering work from routine exhaustive validation and remote CI waiting.

Higher-capability/premium models are expected to perform authority reconstruction, architecture, difficult implementation/debugging, focused/locally useful validation, final diff review, documentation, authoritative private commit/PR preparation, and an exact validation/CI handoff. They should then stop when the remaining work is primarily long-running full-suite validation, public-mirror synchronization, remote GitHub Actions/Docker execution, polling/waiting, and evidence collection.

Lower-cost capable validation models/operators own those routine exhaustive-validation and CI operations and escalate only substantive failures back to the higher-capability engineering model.

## 2026-09-09 refinement — local exhaustive validation follows the same compute rule

The policy was expanded after observing a premium engineering agent remain active while a long-running full Daily-MLB regression suite continued with no reported failures and no active implementation question left to resolve.

The refinement makes the intended boundary explicit:

> **Use premium tests to answer engineering questions. Use lower-cost validation to prove the finished repository exhaustively.**

Premium/high-capability models may and should run focused, targeted, and reasonably fast local tests when the results are needed for active implementation or debugging. They should not normally spend scarce compute sitting on:

- full repository regression suites;
- full Stats/model-quality suites;
- exhaustive migration/replay matrices;
- long E2E/certification runs;
- Docker certification;
- routine dependency/security/locked-install rehearsals;
- remote CI/polling;

once implementation scope is frozen and there is no current failure to diagnose.

If a long-running local suite can be stopped safely, it may be recorded as `INCOMPLETE — DELEGATED`, not failed. The exact command and required pass condition must be included in the validation handoff.

A lower-cost capable validation model then executes the exhaustive local/remote validation, waits for completion, records evidence, and routes only substantive failures back to the higher-capability engineering model.

## Reason

Astra-class/high-capability models consume scarce/high-cost agent allowance quickly. Spending that allowance waiting for either remote CI or long-running local exhaustive validation provides little reasoning value once implementation is frozen and reduces total engineering throughput. The project can preserve every existing quality/certification gate while assigning deterministic validation operations to cheaper models.

## Files/components affected

- `docs/implementation/AI_AGENT_MODEL_AND_CI_EXECUTION_POLICY.md`
- `AGENTS.md` section 18.1
- `docs/implementation/CURRENT_RESUME_POINT.md`
- this change record

## Authority / contract impact

This is an engineering-execution policy. It does not change TDLA runtime architecture or any sport scientific authority.

It establishes the default agent workflow:

```text
premium engineering model
  -> implement / focused validation / commit / PR / validation handoff / stop
lower-cost validation model
  -> exhaustive local suites / mirror / remote CI / Docker / wait / evidence / classify
substantive failure
  -> return exact failure package to premium engineering model
```

## Public CI mirror impact

Where an authorized public CI mirror exists, private source remains authoritative. Exact private-SHA -> public-SHA mapping, sanitization/exclusion records, workflow/run IDs, Docker result, and unexecuted private-exact-head requirements must remain recorded. Public CI must never become an independent source-authority branch.

## Validation / evidence

Documentation-only policy refinement. No production code, schema, model, scientific permission, test requirement, CI gate, or deployment state changed.

## Risks / open questions

Model product names and pricing may change. The policy is therefore capability-based rather than permanently tied to Astra/Sol/Terra names.

The cutoff is intentionally not a rigid wall-clock number. A broad suite may remain with the premium model when its result is immediately needed for active reasoning, when it is reasonably fast, or when handoff overhead would exceed the expected validation cost.

## Rollback / recovery

If the policy later proves inefficient, revise it explicitly and preserve this historical record. Do not silently return to using premium models for routine exhaustive-validation or remote-CI waiting.

## Next exact step

Apply this execution split to future bounded Daily Line Work prompts. Premium implementation prompts should end at the validation/CI-handoff boundary; separate validation prompts should own exhaustive local suites, remote PR/Actions/Docker waiting, and evidence collection.
