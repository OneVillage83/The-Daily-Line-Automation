# AI Agent Model / CI Execution Policy — Change Record

Timestamp: 2026-09-09T00:56:00-07:00 (America/Los_Angeles)  
Area: documentation / agent operations / CI cost control

## Summary

Added a durable project-wide operating policy that separates reasoning-intensive engineering work from routine remote CI waiting.

Higher-capability/premium models are expected to perform authority reconstruction, architecture, difficult implementation/debugging, locally useful validation, final diff review, documentation, authoritative private commit/PR preparation, and an exact CI handoff. They should then stop when the remaining work is primarily public-mirror synchronization, remote GitHub Actions/Docker execution, polling/waiting, and evidence collection.

Lower-cost capable validation models/operators own those routine CI operations and escalate only substantive failures back to the higher-capability engineering model.

## Reason

Astra-class/high-capability models consume scarce/high-cost agent allowance quickly. Spending that allowance waiting for remote CI provides little reasoning value and reduces total engineering throughput. The project can preserve every existing quality/certification gate while assigning deterministic CI operations to cheaper models.

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
  -> implement / local validation / commit / PR / CI handoff / stop
lower-cost validation model
  -> mirror / remote CI / Docker / wait / evidence / classify
substantive failure
  -> return exact failure package to premium engineering model
```

## Public CI mirror impact

Where an authorized public CI mirror exists, private source remains authoritative. Exact private-SHA -> public-SHA mapping, sanitization/exclusion records, workflow/run IDs, Docker result, and unexecuted private-exact-head requirements must remain recorded. Public CI must never become an independent source-authority branch.

## Validation / evidence

Documentation-only policy change. No production code, schema, model, scientific permission, CI gate, or deployment state changed.

## Risks / open questions

Model product names and pricing may change. The policy is therefore capability-based rather than permanently tied to Astra/Sol/Terra names.

## Rollback / recovery

If the policy later proves inefficient, revise it explicitly and preserve this historical record. Do not silently return to using premium models for routine remote CI waiting.

## Next exact step

Apply this execution split to future bounded Daily Line Work prompts. Premium implementation prompts should end at the CI-handoff boundary; separate validation prompts should own remote PR/Actions/Docker waiting and evidence collection.
