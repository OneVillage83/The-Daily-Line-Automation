# Daily NFL Build Boundary V1

**Status:** EXISTING REPOSITORY — F-0 THROUGH F-24 LOCAL ARCHITECTURE GOVERNS  
**Repository:** `OneVillage83/Daily-NFL`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authority

Daily-NFL already has governing F-0 through F-24 architecture and `AGENTS.md`. Those files are authoritative. This is a Bridge checklist only and may not reinterpret locked concepts such as play taxonomy/`PLAY_EXECUTION`, PIT rules, model lineage, or certified football contracts.

## Mission

Produce calibrated football outcome and player-prop distributions from football-native play, tracking, availability and context while preserving an independent TDL Unified Line.

## Canonical sport truth

- teams, players, coaches, roster/depth roles, games, drives, possessions, plays, venues/officials
- preserve the locked play taxonomy
- kickoff/reschedule/cancellation and active/inactive/depth revisions are versioned
- provider IDs remain crosswalks

## Factual evidence

- play-by-play and drive state
- snaps/routes/targets/carries/participation
- internally derived EPA/success/explosive/CPOE-like evidence
- tracking/Next Gen-type factual measures where licensed
- pressure/sack/coverage/run-fit/YAC context
- injuries, practice, actives/inactives, depth chart, OL combinations and usage
- weather/wind/temp/precipitation, surface, rest/travel/time zone
- coaching, neutral pace and play-calling tendencies

## Feature families

- opponent-adjusted offense/defense/special-teams strength
- early-down/pass-down, situation and pace splits
- QB accuracy/decision/pressure response
- receiver route/target quality and rusher efficiency
- OL/pass-protection and defense pressure/coverage
- personnel/formation/motion/play-action when supported
- player opportunity: attempts/targets/routes/carries/red-zone/end-zone usage
- injury/replacement/depth and weather/travel effects

## Target/market universe

- moneyline, spread, total, team totals
- half/quarter markets when settlement/support are certified
- passing yards/TD/INT/completions/attempts
- rushing yards/attempts
- receiving yards/receptions/targets
- anytime/first TD only with participant/opportunity/joint-event support
- kicker/defensive/special markets only after separate certification

## Model Zoo direction

- team power/Elo-style and opponent-adjusted EPA baselines
- hierarchical team/player/context models
- nonlinear/gradient-boosted game and prop models
- drive/play transition and scoring models
- player opportunity/usage specialists
- QB/receiver/rusher/pressure/red-zone/TD/weather specialists
- game simulation producing score, possession and player-stat distributions
- mixture-of-experts preserving target/context specialists

## Full build outline

| Phase | NFL requirement |
|---|---|
| SB-0 | Follow Daily-NFL AGENTS/F-0..F-24; no competing architecture. |
| SB-1 | Maintain canonical game/team/player/roster/play/drive identity, rules and settlement. |
| SB-2 | Persist raw PBP/tracking/participation/injury/weather/roster evidence with PIT provenance. |
| SB-3 | Reconstruct roster/inactive/depth, drive/play/game and pregame availability state. |
| SB-4 | Version EPA/usage/tracking/matchup/weather/travel features under leakage tests. |
| SB-5 | Maintain game/player target taxonomy, thresholds and settlement contracts. |
| SB-6 | Preserve reproducible team-strength/EPA/player-opportunity baselines. |
| SB-7 | Add QB/receiver/rusher/pressure/TD specialists only with target-specific OOS evidence. |
| SB-8 | Generate game/drive/play/player joint distributions. |
| SB-9 | Calibrate and freeze independent NFL TDL Unified Line. |
| SB-10 | Join DDC market evidence after freeze for value/line timing/risk. |
| SB-11 | Apply sport Recommendation Gate and seal SportDecisionPackage/joint refs. |
| SB-12 | Settle/evaluate every supported prediction including PASS/AVOID. |
| SB-13 | Prove manual full-slate output and DLC/report handoff. |
| SB-14 | Later live down/distance/field/clock/score/possession/player-remaining-distribution sibling. |
| SB-15 | TDLA shadow -> supervised -> production only after local manual certification/equivalence. |

## Simulation / joint evidence

- score margin/total, possession/drive and player opportunity/stat distributions
- capture QB/receiver, team-total/TD, game-script/rush-pass and related same-event correlations when published
- preserve random seed, model version and exact cutoff state

## Uncertainty

QB/inactive/depth uncertainty, weather, OL combinations, role ambiguity and limited samples must be explicit. Player props carry opportunity/snap uncertainty, not only conditional efficiency uncertainty.

## Live boundary

Live NFL may model score, clock, quarter, down/distance, field position, possession, timeouts, personnel/availability, drive state and remaining usage. Live outputs are new immutable snapshots.

## Anti-drift rules

- do not duplicate DDC provider acquisition or DMC generic lifecycle
- do not let market lines contaminate football-only/Unified Line inputs
- do not replace F-0..F-24 with a simplified new architecture
- do not build EdgeStack inside Daily-NFL

## Bridge stop conditions

Stop/escalate if work conflicts with F-0..F-24/current resume truth, provider IDs are becoming canonical identity, PIT/revision lineage cannot be proven, or a player market lacks deterministic settlement/opportunity support.

## Exit criteria

- repo-local architecture/implementation certification gates satisfied
- full-slate supported markets have OOS calibration, uncertainty, settlement and gate evidence
- same-event joint evidence validated where published
- SportDecisionPackage hands off cleanly to DLC; live/automation certified separately
