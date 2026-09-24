# Daily NCAAB Build Boundary V1

**Status:** EXISTING EMPTY REPOSITORY — ARCHITECTURE / IMPLEMENTATION NOT AUTHORIZED BY THIS FILE  
**Repository:** `OneVillage83/Daily-NCAAB`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authority / relationship to Daily-NCAAWB

**Daily-NCAAB is men's college basketball only.** Women's college basketball belongs to the separate `OneVillage83/Daily-NCAAWB` repository. The two repos may later share proven generic basketball infrastructure, but identities, data pipelines, models, calibration, market support, Recommendation Gates, settlement evidence and production authority remain independently certifiable.

## Mission

Model men's college basketball across a large heterogeneous team population with tempo, schedule-strength, roster/transfer, neutral-site and small-sample uncertainty.

## Canonical sport truth

- institutions/teams, players, coaches, conferences, rosters, games, venues and tournaments
- conference membership, transfer/eligibility and neutral-site/tournament rules effective-dated
- men's college-basketball models/calibration remain separate from Daily-NCAAWB even when generic tooling is shared

## Factual evidence

- PBP/box score, possessions and lineup/participation where available
- roster/transfer/injury/availability
- tempo, shooting/attempt context, turnovers, offensive rebounds, fouls/free throws
- schedule strength, travel/rest, neutral site, tournament setting, altitude/venue and coaching/rotation changes

## Feature families

- opponent-adjusted offensive/defensive efficiency and tempo
- effective shooting, turnover, rebounding and free-throw rate with shrinkage
- roster continuity, transfers, returning production, player roles and coaching-system context
- neutral-site/tournament/rest/travel and schedule-strength
- explicit data-quality state for sparse PBP/lineup coverage

## Target/market universe

- moneyline, spread, total, team totals
- halves where support/settlement are certified
- player props only for competitions/providers with reliable identity, participation and history
- tournament/postseason markets preserve neutral-site/overtime/rule semantics

## Model Zoo direction

- hierarchical team-strength/efficiency and tempo with conference/competition partial pooling
- Bayesian early-season shrinkage and roster-continuity/transfer priors
- nonlinear game models and possession/score simulation
- shooting/rebounding/turnover/foul/pace specialists where event data supports them
- men's college-basketball calibration/ensemble authority remains local to Daily-NCAAB

## Full build outline

| Phase | NCAAB requirement |
|---|---|
| SB-0 | Bootstrap local governance/architecture for men's college basketball before coding. |
| SB-1 | Canonicalize men's institution/team/player/conference/tournament identity and rules. |
| SB-2 | Acquire PIT PBP/box/roster/transfer/availability/schedule/venue evidence with quality grading. |
| SB-3 | Reconstruct roster/rotation/availability and pregame competition state. |
| SB-4 | Build opponent-adjusted efficiency/tempo/four-factor/roster/neutral-site/travel features. |
| SB-5 | Define game/half/player support and settlement by competition/provider. |
| SB-6 | Establish hierarchical efficiency/tempo baselines and early-season priors. |
| SB-7 | Add roster/shooting/pace/rebounding/foul/tournament specialists with OOS proof. |
| SB-8 | Simulate possessions/score/overtime and player outcomes where supported. |
| SB-9 | Calibrate/freeze the independent men's NCAAB Unified Line. |
| SB-10 | Join DDC market evidence after freeze for value/timing/gate inputs. |
| SB-11 | Apply college-basketball Recommendation Gate and export SportDecisionPackage. |
| SB-12 | Evaluate by conference/competition/season phase/neutral site/market/data quality. |
| SB-13 | Prove manual large-slate/tournament publication and DLC handoff. |
| SB-14 | Later live sibling with score/clock/possession/fouls/timeouts and feed-quality state. |
| SB-15 | Automate after manual certification and large-slate recovery/idempotency proof. |

## Simulation / joint evidence

- reflect college tempo variance, overtime and large team-strength disparities
- player joint evidence remains unsupported until participation/minutes quality is sufficient
- no joint-distribution or calibration authority is shared with Daily-NCAAWB by default

## Uncertainty

Early season, roster turnover, low-major/sparse-data teams and neutral-site tournament conditions receive wider uncertainty. Missing lineup/participation quality must be visible in support/gates.

## Live boundary

Live college basketball may share generic basketball transport/components only after semantic equivalence is demonstrated. Feed reliability remains competition-specific.

## Anti-drift rules

- no NBA minutes/rotation assumptions forced onto college teams
- no pooling with Daily-NCAAWB merely to increase sample size
- no player-prop support without participation/settlement history
- no DLC product assembly here

## Bridge stop conditions

Stop/escalate when work would move women's college-basketball authority into Daily-NCAAB, tournament rules are ambiguous, player identity/participation is insufficient, a shared abstraction hides materially different rules/data quality, or market odds are proposed as independent team-strength inputs.

## Exit criteria

- game predictions OOS calibrated across meaningful team/conference bands
- competition/data-quality degradation proven
- player props explicitly unsupported until separate certification
- SportDecisionPackage and settlement replay pass
