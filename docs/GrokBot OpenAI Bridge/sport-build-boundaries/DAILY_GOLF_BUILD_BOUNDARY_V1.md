# Daily Golf Build Boundary V1

**Status:** EXISTING EMPTY REPOSITORY — ARCHITECTURE / IMPLEMENTATION NOT AUTHORIZED BY THIS FILE  
**Repository:** `OneVillage83/Daily-Golf`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authorization / tour scope

Daily-Golf is tour/tournament/rule aware. PGA Tour, LPGA, DP World Tour, LIV, majors and any other approved circuits may share infrastructure only after tour-specific data/rules/calibration are proven. Repository existence does not authorize any one tour as the default production scope.

## Mission

Produce calibrated golf tournament, finishing-position, matchup, cut and supported round/player-prop distributions from player skill, strokes-gained components, course setup, field strength, weather/tee-wave and schedule context.

## Canonical sport truth

- players, tours, tournaments, courses, rounds, holes, tee times, groups and fields
- course routing/setup and par
- cut/no-cut rules, playoff rules and tournament format
- withdrawals, disqualifications, substitutions/alternates where applicable
- shotgun vs traditional starts and multi-course events
- weather delays/suspensions/resumptions
- provider settlement versions
- provider IDs remain crosswalks

## Factual evidence

- round/hole scores and shot-level data where licensed/available
- strokes-gained components or internally derived shot-quality measures
- driving distance/accuracy, approach proximity, scrambling and putting evidence
- course architecture/setup, yardage, rough, green type/speed and historical scoring
- field strength
- tee times/waves/groups
- wind, temperature, precipitation and delay state
- travel/rest/recent workload and course history
- injury/withdrawal evidence when PIT-valid

## Feature families

- latent player skill with recency and hierarchical shrinkage
- strokes-gained off-tee, approach, around-green and putting components
- course/shot-demand fit derived from repeatable features rather than narrative labels
- field-strength adjustment
- weather and tee-wave exposure
- course-specific scoring distribution
- travel/rest/recent-event load
- cut probability and weekend-field conditional state

## Target / market universe

- outright winner
- top 5 / top 10 / top 20 / other finishing-position markets
- make/miss cut
- head-to-head matchup
- 3-ball / group matchup
- round leader where supported
- player round score / birdies / bogeys / finishing position and other props only after data/settlement certification

## Model Zoo direction

- player-rating / strokes-gained state-space baselines
- hierarchical Bayesian player/course/tour models
- nonlinear player-course-weather models
- round-score distributions
- cut and finishing-position models
- matchup specialists
- whole-field Monte Carlo tournament simulation with cut/playoff rules
- weather/tee-wave specialists
- learned ensemble from frozen chronological OOS predictions

## Full build outline

| Phase | Golf requirement |
|---|---|
| SB-0 | Bootstrap tour/tournament registry, local governance and architecture before code. |
| SB-1 | Canonicalize player/tour/tournament/course/round/hole/field/cut/playoff/settlement identity. |
| SB-2 | Acquire PIT scoring/shot/course/tee-time/field/weather/withdrawal evidence. |
| SB-3 | Reconstruct field, tee-wave, course setup, start state and known availability at cutoff. |
| SB-4 | Build player-skill/strokes-gained/course/weather/field/travel features. |
| SB-5 | Define outright/top-N/cut/matchup/round/prop market contracts. |
| SB-6 | Establish player-skill, round-score and cut baselines. |
| SB-7 | Add course-fit, weather-wave, matchup and component specialists with OOS proof. |
| SB-8 | Simulate full field round-by-round through cut and playoff rules. |
| SB-9 | Calibrate/freeze independent Golf TDL Unified Line for each market. |
| SB-10 | Join DDC market evidence only after freeze; value/EV/timing/withdrawal risk. |
| SB-11 | Apply Golf Recommendation Gate and export SportDecisionPackage/joint refs. |
| SB-12 | Settle/evaluate by tour, course type, field strength, round and market class. |
| SB-13 | Prove manual tournament -> DLC/report handoff. |
| SB-14 | Later live sibling hole/round state with remaining-course/weather distributions. |
| SB-15 | Automate only after manual certification and delay/withdrawal/restart recovery proof. |

## Simulation / joint evidence

- simulate all players against one tournament/course/weather state so finishing-position probabilities are coherent
- implement cut/no-cut, ties and playoff semantics exactly
- matchup/top-N/cut/outright dependencies derive from the same field simulation where practical
- tee-wave weather differences remain PIT-bound and revision-aware

## Uncertainty

Weather, withdrawals/injury, changing course setup, smaller tours, sparse shot-level coverage and volatile putting/short-game components require explicit uncertainty and shrinkage.

## Live boundary

Live Golf may use completed holes/shots/rounds, current leaderboard, remaining course, tee position and updated weather. Suspensions and resumed rounds create new live state; they do not alter the original pre-tournament snapshot.

## Anti-drift rules

- do not use sportsbook odds as player strength
- do not treat "course history" as causal without component-based OOS evidence
- do not transfer PGA calibration to LPGA/other tours by assumption
- do not ignore field-wide dependency in outright/top-N markets
- do not build EdgeStack here

## Bridge stop conditions

Stop/escalate when tournament/cut/playoff format is unclear, shot-data licensing/PIT is unresolved, tee-wave/weather history cannot be reconstructed, or a tour-transfer assumption lacks OOS validation.

## Exit criteria

- tournament/cut/playoff settlement replay is exact
- field simulation and supported markets show OOS calibration
- tour/course/weather uncertainty is explicit
- SportDecisionPackage is DLC-compatible
