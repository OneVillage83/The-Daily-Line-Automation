# Daily NHL Build Boundary V1

**Status:** EXISTING EMPTY REPOSITORY — ARCHITECTURE / IMPLEMENTATION NOT AUTHORIZED BY THIS FILE  
**Repository:** `OneVillage83/Daily-NHL`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authorization

NHL implementation begins only after explicit owner authorization, repository registration, and local SB-0 governance/architecture. Hockey-native goalie, line, manpower, shot/xG, rule and settlement semantics remain in Daily-NHL.

## Detailed planning companion — 2026-10-10

Read the [NHL planning guide](nhl/README.md) and [Feature Dictionary v0.2](nhl/FEATURE_DICTIONARY_V0_2.md), with its [structured registry](nhl/FEATURE_DICTIONARY_V0_2.json), for the detailed proposal developed from this boundary.

The dictionary preserves all 142 v0.1 base field IDs and adds `independent_target_ref`, for 143 records. It specifies conventional and advanced measures, populations, units, source/provenance requirements, candidate windows, missingness, internal model lineage and downstream outputs. The detailed formulas and candidate choices are proposed research specifications; this original boundary did not previously select or certify them.

This is a documentation-only planning revision. `Daily-NHL` was rechecked as empty on 2026-10-10. The companion does not bootstrap that repository, implement a model, certify a source, change ownership, or grant Bridge/production authority. TDLA holds the coordination record; Daily-NHL remains the owner of future hockey semantics and implementation.

## Mission

Model NHL scoring, shot and player outcomes from shot quality, goalies, lines, special teams, manpower state, travel/rest and lineup evidence.

## Canonical sport truth

- teams, skaters, goalies, rosters, lines/pairs, coaches, games, periods and venues
- starting-goalie confirmation/revisions, scratches, line combinations and power-play units
- regulation/OT/shootout rules and settlement distinctions
- reschedules and roster/line revisions are immutable time-versioned state
- provider IDs remain crosswalks

## Factual evidence

- event/PBP and shot location/type data
- shifts/time-on-ice and manpower state where available
- internally derived expected-goal components from factual shot context
- goalie starts/performance/workload and confirmed/probable state
- lines/pairs, injuries/scratches and special-teams units
- rest/back-to-back, travel/time-zone and venue context

## Feature families

- conventional team/player/goalie counts and rates: goals, assists, points, shots on goal, saves, time on ice, shooting/save fractions, goals for/against, PP/PK results, penalties and faceoffs, under explicitly declared counting rules
- 5v5 shot attempt/share and quality measures
- internally computed xG/high-danger/chance features
- goalie shot-stopping relative to shot quality with shrinkage/workload
- special-teams offense/defense, penalty and manpower efficiency
- line/pair usage, matchup and time-on-ice opportunity
- player shot/point opportunity
- travel/back-to-back/rest and empty-net/game-state effects

### Detailed feature discipline

- Independent inputs use factual evidence and internally derived estimates. Third-party xG, forecasts, picks and power ratings are not NHL independent-model inputs; external terminology references do not grant permission to import their predictions.
- Ordinary shot accounting distinguishes SOG, unblocked attempts/Fenwick and all attempts/Corsi; awarded goals, penalty shots and shootout events retain separate classifications. Actual pre-event scoreboard state includes already-credited awarded goals.
- Rates and shares pool matching numerators and denominators. Store playing time in seconds, retain exact manpower/goalie-presence states, include zero-shot exposure, and distinguish unknown data from known zero events.
- Proposed team xG uses an internally estimated ordinary unblocked-attempt baseline. Proposed goalie xGA/GSAx/expected-save measures use the explicitly named conditional-on-SOG baseline on matching goalie-assigned SOG. Partial xG plus a full denominator is invalid without a validated missingness estimator.
- Versioned `independent_target_ref` fixes sporting target, counting population, phase and rules before independent computation/freeze. Post-freeze `market_contract` maps provider selections only to supported projections of the frozen output; it cannot redefine or refit that output.
- Source envelopes retain meaningful effective/published/observed/ingested/available clocks and immutable revisions. Reviewed source descriptions are distinct from verified acquisition, history, rights, freshness or model readiness.
- Coaches and dated factual coaching context remain canonical evidence. Numerical coaching effects, opponent-specific line-matchup adjustments, danger/rush/rebound/flurry definitions, tracking additions, selected windows, shrinkage and ensemble weights require their own source support and chronological research.

## Target/market universe

- moneyline including OT/SO where defined
- 3-way regulation
- puck line, game total, team totals
- period markets with explicit settlement
- player shots on goal, goals, points and related props where opportunity/history are certified
- goalie saves/goalie props only with confirmed-start/support rules

## Model Zoo direction

- Poisson/Skellam and overdispersed scoring baselines
- team-strength and shot-process/xG models
- goalie true-talent/current-state specialists
- special-teams and line-matchup models
- player shot/opportunity specialists
- event/shot or period/game simulation producing score, shot and player distributions
- learned ensemble from frozen OOS predictions only

## Full build outline

| Phase | NHL requirement |
|---|---|
| SB-0 | Bootstrap hockey-specific constitution/architecture before code. |
| SB-1 | Canonicalize team/skater/goalie/line/game/period/rules and regulation-vs-OT settlement. |
| SB-2 | Acquire PIT event/shot/shift/goalie/lineup/injury/travel evidence. |
| SB-3 | Reconstruct expected/confirmed goalie, scratches, lines/pairs and special-team state. |
| SB-4 | Build xG/shot/goalie/special-team/line/rest/travel features. |
| SB-5 | Define regulation/OT/SO, puck/total/period/player/goalie market contracts. |
| SB-6 | Build team/scoring/shot/goalie baselines. |
| SB-7 | Add goalie, special-team, player-shot and line-matchup specialists. |
| SB-8 | Simulate goals/shots/periods/OT-SO/player outcomes and joint dependencies. |
| SB-9 | Calibrate/freeze independent NHL TDL Unified Line. |
| SB-10 | Join DDC market evidence after freeze; value/timing/goalie-confirmation risk. |
| SB-11 | Apply NHL Recommendation Gate and export SportDecisionPackage/joint refs. |
| SB-12 | Settle/evaluate by goalie certainty, rest, market class, regulation/OT rule and season phase. |
| SB-13 | Prove manual slate -> DLC/report handoff. |
| SB-14 | Later live sibling using score/time/period/manpower/penalties/goalie/shots/xG. |
| SB-15 | Automate only after manual certification and late-goalie-change recovery proof. |

## Simulation / joint evidence

- model low-scoring overdispersion, regulation/OT/SO paths and empty-net effects
- player shot/point distributions reflect ice time, line and power-play opportunity
- goalie-start uncertainty propagates through team/player distributions
- same-event joint evidence is exported only when calibrated

## Uncertainty

Unconfirmed goalies, line changes, scratches, small goalie samples and back-to-backs are explicit uncertainty drivers. Low-frequency goal/point props require stronger evidence than shots.

An unconfirmed starter may be represented through explicit conditional scenarios under a declared, validated support contract; mixture weights require justified internal evidence. Unresolved conflicting evidence that the contract cannot handle blocks the affected authoritative output. Confirmed-start-dependent goalie props remain unsupported until their requirements are met. This planning option does not claim that a scenario model is already validated.

## Live boundary

Live NHL may update score/time/period, manpower, penalties, shots/xG, goalie status and remaining player opportunity. Pregame goalie/line predictions remain immutable.

## Anti-drift rules

- do not reduce hockey to score-only inputs if shot/goalie/manpower evidence exists
- do not treat regulation 3-way and incl-OT moneyline as one target
- do not infer starting goalie from market movement
- do not build EdgeStack here

## Bridge stop conditions

Stop/escalate for the affected capability when goalie uncertainty or conflicting evidence cannot be represented under its declared support contract, settlement state is ambiguous, shot/shift source timing cannot be PIT-reconstructed, regulation/OT/SO identity is being collapsed, or a live shortcut would rewrite pregame state. Named conditional scenarios are not unconditional forecasts or permission to bypass confirmed-start requirements.

## Exit criteria

- game/goalie/player distributions have OOS calibration
- regulation/OT/SO settlement replay is exact
- late goalie/line revisions create correct immutable snapshots
- SportDecisionPackage and joint evidence are DLC-compatible
