# Daily MLB Build Boundary V1

**Status:** EXISTING REPOSITORY — COORDINATION OVERLAY ONLY  
**Repository:** `OneVillage83/Daily-MLB`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authority

Daily-MLB already has active audit/architecture/implementation authority. Read its `AGENTS.md`, `CODEX_START_HERE.md`, latest status/audit/freeze documents, and current Git truth before work. Do **not** restart MLB from this outline or replace local architecture with SB numbering.

## Mission

Produce calibrated pregame baseball probability distributions and individual-market decisions from baseball-native evidence, then seal them for Daily-Line-Core.

## Canonical sport truth

- teams, players, rosters, games/series, venues, batting orders, pitcher roles
- doubleheaders, postponed/rescheduled and suspended/resumed games
- probable/confirmed starter revisions and lineup revisions
- extra-inning/rule and provider settlement versions
- provider IDs remain crosswalks, not canonical Daily Line identity

## Factual evidence

- pitch-level Statcast/tracking, plate appearances, batted-ball events and play-by-play
- roster/transaction/injury/availability evidence, lineups, probable/confirmed pitchers
- pitch mix, velocity, movement, whiff/chase/contact, handedness and times-through-order context
- hitter contact quality, expected-result components, discipline, platoon, baserunning and defense
- bullpen usage, leverage, roles, availability and workload
- park/roof/weather/air/wind, travel/rest/time-zone and schedule context
- umpire effects only when PIT/source quality and incremental value are demonstrated

## Feature families

- opponent/park-adjusted offense and platoon strength with shrinkage
- pitcher K-BB, command, whiff/chase, velocity/movement, pitch mix, contact quality and workload
- hitter expected-contact/quality measures, launch/barrel/hard-hit, discipline and pitch-type matchup
- bullpen depth/fatigue/leverage availability
- lineup strength/order position and confirmed-vs-projected uncertainty
- defense/catching/baserunning when evidence supports it
- park/weather/travel/rest effects with PIT validation

## Target/market universe

Represent from the start, but certify support individually:

- full-game moneyline, run line, total, team totals
- first-five ML/run line/total and other inning-window markets with explicit settlement
- pitcher strikeouts, outs, walks, hits allowed and related props
- hitter hits, total bases, HR, walks, runs/RBI and other props only after data/calibration support

## Model Zoo direction

- team-strength/Elo-style and run-environment baselines
- hierarchical/Bayesian team, pitcher, batter and bullpen models
- nonlinear/gradient-boosted game and prop models
- pitcher-batter/pitch-type and sequence/count specialists
- Poisson/negative-binomial or richer run models
- inning/plate-appearance simulation
- pitcher-outs/removal survival and hitter-opportunity models
- learned mixture-of-experts from frozen forward/OOS predictions only

## Full build outline

| Phase | MLB requirement |
|---|---|
| SB-0 | Preserve current Daily-MLB audit/resume/certification chain; no competing roadmap. |
| SB-1 | Canonicalize games/doubleheaders/suspensions, teams/players/rosters/lineups/pitcher roles and settlement. |
| SB-2 | Retain immutable pitch/PBP/roster/lineup/availability/weather/travel evidence with available-at semantics. |
| SB-3 | Reconstruct pregame lineup, starter, bullpen availability, roster and venue/weather state. |
| SB-4 | Version pitcher/batter/bullpen/lineup/park/weather/travel features. |
| SB-5 | Freeze market taxonomy and settlement for game/F5/team-total/player targets. |
| SB-6 | Establish team-strength/run-distribution and prop baselines under walk-forward validation. |
| SB-7 | Add pitcher-batter, bullpen, hitter-opportunity, pitcher-outs/K and other specialists with OOS proof. |
| SB-8 | Produce run/inning/player distributions and same-event joint samples. |
| SB-9 | Calibrate and freeze independent MLB TDL Unified Line before market evidence. |
| SB-10 | Join DDC quotes after freeze; compute value/EV/timing and baseball-specific risk. |
| SB-11 | Apply deterministic sport Recommendation Gate and seal SportDecisionPackage/joint refs. |
| SB-12 | Settle every forecast/gate state; evaluate calibration plus downstream CLV/EV/ROI/miss attribution. |
| SB-13 | Prove manual daily slate -> DLC/report/infographic end-to-end. |
| SB-14 | Later live inning/base-out/count/pitcher/bullpen sibling; never mutate pregame. |
| SB-15 | TDLA shadow -> supervised -> explicit production equivalence/failure/idempotency proof. |

## Simulation / joint evidence

- model score/run distributions, extra innings, starter duration, bullpen paths and player opportunities
- preserve deterministic seed/config/model/data provenance
- export joint evidence for starter props + outcomes, hitter props + totals and same-game combinations only when validated

## Uncertainty

Lineup not confirmed, starter uncertainty, bullpen ambiguity, weather/roof uncertainty, stale roster evidence and small-sample pitch/platoon changes must widen uncertainty or degrade support rather than fabricate certainty.

## Live boundary

Live MLB may use inning, outs, bases, count, score, current pitcher, pitch count, bullpen availability, leverage and remaining lineup path. It consumes Daily-Data-Live-Core transport and writes a separate live ledger.

## Anti-drift rules

- no All Bets/EdgeStack implementation inside Daily-MLB
- no market-line input to the independent baseball forecast
- no requirement to finish live before pregame certification
- no generic rewrite that discards current audited Daily-MLB work

## Bridge stop conditions

Stop/escalate if current Daily-MLB authority conflicts with a task, game/market/settlement identity is ambiguous, PIT/licensing cannot be proven, or a market-aware shortcut would contaminate the independent line.

## Exit criteria

- local Daily-MLB manual pipeline reaches its own production certification
- supported game/F5/player markets have PIT OOS calibration and settlement evidence
- sealed SportDecisionPackage is DLC-compatible without DLC reconstructing MLB truth
- live and automation remain separately certified extensions
