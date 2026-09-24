# Daily Soccer Build Boundary V1

**Status:** PLANNED — IMPLEMENTATION NOT AUTHORIZED BY THIS FILE  
**Planned repository:** `OneVillage83/Daily-Soccer`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authorization / competition architecture

Daily-Soccer is competition-registry driven rather than hard-coded to one league. Men's and women's competitions share infrastructure only where rules/data semantics align; each competition/model domain requires its own calibration and data-quality evidence.

## Mission

Model soccer across domestic/international competitions from event/xG, tactical, lineup, player-availability, travel/congestion and competition-rule evidence, with correct draw and knockout semantics.

## Canonical sport truth

- clubs/national teams, players, managers, competitions, seasons, fixtures/legs, venues and officials
- promotion/relegation, transfers/loans, suspensions and competition membership are effective-dated
- manager changes and tactical regime changes are time-versioned
- competition rules for points, substitutions, extra time, penalties and aggregate legs are versioned
- women's competitions (for example NWSL/WSL and later supported leagues) use explicit competition namespace and independent calibration

## Factual evidence

- event data: shots, locations, chances/assists, possession sequences, set pieces, cards/fouls and substitutions
- lineups/formations, injuries/suspensions, player minutes/roles, transfers and manager changes
- internally derived xG/xA/shot-quality and pressing/possession/progression features from factual event data where licensed
- rest, travel, fixture congestion, altitude/weather/surface, home/away/neutral and competition context

## Feature families

- team attack/defense strength with competition/opponent adjustment and home advantage
- xG for/against, shot volume/quality and finishing/shot-stopping residuals with shrinkage
- possession/progression/pressing/set-piece and formation/lineup effects where supported
- player availability/minutes/role and transfer/manager regime
- fixture congestion/travel/rest and cross-competition strength uncertainty

## Target/market universe

- 1X2
- draw-no-bet
- Asian handicap
- totals
- both teams to score
- team totals
- half markets where settlement is explicit
- corners/cards and player shots/goals/assists only when event/provider coverage supports PIT calibration
- knockout qualification/advance markets only with competition-rule-specific simulation/settlement

## Model Zoo direction

- Poisson, bivariate Poisson and Dixon-Coles-style baselines with competition-specific validation
- xG-based attack/defense and hierarchical team/player models
- nonlinear fixture models
- hazard/time-to-goal models where justified
- lineup/player-availability and set-piece/discipline specialists
- match simulation supporting draws, added time, ET/penalties/aggregate ties
- competition-aware learned ensemble; no assumption that one league's calibration transfers to another

## Full build outline

| Phase | Soccer requirement |
|---|---|
| SB-0 | Create competition registry, local constitution and ownership map before code. |
| SB-1 | Canonicalize teams/players/competitions/fixtures/legs/rules/transfers/suspensions. |
| SB-2 | Acquire PIT event/lineup/availability/competition/weather/travel evidence with licensing/quality state. |
| SB-3 | Reconstruct expected/confirmed lineups, formation/availability and competition/tie state. |
| SB-4 | Build xG/attack-defense/lineup/tactical/set-piece/congestion/travel features. |
| SB-5 | Define 1X2/AH/totals/BTTS/team-total/corners/cards/player/qualification market contracts by competition. |
| SB-6 | Establish Poisson/xG/team-strength baselines per competition family. |
| SB-7 | Add lineup/player/set-piece/discipline/congestion/knockout specialists. |
| SB-8 | Simulate score paths, draws, added time and competition-specific ET/PK/aggregate rules. |
| SB-9 | Calibrate/freeze independent Soccer Unified Line by competition/data regime. |
| SB-10 | Join DDC market evidence after freeze for value/timing/risk. |
| SB-11 | Apply soccer Recommendation Gate and export competition-aware SportDecisionPackage. |
| SB-12 | Evaluate by league/competition, home/away, total band, lineup certainty, season phase and market. |
| SB-13 | Prove manual multi-competition slate -> DLC/report handoff. |
| SB-14 | Later live sibling using minute/score/cards/substitutions/shots/xG/manpower/tie state. |
| SB-15 | Automate only after competition-specific manual certification and schedule/time-zone recovery proof. |

## Simulation / joint evidence

- full-time score distributions preserve draw probability
- knockout competitions preserve aggregate/extra-time/penalty semantics
- corners/cards/player markets require separate validated process models, not score-only inference
- same-match dependency evidence exported only when calibrated

## Uncertainty

Unconfirmed lineups, transfer windows, manager changes, fixture congestion and cross-league strength comparisons require explicit uncertainty. A market may be supported in one competition and unsupported in another.

## Live boundary

Live Soccer may use minute/score/red-card state, substitutions, shots/xG, possession/territory and remaining match/tie context. Red cards and aggregate state may dramatically change live distributions but never revise the pregame snapshot.

## Anti-drift rules

- no hard-coding around one league
- no pooling men's/women's or separate leagues without validation
- no public odds or third-party predictive outputs as hidden independent inputs
- factual third-party event measures require explicit semantics/licensing
- do not collapse 90-minute, incl-ET, qualification and Asian-handicap settlement

## Bridge stop conditions

Stop/escalate when competition/leg/ET/penalty rules are ambiguous, lineup/event PIT or licensing is unclear, a model/calibrator is transferred across competitions without OOS evidence, or a market lacks reliable event/provider history.

## Exit criteria

- competition registry/rule engine and PIT replay exact
- supported competitions/markets show OOS calibration and explicit degradation
- knockout/aggregate settlement and simulation pass
- SportDecisionPackage remains competition-aware and DLC-compatible
