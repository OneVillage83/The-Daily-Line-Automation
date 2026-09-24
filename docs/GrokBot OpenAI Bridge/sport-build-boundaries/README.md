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

The current GitHub sport-repository catalog is:

- `Daily-MLB` -> `DAILY_MLB_BUILD_BOUNDARY_V1.md` — existing active repo; local Daily-MLB authority wins
- `Daily-NFL` -> `DAILY_NFL_BUILD_BOUNDARY_V1.md` — existing active repo; F-0 through F-24 local authority wins
- `Daily-NCAAF` -> `DAILY_NCAAF_BUILD_BOUNDARY_V1.md` — existing active repo; local F-layer architecture/overlay wins
- `Daily-NBA` -> `DAILY_NBA_BUILD_BOUNDARY_V1.md` — existing empty repo
- `Daily-WNBA` -> `DAILY_WNBA_BUILD_BOUNDARY_V1.md` — existing empty repo
- `Daily-NCAAB` -> `DAILY_NCAAB_BUILD_BOUNDARY_V1.md` — existing empty repo; **men's college basketball**
- `Daily-NCAAWB` -> `DAILY_NCAAWB_BUILD_BOUNDARY_V1.md` — existing empty repo; **women's college basketball**
- `Daily-NHL` -> `DAILY_NHL_BUILD_BOUNDARY_V1.md` — existing empty repo
- `Daily-Soccer` -> `DAILY_SOCCER_BUILD_BOUNDARY_V1.md` — existing empty repo; multi-competition, including separately validated men's and women's competitions
- `Daily-Tennis` -> `DAILY_TENNIS_BUILD_BOUNDARY_V1.md` — existing empty repo
- `Daily-Golf` -> `DAILY_GOLF_BUILD_BOUNDARY_V1.md` — existing empty repo
- `Daily-MMA` -> `DAILY_MMA_BUILD_BOUNDARY_V1.md` — existing empty repo
- `Daily-Boxing` -> `DAILY_BOXING_BUILD_BOUNDARY_V1.md` — existing empty repo
- `Daily-Motorsports` -> `DAILY_MOTORSPORTS_BUILD_BOUNDARY_V1.md` — existing empty repo; series-adapter architecture
- `Daily-Esports` -> `DAILY_ESPORTS_BUILD_BOUNDARY_V1.md` — existing empty repo; title/patch-adapter architecture

`FUTURE_SPORT_TEMPLATE_V1.md` remains the required bootstrap template if another sport repo is added later.

Shared/core repositories such as `Daily-Data-Core`, `Daily-Model-Core`, `Daily-Line-Core`, validation, website, and automation are intentionally not listed as sports.

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
