# Daily MMA Build Boundary V1

**Status:** EXISTING EMPTY REPOSITORY — ARCHITECTURE / IMPLEMENTATION NOT AUTHORIZED BY THIS FILE  
**Repository:** `OneVillage83/Daily-MMA`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authorization / promotion scope

Daily-MMA is promotion/ruleset aware. Initial promotion coverage is an explicit owner decision; UFC or any other promotion must not become an architectural assumption that makes other rulesets impossible.

## Mission

Produce calibrated MMA bout, method and round probability distributions from fighter skill, opponent-adjusted striking/grappling, pace, finishing/submission dynamics, weight class, availability and ruleset evidence.

## Canonical sport truth

- fighters, promotions, events, bouts, weight classes and contracted/catch weights
- scheduled rounds/duration, referee and judges where used
- stance and participant identity
- bout cancellations, replacements, no contests, overturned results and disqualifications
- weigh-in result/missed weight state
- ruleset/version and provider settlement
- provider IDs remain crosswalks

## Factual evidence

- official/credible round and bout statistics
- significant/total strikes by position/target where available
- knockdowns
- takedown attempts/completions/defense
- control time, submission attempts and position transitions where available
- opponent strength and career chronology
- age, height/reach, stance, weight class and bout frequency
- weigh-ins and opponent replacements
- travel/altitude and layoff
- injury/camp information only when source/PIT reliability is strong enough for approved use

## Feature families

- opponent-adjusted striking offense/defense, pace and accuracy
- damage/knockdown/finish rates with shrinkage
- takedown/grappling/control/submission offense/defense
- position/style matchup features
- cardio/round-decay and pace sustainability
- age/layoff/experience/weight-class history
- short-notice/replacement and missed-weight state
- judging/referee effects only if validated and appropriate

## Target / market universe

- fight winner / moneyline
- method of victory
- goes distance
- total rounds / over-under
- round of victory / fight ends in round
- decision type and other props only after sufficient history/calibration
- fighter-specific strike/takedown props only if provider settlement and underlying data are robust

## Model Zoo direction

- Elo/Bradley-Terry/opponent-adjusted fighter rating baselines
- hierarchical Bayesian striking/grappling/finishing models
- nonlinear bout models
- competing-risk / survival-hazard models for KO/TKO, submission, decision
- style-matchup and round-decay specialists
- Monte Carlo round/bout simulation
- learned ensemble from frozen chronological OOS predictions

## Full build outline

| Phase | MMA requirement |
|---|---|
| SB-0 | Bootstrap promotion/ruleset-aware local architecture before code. |
| SB-1 | Canonicalize fighter/event/bout/weight/rules/result/settlement identity. |
| SB-2 | Acquire immutable PIT fight stats, weigh-in, replacement, availability and context evidence. |
| SB-3 | Reconstruct scheduled bout, opponent, weight, rounds, replacement and known availability state. |
| SB-4 | Build opponent-adjusted striking/grappling/pace/finish/cardio/style features. |
| SB-5 | Define winner/method/distance/round/prop target and settlement contracts. |
| SB-6 | Establish fighter-rating and finish/distance baselines. |
| SB-7 | Add style/grappling/striking/cardio/competing-risk specialists with OOS proof. |
| SB-8 | Simulate round/bout outcome paths and method/round dependencies. |
| SB-9 | Calibrate/freeze independent MMA TDL Unified Line. |
| SB-10 | Join DDC market evidence only after freeze; value/EV/timing/risk. |
| SB-11 | Apply MMA Recommendation Gate and export SportDecisionPackage/joint refs. |
| SB-12 | Settle/evaluate by weight class, rounds, favorite band, method and promotion. |
| SB-13 | Prove manual event card -> DLC/report handoff. |
| SB-14 | Later live sibling from round/time/official in-bout event state where feed quality supports it. |
| SB-15 | Automate only after manual certification and bout-change/cancellation recovery proof. |

## Simulation / joint evidence

- competing outcomes must sum coherently across fighter × method × round/distance
- scheduled 3-round vs 5-round bouts are separate contexts
- same-bout winner/method/round/total correlations come from the joint model, not independent multiplication
- cancellations/no-contests are settlement states, not modeled sporting outcomes unless explicitly required

## Uncertainty

Short-notice replacements, long layoffs, limited fight samples, major weight changes, missed weight and sparse lower-promotion statistics require wider uncertainty/degradation.

## Live boundary

Live MMA may consume round/time plus reliable official in-bout event evidence. Because live fight stats can lag/revise, source freshness/revision state is first-class. Live never rewrites the pre-fight ledger.

## Anti-drift rules

- no subjective media scorecards/public picks as independent prediction input
- no assuming all promotions/rulesets are interchangeable
- no treating a tiny recent sample as a regime change without shrinkage
- no market-line input into independent fighter strength
- no EdgeStack implementation here

## Bridge stop conditions

Stop/escalate when bout/rules/weight/settlement identity is ambiguous, live/stat source timing is unreliable, injury/camp claims lack trustworthy PIT sourcing, or method/round support lacks enough outcome history.

## Exit criteria

- bout/result/settlement replay is exact
- winner/method/distance/round distributions are chronologically calibrated
- joint probability coherence is validated
- SportDecisionPackage is DLC-compatible
