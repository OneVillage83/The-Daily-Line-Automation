---
name: daily-line-validation-handoff
description: Convert a code-complete Daily Line engineering unit into an exact, cost-efficient exhaustive-validation and CI handoff without weakening any gate.
---

# Daily Line Validation Handoff

## Trigger

Use when implementation scope is frozen, focused proof is complete, and remaining work is primarily full-suite/CI/Docker/matrix/security evidence collection.

## Workflow

1. Verify exact source branch/SHA/tree when available.
2. List focused proof already completed.
3. List every remaining exhaustive command/job/matrix and expected success condition.
4. Identify required environment/runner/provider without exposing secrets.
5. Identify public-mirror mapping requirements, if any.
6. Define transient/mechanical failures the validation role may retry.
7. Define substantive failure classes that must be escalated.
8. Mark the engineering work `INCOMPLETE_DELEGATED` or `READY_FOR_VALIDATION`; never call it certified early.
9. Provide exact evidence artifacts/run IDs/logs that must be captured.
10. Update the target repo's required handoff/status docs.

## Core rule

Use premium tests to answer engineering questions. Use lower-cost validation to prove the finished repository exhaustively. This changes who performs proof, not the proof required.