# Daily NCAAWB Build Boundary V1

**Status:** EXISTING EMPTY REPOSITORY — ARCHITECTURE / IMPLEMENTATION NOT AUTHORIZED BY THIS FILE  
**Repository:** `OneVillage83/Daily-NCAAWB`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authority / relationship to Daily-NCAAB

Daily-NCAAWB is the separate women's college-basketball sport repository. Daily-NCAAB must not absorb NCAAWB production authority. The two repos may later share proven basketball infrastructure, but identities, data quality, models, calibration, promotion evidence and Recommendation Gates remain independently certifiable.

## Mission

Model women's college basketball with competition-aware team strength, tempo, roster/transfer continuity, neutral-site/tournament context and explicit small-sample/data-quality uncertainty.

## Canonical sport truth

- institutions/teams, players, coaches, conferences, rosters, games, venues and tournaments
- NCAA division/competition scope and postseason structure
- transfer/eligibility, conference membership and coaching changes effective-dated
- neutral-site and tournament rules
- provider IDs remain crosswalks

## Factual evidence

- play-by-play and box-score evidence
- possessions, participation/lineup/minutes where available
- rosters, transfers, injuries/availability and returning production
- shooting, turnovers, offensive rebounding, fouls/free throws and opponent context
- schedule strength, rest/travel, neutral sites, tournaments, altitude/venue
- coaching/rotation changes
- data-quality grading for teams/players with incomplete feeds

## Feature families

- opponent-adjusted offensive/defensive efficiency and tempo
- effective shooting, turnover, rebounding and free-throw-rate components
- roster continuity/transfers/returning production
- player roles/usage/minutes where coverage supports them
- conference strength and schedule quality with hierarchical shrinkage
- neutral-site/tournament/rest/travel context
- explicit sparse-data confidence features

## Target / market universe

- moneyline, spread, total, team totals
- halves when data and settlement support them
- player props only after player identity/participation/provider history is independently certified
- tournament/postseason markets with explicit neutral-site/overtime semantics

## Model Zoo direction

- hierarchical team-strength / efficiency / tempo models
- Bayesian early-season and sparse-team shrinkage
- roster-continuity / transfer / returning-production priors
- nonlinear game models
- possession/score simulation
- shooting/rebounding/turnover/foul specialists where event data supports them
- learned ensemble trained/evaluated on NCAAWB OOS evidence; no automatic NCAAB weight transfer

## Full build outline

| Phase | NCAAWB requirement |
|---|---|
| SB-0 | Bootstrap separate local authority, roadmap, status and architecture. |
| SB-1 | Canonicalize institution/team/player/conference/tournament/rule/settlement identity. |
| SB-2 | Acquire PIT PBP/box/roster/transfer/availability/schedule/venue evidence with quality grades. |
| SB-3 | Reconstruct roster/rotation/availability and pregame competition state. |
| SB-4 | Build opponent-adjusted efficiency/tempo/roster/neutral-site/travel features. |
| SB-5 | Define game/half/player support and deterministic settlement. |
| SB-6 | Establish NCAAWB-specific hierarchical baselines and early-season priors. |
| SB-7 | Add roster/shooting/rebounding/pace/tournament specialists with OOS proof. |
| SB-8 | Simulate possessions, score, overtime and player outcomes where supported. |
| SB-9 | Calibrate/freeze independent NCAAWB TDL Unified Line. |
| SB-10 | Join DDC market evidence only after freeze. |
| SB-11 | Apply NCAAWB Recommendation Gate and export SportDecisionPackage. |
| SB-12 | Evaluate by conference, season phase, neutral site, data quality and market. |
| SB-13 | Prove manual slate/tournament -> DLC/report handoff. |
| SB-14 | Later live sibling with score/clock/possession/fouls/timeouts and feed-quality state. |
| SB-15 | Automate only after manual certification and large-slate recovery/idempotency proof. |

## Simulation / joint evidence

- account for college pace variance, overtime and large strength gaps
- propagate roster/rotation uncertainty
- player joint evidence remains unsupported until minutes/participation coverage is sufficient
- do not borrow NCAAB correlation coefficients without NCAAWB validation

## Uncertainty

Early season, roster turnover, sparse lower-profile teams, incomplete participation feeds and neutral-site tournament conditions receive explicit wider uncertainty.

## Live boundary

Live NCAAWB may share generic basketball state components with NBA/WNBA/NCAAB only when semantics are truly common. Live models/calibration remain NCAAWB-specific.

## Anti-drift rules

- do not merge this repository's statistical authority into Daily-NCAAB
- do not transfer men's college model weights/calibration by assumption
- do not force player-prop coverage without participation/settlement history
- do not build DLC product logic here

## Bridge stop conditions

Stop/escalate when NCAAB/NCAAWB ownership is being blurred, player participation history is inadequate, shared basketball code hides different data/rules, or market evidence is proposed as independent strength input.

## Exit criteria

- NCAAWB-specific OOS calibration and degradation behavior pass
- tournament/neutral-site and settlement replay are exact
- supported player props have separate evidence
- sealed SportDecisionPackage passes DLC handoff
