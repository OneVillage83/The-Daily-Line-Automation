# DLADS Bounded Work Handoff Contract

Every delegated material task should end with a compact handoff containing these fields.

```text
Task ID:
Role:
Target repository:
Entry branch/SHA:
Working branch/PR:
Governing docs:
Objective:
Non-goals:
Files/components changed:
Implementation summary:
Authority/contract impact:
Data/migration impact:
Focused validation completed:
Exhaustive validation status:
QA/Audit disposition:
Known limits/risks:
Rollback/recovery:
Documentation updated:
Program-state impact:
Exact next step:
```

## Status vocabulary

Use one of:

- `COMPLETE`
- `READY_FOR_QA`
- `READY_FOR_VALIDATION`
- `READY_FOR_OWNER_REVIEW`
- `BLOCKED`
- `INCOMPLETE_DELEGATED`
- `SUPERSEDED`

Do not use `DONE`, `CERTIFIED`, `PRODUCTION_READY`, or similar stronger words unless the governing repository's required gate has actually been satisfied.

## Failure package

When blocked, include:

- minimal reproducible failure;
- exact source/head;
- command/test/run ID;
- expected vs observed behavior;
- classification (`mechanical`, `contract`, `temporal`, `scientific`, `security`, `infrastructure`, `evidence`, `unknown`);
- smallest safe next investigation/repair;
- changes explicitly not authorized.

## Cross-agent handoff

A receiving agent must re-check the target repo's current head before relying on the handoff. If the head or governing docs changed, the handoff is stale until reconciled.