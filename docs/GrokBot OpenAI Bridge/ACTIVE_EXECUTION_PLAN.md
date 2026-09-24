# Daily Line — Active Program Execution Plan

Program state version: 1  
Updated: 2026-09-15  
Current program milestone: **DL-AGENT-1 — Cross-repository truth reconciliation**

## Why this is first

The individual Daily Line repositories already contain detailed, independently evolving continuation documents. Some were updated after the last program-wide planning pass. Before the supervisor can safely choose implementation work from a one-line command, it must reconcile live repository truth into the program state.

This is a **coordination audit**, not an architecture rewrite and not permission to alter sport/model authority.

## DL-AGENT-1 task

Inspect and reconcile, at minimum:

1. `Daily-Data-Core`
2. `Daily-MLB`
3. `Daily-NFL`
4. `Daily-NCAAF`
5. `Daily-Model-Core`
6. `The-Daily-Line-website`
7. `The-Daily-Line-Automation`
8. `Daily-Line-Private-Validation` where validation evidence affects a private authoritative repo

For each repository record:

- default branch and exact HEAD;
- repo-local authority/start documents;
- current certified/frozen milestone;
- current active/draft milestone;
- exact next authorized task;
- blockers;
- open PRs relevant to the next task;
- required validation/owner gate;
- cross-repo dependencies;
- whether the program registry/state is stale.

## Seed facts — verify, do not blindly trust

These are only bootstrap hints for the first reconciliation run:

- TDLA's own local resume point still identifies **A-11 Retry / Timeout / Idempotency Architecture** as the next core automation architecture step; DLADS does not supersede it.
- `Daily-Model-Core` documents DMC-2 as merged/frozen and DMC-3 as authorized/not started.
- `Daily-NFL` has recent DDC7 weather/weather-activation merge-freeze work dated through 2026-09-15; determine its exact current next step from repo-local evidence.
- `Daily-MLB` has extensive current Codex/status docs and active manual-production-line certification work; reconcile the newest exact head before dispatching implementation.
- `Daily-NCAAF` remains much earlier in implementation than MLB/NFL.
- Website and automation progress must not be allowed to outrun certified upstream prediction/publication contracts.

## Acceptance criteria

DL-AGENT-1 is complete only when:

- `state/program_state.json` reflects verified current heads/statuses;
- every priority repository has an exact continuation pointer or explicit `BLOCKED/UNKNOWN` state;
- stale or contradictory program-level claims are removed or marked superseded;
- the supervisor can select one highest-priority unblocked next task without relying on chat memory;
- that selected task names its target repo, governing docs, entry SHA/branch, acceptance criteria, validation lane, and required handoff.

## Priority rule after reconciliation

Select work in this order unless the user explicitly chooses another track:

1. blockers preventing certification of the current priority sport/data pipeline;
2. complete/certify MLB, then NFL, then NCAAF manual production pipelines and shared dependencies;
3. advance Daily-Model-Core reusable model lifecycle only when its dependencies are satisfied;
4. calibration -> learned ensemble / Unified Line -> market intelligence;
5. publication outputs/report/infographic/review;
6. website integration;
7. automation authority;
8. social/video authority;
9. cross-sport expansion.

## Parallelism rule

Read-only audits may run in parallel. Writes may proceed in parallel only when repositories and contracts are independent and the supervisor proves there is no shared-schema/release dependency. Never create two competing authoritative changes to the same contract at once.

## Completion handoff

At the end of DL-AGENT-1, replace this file's current milestone section with the exact selected development task and retain a short reconciliation receipt in `docs/GrokBot OpenAI Bridge/history/`.