# Daily Line Sport Build Boundaries

**Status:** PROGRAM COORDINATION PACK  
**Established:** 2026-09-23

This directory gives DLADS / the GrokBot-OpenAI-Bridge durable sport-by-sport boundaries before Codex work is dispatched.

These documents are **coordination guardrails, not replacement architecture**. Existing sport repositories retain authority through their own `AGENTS.md`, start/resume files, certified architecture, certification logs, and current Git evidence.

## Mandatory read order for sport work

1. `SHARED_SPORT_BUILD_CONSTITUTION_V1.md`
2. the exact sport boundary file
3. the target repository's local authority documents, if the repo already exists
4. current Git/PR/CI evidence
5. only then choose one bounded Codex task

## Sport files

- `DAILY_MLB_BUILD_BOUNDARY_V1.md` — existing repo; local Daily-MLB authority wins
- `DAILY_NFL_BUILD_BOUNDARY_V1.md` — existing repo; F-0 through F-24 local authority wins
- `DAILY_NCAAF_BUILD_BOUNDARY_V1.md` — existing repo; local F-layer architecture/overlay wins
- `DAILY_NBA_BUILD_BOUNDARY_V1.md` — planned
- `DAILY_NCAAB_BUILD_BOUNDARY_V1.md` — planned college-basketball architecture
- `DAILY_WNBA_BUILD_BOUNDARY_V1.md` — planned; separate validation/calibration from NBA
- `DAILY_NHL_BUILD_BOUNDARY_V1.md` — planned
- `DAILY_SOCCER_BUILD_BOUNDARY_V1.md` — planned multi-competition architecture
- `FUTURE_SPORT_TEMPLATE_V1.md` — bootstrap template for any later sport

## Required program flow

```text
sport factual evidence
  -> independent sport models
  -> calibrated TDL Unified Line (FREEZE)
  -> point-in-time market comparison
  -> sport Recommendation Gate
  -> sealed SportDecisionPackage
  -> Daily-Line-Core
       -> All Bets
       -> EdgeStack
       -> DailyLinePublicationPackage
  -> report / infographic / website / TDLA
```

Live capability is a separate sibling lineage:

```text
Daily-Data-Live-Core transport
  -> sport-owned live state/features/models/gates
  -> live decision package
```

Live may compare with pregame output, but may never rewrite the pregame prediction ledger.

## Authorization rule

A boundary file does **not** create a repository, register it with the Bridge, authorize implementation, certify architecture, or grant production authority. Future sport work begins only after explicit owner direction and a bounded one-repository turn.
