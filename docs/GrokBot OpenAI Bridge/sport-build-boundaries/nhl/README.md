# NHL modeling plan and feature dictionary

**Status:** PROPOSED — REPOSITORY DOCUMENTATION ONLY

**Planning revision:** v0.2, 2026-10-10

**Intended sport owner:** `OneVillage83/Daily-NHL`

This guide connects the original NHL build outline to the detailed evidence and feature definitions. The plan models shot opportunities, shot quality, goalies, special teams, player usage, and game state to produce independent team and player distributions. It retains conventional statistics alongside advanced measures that explain how those outcomes arise.

This folder is a planning home within TDLA's sport-boundary pack. NHL identity, state, feature engineering, models, simulation, decisions, and settlement remain Daily-NHL responsibilities. These documents establish no implemented adapter, trained model, certified rule interpretation, or production authority.

## Read the plan together

- [Daily NHL Build Boundary V1](../DAILY_NHL_BUILD_BOUNDARY_V1.md) retains the complete NHL scope and SB-0 through SB-15 sequence.
- [Shared Sport Build Constitution V1](../SHARED_SPORT_BUILD_CONSTITUTION_V1.md) governs ownership, independent prediction, point-in-time evidence, evaluation, and handoffs.
- [Feature Dictionary v0.2](FEATURE_DICTIONARY_V0_2.md) is the readable field and protocol reference.
- [Feature Dictionary v0.2 JSON](FEATURE_DICTIONARY_V0_2.json) contains the proposed registry used to generate that reference.

The v0.1 Excel workbook remains a prior review snapshot. Repository v0.2 preserves its **142 field IDs** and adds the `independent_target_ref` control, for **143 base fields**. A base field can have explicitly identified state, window, measure, and transformation variants. The registry is not a claim that 143 predictors have been selected: evidence, controls, training labels, internal estimates, forecasts, and downstream market fields have different roles.

## What the statistics must explain

The original requirements remain covered as follows. The dictionary makes definitions inspectable; the boundary still supplies the wider model and delivery obligations.

| Original requirement | Detailed coverage and modeling purpose |
|---|---|
| 5-on-5 attempts, shares, and quality | Team goals, SOG, misses, blocked attempts, Corsi, Fenwick, matching per-60 rates, shares, and internally derived xG. Separate territorial balance from total activity. |
| Own xG, high-danger, and chance features | Shot geometry/type/context and internal shot-model components. Danger, rebound, rush, and flurry features remain reserved research until their definitions and coverage are validated. |
| Goalie stopping, shrinkage, and workload | Saves, SOG faced, goals allowed, save percentage, goals allowed per 60, SOG-based xGA/GSAx, stopping effects, appearances/workload, and starter scenarios. |
| Special teams, penalties, and manpower | Official PP/PK opportunities and conversion measures, analytical state exposure, penalties drawn/taken, PP xGF and PK xGA. Penalty minutes and PP opportunities are distinct. |
| Lines, pairs, matchups, and player opportunity | Individual goals/assists/points/shots, observed and projected ice time, unit assignments, shared minutes, on-ice rates, availability, and finishing effects. |
| Rest, travel, venue, and coaching context | Recovery intervals, schedule load, back-to-backs, venue/time-zone proxies, and dated coach identity/context within entity evidence. Coaching observations do not imply an invented numerical coaching effect. |
| Regulation, completed-game, period, team, player, and goalie targets | Explicit independent target definitions and outcome distributions, then compatible provider-contract mappings after freeze. Support remains conditional on evidence and certification. |
| Joint simulation and uncertainty | Shot/goal/player distributions, goalie and lineup scenarios, model disagreement, and calibrated joint evidence where demonstrated. |
| Evaluation, live, manual handoff, and automation | Protocol plus SB-12 through SB-15 retain settlement replay, a separate live sibling, manual sport-to-DLC proof, and later automation equivalence. |

Conventional records, goals per game, shooting/save percentages, faceoffs, hits, blocks, giveaways, and takeaways remain available as descriptive or supporting evidence. Their inclusion does not guarantee predictive weight. Opponent and score adjustments must be internally defined and tested. PDO is a diagnostic combination of shooting and saving, not an automatic next-game reversal rule.

Player production and on-ice team results stay separate. A line's xG rate describes shared deployment; it does not establish one player's causal contribution. An injury scenario should redistribute minutes, line combinations, and special-team roles to the expected replacements.

## Shared definitions come before model fitting

Build mutually exclusive clock intervals from phase, skater counts, goalie presence, penalty state, and score. Five-on-five requires five skaters per side and both goalies present. Missing goalie identification does not prove an empty net. Exposure includes eligible intervals with no shots.

For ordinary shot events, SOG includes goals and saves, Fenwick adds misses, and Corsi adds blocked attempts. A provider's separate goal records must be normalized before counting. Retain penalty shots, shootout attempts, awarded goals, and unresolved scoring exceptions under explicit classifications.

Store exposure in seconds:

`rate_per60 = 3600 * event_total / matching_exposure_seconds`

Counts and exposure use the same state filters, windows, and weights. Pool matching numerators and denominators rather than averaging per-game percentages or rates indiscriminately. Zero exposure yields a null rate. An observed zero with valid exposure remains zero; missing evidence remains null with a reason. Partial xG cannot be divided by a full, differently covered attempt population and presented as the complete metric.

### Own expected goals and goalie comparison

The proposed primary opportunity universe is ordinary unblocked attempts (UA). An internal on-target model estimates `q = P(SOG | UA, pre-outcome context)`. A separate neutral finishing/stopping baseline estimates `r = P(goal | SOG, pre-outcome context)`. Their product gives attempt-level xG. Both components need predictors available for all eligible UA, including misses. Any all-attempt extension first models blocked versus unblocked outcomes.

Historical coordinates are observed evidence. Future shot locations, types, and opportunities must be forecast or simulated. Outcome labels train the appropriate component; they cannot become predictors for that same event.

Keep `xga_ua` and conditional-on-SOG `xga_sog` separate. Goalie comparison uses the same eligible goalie-assigned SOG population for xGA, goals allowed, and shots faced:

- `goalie_gsax_sog = xga_sog - goals_allowed`
- `expected_save_fraction = 1 - xga_sog / sog_faced`

The descriptive GSAx residual is distinct from a shrunken stopping-talent estimate. Finishing and goalie effects need an identified baseline and must not be credited twice. All predictive xG inputs and fitted adjustments must come from TDL's own versioned models; outside predictive ratings, xG outputs, or GSAx outputs do not enter the independent forecast.

## How the Model Zoo uses this evidence

| Model family | Intended contribution |
|---|---|
| Poisson/Skellam and overdispersed baselines | Interpretable goal-count and goal-difference benchmarks; test whether richer distributions improve fit and calibration. |
| Team strength and shot process/xG | Forecast opportunity volume and quality by state, integrating over future shot context. |
| Goalie specialists | Estimate stopping ability, current workload/context, and conditional outcomes for plausible starters. |
| PP/PK and line-matchup specialists | Model special-team exposure/production and the personnel likely to share important minutes. |
| Player opportunity specialists | Allocate ice time, attempts, SOG, goals, assists, points, and goalie saves consistently with the game process. |
| Event/period/game simulation | Represent regulation, overtime, shootout, manpower, score, empty-net behavior, and dependencies among team/player outcomes. |
| Chronological ensemble and calibration | Combine frozen out-of-sample base predictions, assess disagreement, and produce the independent TDL Unified Line. |

A simulation must account for sequence dependence: a simulated goal ends that possession/sequence rather than leaving later rebound attempts that would not occur. Shared game paths should reconcile team shots, assigned goalie shots, saves, and goals. Same-event joint evidence is publishable only when its calibration is demonstrated.

Opponent-specific shared exposure and matchup adjustment remain planned SB-7 line-matchup work. The current lineup, pair and shared-minute records are prerequisites, not a completed matchup model.

## Target meaning is fixed before market comparison

`independent_target_ref` identifies the forecast's phase, statistical counting rules, and rules-version semantics before inference and freeze. Regulation three-way outcomes and a winner including an applicable tiebreak process remain separate targets. The relevant rule version and historical applicability require verification; this guide does not certify a current rulebook.

Ordinary shot-goal counts, scoreboard state, official results, and provider settlement are distinct views. In particular, `pre_event_score_diff` includes an awarded goal already credited to the scoreboard even though that award is not an ordinary shot event. A shootout result must not silently become an ordinary player goal or goalie shot.

After the independent forecast is frozen, `market_contract` maps a provider's selection, threshold, and settlement terms to compatible independent outputs. Quotes, no-vig probabilities, movement, closing prices, edge/EV, price thresholds, timing, and Recommendation Gate logic remain downstream. Ambiguous or unsupported mappings stay explicit. Market information cannot revise the frozen forecast or supply a missing starting goalie.

## Point-in-time evidence and uncertainty

Every snapshot selects the source revision legitimately available by its cutoff. Preserve event/effective time, publication time when supplied, first observation, ingestion time, defensible availability, and revision identity. Later corrections and confirmations create new snapshots. Future schedule facts may be usable when their published version was already known; future performance is not historical evidence.

The same restriction applies to fitted xG, priors, feature transformations, ensemble weights, and calibration. Chronological evaluation cannot rescore earlier forecasts with future-trained components and call them original predictions. Candidate recent-game, season, multiseason, and workload windows remain subject to selection. Decay, shrinkage, minimum samples, and thresholds are not fitted settings merely because a field exists.

Confirmed, probable, conflicting, unannounced, and ruled-out goalie evidence remain timestamped statuses. Use conditional forecasts when several starters are plausible. Combine them only with defensible recorded weights; do not invent 50/50 or translate “probable” into an arbitrary percentage. Keep goalie uncertainty, lineup uncertainty, model disagreement, and outcome variation identifiable. A scenario range does not establish nominal confidence coverage.

Unresolved contradictions beyond a declared, validated support contract block the affected authoritative output. Confirmed-start-dependent goalie props remain unsupported until their own conditions are met; scenarios do not override that requirement.

Evaluate calibration and proper scoring metrics chronologically, including strata for goalie certainty, rest/workload, target class, regulation/OT rules, and season phase. Preserve forecasts and all gate outcomes for settlement and review. Live updates get separate identities, cutoffs, state, and evaluation while the pregame record remains immutable.

## Next documentation and research step

Build the **source coverage and point-in-time acquisition matrix**. For each required field/variant, record the proposed source and exact mapping, historical seasons, event/state coverage, units, revision history, availability clocks, access conditions, freshness, reconciliation checks, and missing-data treatment. Separate reviewed source concepts from verified adapters. A glossary link or public tracking display does not prove ingestion rights, historical completeness, or live suitability.

Use that matrix to identify the first feasible core candidate set and specific gaps. Shot/goalie/manpower evidence remains central. Optional tracking, detailed video tags, danger thresholds, rush/rebound classifiers, and other deferred features require their own coverage and validation. Missing optional enrichment should restrict the dependent component rather than fabricate a value or halt every supported output.

Daily-NHL implementation requires a separately scoped owner instruction, repository registration, and local **SB-0 governance/architecture** before code. The established SB sequence then leads through evidence, models, calibration, manual handoff, live separation, and eventual automation proof. This planning update changes no Bridge authorization or production authority. TDLA's exact core continuation remains **A-11 Retry / Timeout / Idempotency Architecture**.
