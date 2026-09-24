# Daily NBA Build Boundary V1

**Status:** PLANNED — IMPLEMENTATION NOT AUTHORIZED BY THIS FILE  
**Planned repository:** `OneVillage83/Daily-NBA`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authorization

Do not begin NBA implementation until the owner explicitly authorizes repository creation/registration and SB-0 local governance/architecture documents exist.

## Mission

Model NBA games and player props from possession, lineup, rotation, tracking, availability and schedule context, treating minutes/opportunity uncertainty as a first-class driver.

## Canonical sport truth

- teams, players, coaches, rosters, games, venues, officials, lineups and substitutions
- active/inactive, starting lineup, rotation and minute-role revisions
- overtime/rule versions and schedule changes
- traded-player team history is effective-dated

## Factual evidence

- PBP, possessions, box scores, lineup/substitution data
- shot-location/tracking data where licensed
- injuries/availability, starting lineups, rotation roles and minute restrictions
- attempts/locations/quality components, rebounds, turnovers, fouls/free throws and pace
- travel/rest/back-to-back, altitude, home/away and schedule density

## Feature families

- possession-adjusted offense/defense and four-factor-style components
- transition/half-court and shot-profile features
- lineup/on-off and internally estimated adjusted-plus-minus-style effects with shrinkage
- player minutes/opportunity, usage, assist/rebound chances, 3PA/rim attempts and foul risk
- replacement/role changes and opponent lineup/matchup
- rest/travel/back-to-back/altitude

## Target/market universe

- moneyline, spread, total, team totals
- quarter/half markets when supported
- player points, rebounds, assists, 3PM, PRA/PR/PA/RA
- steals, blocks, turnovers and other lower-frequency props only after separate calibration proof

## Model Zoo direction

- team-strength and possession-efficiency baselines
- hierarchical lineup/player impact and minutes-allocation models
- nonlinear game/player models
- shot-attempt/make, rebound, assist and usage specialists
- possession/game simulation with overtime and player minutes
- learned mixture-of-experts with target/role/opponent/data-quality context

## Full build outline

| Phase | NBA requirement |
|---|---|
| SB-0 | Create local constitution/roadmap/status before source code; register repo only after owner authorization. |
| SB-1 | Canonicalize team/player/roster/game/lineup/substitution/rule/settlement identity. |
| SB-2 | Acquire immutable PBP/lineup/tracking/availability/schedule evidence with PIT revisions. |
| SB-3 | Reconstruct active roster, expected starters/rotation/minutes restrictions and game context. |
| SB-4 | Build possession, lineup, player-impact, minutes/opportunity, matchup and rest/travel features. |
| SB-5 | Define game/quarter/half/player market taxonomy and deterministic settlement. |
| SB-6 | Build team/pace/efficiency and player-minute/opportunity baselines. |
| SB-7 | Add shot/rebound/assist/usage/matchup/injury specialists with OOS evidence. |
| SB-8 | Simulate possessions, score margin/total, overtime, minutes and joint player outcomes. |
| SB-9 | Calibrate/freeze independent NBA Unified Line and player distributions. |
| SB-10 | Join DDC evidence only after freeze for value/EV/timing. |
| SB-11 | Apply NBA Recommendation Gate and seal SportDecisionPackage/joint refs. |
| SB-12 | Evaluate by market, player role, rest/injury and season phase; settle every gate state. |
| SB-13 | Prove manual slate -> DLC/report/infographic handoff. |
| SB-14 | Later live sibling with score/clock/possession/fouls/timeouts/lineups/substitutions. |
| SB-15 | TDLA automation only after manual certification and retry/equivalence proof. |

## Simulation / joint evidence

- possession-level or sufficiently faithful game simulation for score/spread/total
- player minutes/rotation uncertainty propagates into props
- joint samples preserve points/PRA/team-total, teammate usage substitution, blowout and overtime relationships

## Uncertainty

Questionable tags, late scratches, minutes limits, rotation changes and back-to-backs must materially alter uncertainty. Player props cannot hide opportunity uncertainty behind one point estimate.

## Live boundary

Live NBA tracks score, clock, possession, fouls, timeouts, lineups/substitutions and remaining minutes/opportunity. It writes separate live snapshots.

## Anti-drift rules

- do not use proprietary third-party predictive ratings as independent truth
- do not clone football architecture
- do not use market-implied lines to set independent minutes/team strength
- do not implement EdgeStack in Daily-NBA

## Bridge stop conditions

Stop/escalate when expected-minutes/availability state cannot be reconstructed PIT-correctly, settlement differs by provider and is unresolved, tracking/licensing semantics are unclear, or a shared basketball abstraction would force NBA assumptions onto WNBA/NCAAB.

## Exit criteria

- independent game/player distributions calibrated OOS
- minutes/rotation/availability uncertainty validated
- supported-market settlement and package replay pass
- live and automation separately certified
