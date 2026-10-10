# Daily NHL Feature Dictionary v0.2

**Status: PROPOSED — documentation only; no NHL source adapter, model or production authority is certified.**

Updated: 2026-10-10. Read the [NHL planning guide](README.md), [NHL build boundary](../DAILY_NHL_BUILD_BOUNDARY_V1.md), and [shared sport constitution](../SHARED_SPORT_BUILD_CONSTITUTION_V1.md) with this reference.

This readable reference is generated from [FEATURE_DICTIONARY_V0_2.json](FEATURE_DICTIONARY_V0_2.json), the structured source for these proposed definitions. Source SHA-256: `ccb22e7856c07b399fc00599cb662604b989374b640a06afe1ce8eaaef00b677`. Change the structured registry first, then regenerate this reference in the same documentation work unit; upstream/local certified authority always takes precedence.

The registry contains **143 base records with 17 attributes each**: all 142 v0.1 field IDs plus `independent_target_ref`. A base record is not necessarily a training column; roles include evidence, controls, labels, model outputs and downstream market records. Population/window variants are explicit configurations.

The original boundary establishes required feature families and authority rules. The detailed populations, formulas, candidate windows and internal xG convention below are newly proposed research specifications; citations to the boundary do not mean those details were previously selected or certified.

## Revision from v0.1

- Add a price-free independent sporting target/rules reference before freeze; keep provider market mapping downstream.
- Remove the residual coverage-only exception from team_xg_per_ua validation.
- Use actual already-credited scoreboard goals for pre-event score state, including awarded goals.
- Preserve coach identity and dated factual coaching context, plus rest/workload evaluation strata from the prior plan.
- Pin original project evidence to the verified commit and distinguish reference review from unverified acquisition/model readiness.
- Replace standalone-workbook scope wording with repository-documentation-only status; retain all pending research and certification decisions.

The previously delivered Excel workbook remains a v0.1 review snapshot. This v0.2 JSON/reference is the revised proposed plan. The revision metadata preserves the prior registry/workbook hashes.

## Record attributes

| Key | Meaning |
|---|---|
| `id` | Field ID |
| `name` | Name |
| `family` | Family |
| `role` | Role |
| `grain` | Grain |
| `priority` | Priority |
| `definition` | Definition / calculation |
| `dtype` | Data type |
| `unit` | Unit |
| `population` | Population / exposure |
| `window` | Window |
| `source_ids` | Source IDs |
| `availability` | Availability rule |
| `missing` | Missing-data rule |
| `validation` | Validation |
| `use` | Model use |
| `readiness` | Readiness |

## Protocol

### Status

**Version.** Proposed Feature Dictionary v0.2, 2026-10-10. Supersedes the v0.1 planning definitions while preserving all 142 prior base field IDs and adding independent_target_ref (143 total). Not a trained model, selected/certified feature set, or repository-local Daily-NHL architecture. Numeric examples are synthetic. Source IDs: B1; B2.

**Scope.** Definitions of evidence, feature families, internal estimates and downstream outputs for pregame NHL. Live has separate snapshot identity, cutoffs and evaluation. Repository documentation only; no source adapter, feature computation, model, production integration or Bridge execution authority is implemented or certified. Source IDs: B1; B2.

### Schema

**Materialized feature key.** (snapshot_id, entity_type, entity_id, opponent_id where relevant, field_id, measure_variant_id, population_id, window_id, transform_version). Variant ID distinguishes event type/tracking metric/component. Base measures expand only into explicitly configured variants, not every possible training column. Source IDs: B1; B2.

**Required payload.** value plus numerator/count, exposure/denominator, eligible_count, observed_count and coverage where applicable; otherwise null/NOT_APPLICABLE. Always retain quality_status, missing_reason, available_at, source_snapshot_id and definition_version. Model estimates additionally require internal_model_id/training_cutoff. Every forecast also pins independent_target_ref before freeze; provider market mapping is not its target-definition authority. Source IDs: B1; B2.

**Role separation.** EVIDENCE = factual observation/state. DESCRIPTIVE = deterministic aggregate. MODEL_FEATURE = candidate independent covariate. INTERNAL_ESTIMATE = output of an upstream TDL model. TRAINING_LABEL = future outcome for a fitted component. FORECAST_OUTPUT = sealed prediction. MARKET_ONLY = downstream market evidence/calculation. CONTROL = provenance/eligibility; not an ordinary numeric covariate. Source IDs: B1; B2.

**Priority.** FOUNDATION is required for the dependent capability. CORE_CANDIDATE is in the first research set, not a proven selected feature. SUPPORTING is retained for diagnostics or incremental tests. LATER is deferred until evidence and validation support it. OUTPUT_ONLY and POST_FREEZE do not belong in the independent design matrix. Source IDs: B1; B2.

**Readiness.** SOURCE_MAPPING_REQUIRED; DERIVATION_NOT_BUILT; MODEL_NOT_BUILT; OPTIONAL_FEED_UNVERIFIED; POST_FREEZE_ONLY. This dictionary makes no claim that source adapters or models already exist. Source IDs: B1; B2.

### Units

**Stored units.** Store elapsed time and ice time in seconds, coordinates/distances with explicit feet or km, timestamps in UTC with venue IANA time zone retained. Store proportions as fractions 0..1. Display percentages separately; shooting-minus-expected uses fraction internally and percentage points in a report. Source IDs: B1; B2.

**Per-60 formula.** per60 = 3600 * SUM(event count or expected-goal value) / SUM(eligible ice_time_seconds). Denominator must match entity, state, window and eligibility. Do not average game-level per60 rates. Source IDs: B1; B2.

**Share formula.** share = SUM(for) / (SUM(for) + SUM(against)) for matching populations. Numerator 0 with a positive denominator is a legitimate 0. A zero or missing denominator yields null with reason. Source IDs: B1; B2.

**Signed metrics.** GSAx is xGA - GA, so positive indicates goals prevented above that declared baseline. Rest and time-zone differences have explicitly declared direction. No field's sign is inferred from its name alone. Source IDs: B1; B2.

### Point in time

**Historical eligibility.** At forecast cutoff T, an evidence version is eligible only if its defensible available_at <= T and the relevant historical play occurred before T. Pregame aggregates use only completed, eligible prior games by default. Never filter by date alone. Source IDs: B1; B2.

**Availability clocks.** Retain effective_at, source_published_at if provided, first_observed_at, ingested_at and available_at. Prospective default: available_at is the later of first observation and a trustworthy publication timestamp. A dated webpage fetched later does not prove earlier availability. Source IDs: B1; B2.

**Historical archive exception.** Earlier available_at requires certified immutable as-of evidence. If not reconstructable, mark PIT_AMBIGUOUS and exclude from that historical experiment; do not backdate to game date. Source IDs: B1; B2.

**Revisions.** Append each corrected event, goalie report, lineup or schedule version. A replay selects the latest eligible version at its cutoff. A new forecast links supersedes_snapshot_id without changing the prior snapshot. Source IDs: B1; B2.

**Model-generated features.** Internal xG, talent, opportunity, opponent adjustment, normalization, shrinkage and imputation must be fitted only within the training history of that fold/cutoff. Store model version and training cutoff. OOF/forward predictions are required for learned stackers. Source IDs: B1; B2.

**Quote isolation.** Independent sporting target/counting/rules definitions and supported output scope are fixed through independent_target_ref before computation and freeze. After independent_snapshot_frozen_at, market_contract maps a provider selection to that frozen distribution under a supported deterministic projection. Prices never refit the model or change its frozen distribution. Quote changes may re-evaluate value; new sport evidence requires a new independent snapshot. Source IDs: B1; B2.

### Populations

**Orthogonal state.** Retain period_type REG/OT/SO, own/opponent skater counts, both goalie-presence flags, penalty advantage, delayed penalty status and pre-event score separately. These fields are the state authority; convenience buckets never discard them. Source IDs: B1; B2.

**REG5V5.** Regulation, five skaters per team, both goalies present. Intervals are [start,end), exclude stoppages, and use pre-event state for events. Do not combine 4v4 or overtime 5v5 with REG5V5. Source IDs: B1; B2.

**REG5V4 / REG4V5.** Regulation 5v4 or 4v5, both goalies present, with verified penalty manpower context. Numerators and seconds use that exact state. Other PP/PK states such as 5v3 and 4v3 remain separate variants. Source IDs: B1; B2.

**Occupied / empty-net states.** REG_OTHER_OCCUPIED retains exact skater counts and penalty context. OWN_EMPTY, OPP_EMPTY and BOTH_EMPTY retain simultaneous penalty state, e.g. 6v4. Goalies absent due to tactical pull versus delayed penalty are distinct when known; unknown reason stays unknown. Source IDs: B1; B2.

**OT and shootout.** Overtime is separately tagged with game type/rules version and exact manpower. Shootout events are excluded from ordinary shot/xG/goalie feature populations and modeled/settled under separate contracts. Source IDs: B1; B2.

**Special scoring events.** Penalty shots, awarded goals, shootout attempts and shootout score adjustments have separate flags and records. Ordinary chance-model populations exclude them by default. Reconcile official result/individual-stat targets using their own contracts, not by forcing all totals to match. Source IDs: B1; B2.

**Shot accounting.** Ordinary SOG = saved physical shots + physical goals. Fenwick/unblocked attempts = SOG + missed attempts. Corsi/all attempts = Fenwick + blocked attempts. A blocked attempt belongs to the shooting team, not the blocker. Preserve original event codes. Source IDs: B1; D1; D3.

**On-ice exposure.** Team minutes are wall-clock playing intervals; skater/goalie minutes require actual participation. Sum overlapping shift intervals once per participant. Confirmed no appearance is zero exposure, not missing shifts. Unknown participation invalidates dependent on-ice rates. Source IDs: B1; B2.

**Zone starts.** Define OZ_faceoff_start_share = OZ/(OZ+DZ), neutral excluded, and retain NZ and on-the-fly counts separately. This is a chosen TDL convention; never silently substitute a provider denominator including neutral/on-the-fly starts. Source IDs: B1; D1.

### Windows

**S2D.** Current season and explicit game type through T. Only prior completed games whose selected evidence versions were available at T. Playoffs and regular season remain separate unless a versioned training rule explicitly combines them. Source IDs: B1; B2.

**G5 / G10 / G20.** Prior 5/10/20 eligible completed games for a team; prior eligible appearances for a skater/goalie. Retain actual game count, starts/relief count and exposure. Team schedule workload windows include non-appearance separately. These are candidate windows, not certified weights. Source IDs: B1; B2.

**H2S.** Previous two complete seasons of the explicit game type, cut off at T. Candidate prior-support window; roster/team history and player transfers are retained. No automatic 70/30 season blend. Source IDs: B1; B2.

**D7 / D14.** Trailing 7/14*24 hours ending at T for historical workload totals. Exact timestamps define boundaries. A future schedule-density field must be named separately and can use only schedule versions known at T. Source IDs: B1; B2.

**Weighted rate.** Optional exponential decay: w_j = exp(-ln(2)*age_days_j/h). weighted_per60 = 3600*SUM(w_j*c_j)/SUM(w_j*seconds_j). Half-life h is tuned on chronological training folds, not guessed or optimized on final holdout. Source IDs: B1; B2.

**Shrinkage.** Proposed rate smoothing: lambda=(C+lambda_prior*E0)/(E+E0), with consistent exposure units. Proportion smoothing: p=(successes+alpha)/(trials+alpha+beta). Priors/grouping are training-only and undecided. Weighted/decayed versions are smoothing forms, not automatically exact posterior distributions. Source IDs: B1; B2.

### Missing data

**Null is not zero.** Unknown value -> null plus a reason. No applicable state or no exposure -> null for rates, even if event counts are 0. Known zero events over positive complete exposure -> numeric 0. Do not default missing xG, goalie IDs or travel to 0. Source IDs: B1; B2.

**Coverage.** Store usable eligible event count/eligible count and observed seconds/required seconds. Unknown denominator -> unknown coverage. Incomplete xG -> full-population model value null absent a validated estimator; partial sums are diagnostics on a separately identified scored subset, never paired with a full denominator. Source IDs: B1; B2.

**Branch-local failure.** Missing/conflicting mandatory evidence blocks the model or market that requires it. Another model may run only if its own predeclared inputs, fallback and calibration are satisfied. Do not call unsupported predictions PASS; preserve UNSUPPORTED separately from a recommendation gate. Source IDs: B1; B2.

**Optional features.** Unknown tracking or optional event context stays null with indicators. An optional-feature model needs validated missing-data treatment; absence does not justify invented observations. Source IDs: B1; B2.

**Quality status.** Use VALID, PARTIAL, MISSING, ZERO_EXPOSURE, NOT_APPLICABLE, CONFLICT, PIT_AMBIGUOUS, or UNSUPPORTED. These are data statuses, distinct from BET/LEAN/WATCH/PASS/AVOID. Source IDs: B1; B2.

### Internal xG

**Unblocked-attempt baseline.** Proposed two-stage UA baseline: q_i=P(SOG|UA, pre-outcome X), fitted on UA; r_i=P(goal|SOG, pre-outcome X), fitted on SOG but evaluated on all UA including misses. xg_ua_i=q_i*r_i. Both stages require predictors defined before outcome on all UA; SOG-only placement/trajectory needs integration or a separate model. Neutral shooter/goalie reference. Source IDs: B1; B2.

**Goalie comparison.** For SOG, xga_sog=SUM(r_i); GA and SOG use exactly the same eligible goalie-assigned population. GSAx_SOG=xga_sog-GA; xsv=1-xga_sog/SOG; sv=(SOG-GA)/SOG. Incomplete scoring cannot pair partial xGA with full GA/SOG. Scored-subset diagnostics retain separate subset identity and coverage. Source IDs: B1; B2.

**Finishing and goalie effects.** Estimate shrinkage-adjusted shooter/goalie effects separately from the neutral shot-quality baseline, or in one identified model. Do not apply the same skill effect both inside baseline xG and again in the game simulator. Source IDs: B1; B2.

**Danger / rebound / rush.** These features remain reserved in v0.2; production thresholds and labeling rules are undecided. They remain LATER/inactive until a versioned region, threshold or sequence classifier with coverage and validation is selected. Source IDs: B1; B2.

**Sequence dependence.** Realized-shot xG sums and sequence scoring probability are different quantities. A simulation that scores a goal terminates that possession/sequence. Do not add repeated rebound opportunities that would not exist after that goal. Source IDs: B1; B2.

### Goalie state

**Confirmation.** CONFIRMED requires attributable explicit evidence as of T; PROBABLE is a reported/estimated state with source. UNKNOWN and CONFLICT remain explicit. Store goalie-specific scenario outputs if required, and do not infer the starter from odds. Source IDs: B1; B2.

**Scenario probabilities.** Weights need a documented internal estimate or other allowed factual basis. If weights are unavailable, publish conditional scenarios/range; do not silently assign 50/50. Confirmed-start-dependent goalie props remain unsupported until their own conditions are met. Source IDs: B1; B2.

### QA

**Count identities.** On each matching population: SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK. Goalie saves=eligible SOG faced-eligible goals allowed. Record exceptions outside these populations separately. Source IDs: B1; B2.

**Exposure identities.** Mutually exclusive team interval durations sum to known playing time for the selected phase. Do not count stoppages or double-count overlaps. Sum of skater exposure matches skater-count-integral when shifts are complete. Source IDs: B1; B2.

**xG bounds.** 0<=q_i,r_i,xg_ua_i<=1. 0<=SUM(xg_ua)<=eligible UA count; 0<=xga_sog<=eligible SOG count. For matching goalie sample, sv-xsv=GSAx_SOG/SOG. Source IDs: B1; B2.

**Forecast consistency.** Regulation home win + tie + away win =1. Completed-game home+away win=1 only for contracts guaranteed decisive. Player/team/goalie simulations reconcile under their declared target rules. Probability uncertainty is distinct from the distribution of possible scores. Source IDs: B1; B2.

### Sources

**Source classes.** B1/B2 are original project authority pinned to the verified source commit; linked current companion documents retain their own authority. D1-D4 are reviewed terminology/public-description references. E/S/A/V/T/M are acquisition classes, not verified adapters; I denotes proposed TDL artifacts. reviewed_at records the planning/reference review, not data access, historical coverage, rights, freshness or operational validation. Acquisition/model records retain verified_at=null and explicit unverified/unbuilt status. Source IDs: B1; B2.

### Outputs

**Settlement and pushes.** The independent sporting target/counting/rules definition is pinned before freeze; provider settlement/threshold/push/void/fee mapping is attached afterward only within supported frozen output scope. For a stake-returned push contract and p_win>0: fair decimal d=(1-p_push)/p_win and EV=p_win*(d-1)-p_loss before explicit expected fees. With p_win=0 no finite fair win price is defined; all-push cases have no action. Do not use this contract for every binary exchange without mapping. Source IDs: B1; B2.

**Selection and evaluation.** Dictionary availability does not imply model selection. Compare justified feature groups in walk-forward folds; use held-out calibration, preserve all supported forecasts and BET/LEAN/WATCH/PASS/AVOID states, and assess results by goalie certainty, rest/back-to-back/workload, manpower/state, market class, regulation/OT/SO target/rules and season phase. Dated factual coaching context may be retained; any estimated coaching effect needs independent chronological evidence. Source IDs: B1; B2.

## Field families

| Family | Base records |
|---|---|
| Provenance | 12 |
| Identity and state | 15 |
| Shot and exposure primitives | 11 |
| Team counts | 12 |
| Team rates and shares | 14 |
| Team shot quality | 6 |
| Special teams | 9 |
| Team supporting features | 10 |
| Goalie performance | 13 |
| Lineup and confirmation | 5 |
| Player opportunity | 12 |
| Rest travel and tracking | 8 |
| Internal model components | 4 |
| Independent forecast outputs | 7 |
| Market and gate outputs | 5 |

## Provenance

### snapshot_id

**Forecast snapshot ID**

| Attribute | Definition |
|---|---|
| Field ID | snapshot_id |
| Name | Forecast snapshot ID |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Unique immutable pregame/live forecast version; never reused after a material revision. |
| Data type | string |
| Unit | ID |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Missing required lineage prevents affected PIT use. |
| Validation | Immutable, timestamped, and traceable to exact revision. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### prediction_cutoff_utc

**Prediction cutoff**

| Attribute | Definition |
|---|---|
| Field ID | prediction_cutoff_utc |
| Name | Prediction cutoff |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Exact UTC instant T used to select all eligible evidence and models. |
| Data type | timestamp |
| Unit | UTC instant |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Missing required lineage prevents affected PIT use. |
| Validation | Immutable, timestamped, and traceable to exact revision. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### source_snapshot_id

**Source snapshot ID**

| Attribute | Definition |
|---|---|
| Field ID | source_snapshot_id |
| Name | Source snapshot ID |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Immutable raw-source envelope reference with provider, URI/object ID, revision and content hash. Retain meaningful effective_at, source_published_at, first_observed_at, ingested_at and defensible available_at; unavailable/not-applicable clocks remain explicitly null with reason. The envelope preserves each source revision and does not backdate historical availability. |
| Data type | string |
| Unit | ID |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Missing required lineage prevents affected PIT use. |
| Validation | Immutable, timestamped, and traceable to exact revision. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### source_published_at

**Source publication time**

| Attribute | Definition |
|---|---|
| Field ID | source_published_at |
| Name | Source publication time |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Timestamp asserted by source when supplied and reliable; never inferred from event date. |
| Data type | timestamp&#124;null |
| Unit | UTC instant |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null permitted; use actual first observation conservatively. |
| Validation | Immutable, timestamped, and traceable to exact revision. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### first_observed_at

**First observed time**

| Attribute | Definition |
|---|---|
| Field ID | first_observed_at |
| Name | First observed time |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Earliest provable time this source version was observed by the collection system. |
| Data type | timestamp |
| Unit | UTC instant |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Missing required lineage prevents affected PIT use. |
| Validation | Immutable, timestamped, and traceable to exact revision. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### available_at

**Defensible availability time**

| Attribute | Definition |
|---|---|
| Field ID | available_at |
| Name | Defensible availability time |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Prospective default max(first_observed_at, trustworthy source_published_at); earlier archive availability needs separate certified evidence. |
| Data type | timestamp |
| Unit | UTC instant |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Missing required lineage prevents affected PIT use. |
| Validation | Immutable, timestamped, and traceable to exact revision. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### definition_version

**Definition version**

| Attribute | Definition |
|---|---|
| Field ID | definition_version |
| Name | Definition version |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Version/hash of field formula, event mapping, population and denominator contract. |
| Data type | string |
| Unit | version |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Missing required lineage prevents affected PIT use. |
| Validation | Immutable, timestamped, and traceable to exact revision. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### internal_model_ref

**Internal model lineage**

| Attribute | Definition |
|---|---|
| Field ID | internal_model_ref |
| Name | Internal model lineage |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | For any internal estimate: model ID, training cutoff, fold and calibration/transform versions. |
| Data type | object&#124;null |
| Unit | lineage |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Not applicable for factual fields; mandatory for model-derived estimates. |
| Validation | Immutable, timestamped, and traceable to exact revision. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### quality_status

**Data quality status**

| Attribute | Definition |
|---|---|
| Field ID | quality_status |
| Name | Data quality status |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | VALID/PARTIAL/MISSING/ZERO_EXPOSURE/NOT_APPLICABLE/CONFLICT/PIT_AMBIGUOUS/UNSUPPORTED; distinct from recommendation gate. |
| Data type | enum |
| Unit | category |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Missing required lineage prevents affected PIT use. |
| Validation | Immutable, timestamped, and traceable to exact revision. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### event_coverage_fraction

**Event coverage**

| Attribute | Definition |
|---|---|
| Field ID | event_coverage_fraction |
| Name | Event coverage |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Observed usable eligible events / known total eligible events for this feature; unknown denominator -> null. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Missing required lineage prevents affected PIT use. |
| Validation | 0..1 when known; denominator must be documented. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### interval_coverage_fraction

**Interval coverage**

| Attribute | Definition |
|---|---|
| Field ID | interval_coverage_fraction |
| Name | Interval coverage |
| Family | Provenance |
| Role | CONTROL |
| Grain | Source or feature snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Observed consistent eligible playing seconds / known required playing seconds; unknown denominator -> null. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; B1; B2 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Missing required lineage prevents affected PIT use. |
| Validation | 0..1 when known; denominator must be documented. |
| Model use | Eligibility and audit; not an ordinary model covariate |
| Readiness | SOURCE_MAPPING_REQUIRED |

### independent_target_ref

**Independent sporting target and rules reference**

| Attribute | Definition |
|---|---|
| Field ID | independent_target_ref |
| Name | Independent sporting target and rules reference |
| Family | Provenance |
| Role | CONTROL |
| Grain | Target definition / forecast snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Versioned price-free target specification fixed before modeling and freeze: entity, outcome/statistic, counting population, phase/game type, rules version, regulation/OT/SO and exceptional-goal accounting, participation conditions, and supported distribution/projection scope. Provider selection, quote, payout and settlement mapping remain in market_contract after freeze. |
| Data type | object |
| Unit | versioned reference |
| Population / exposure | Independent sporting target; no market prices or provider forecasts |
| Window | TARGET |
| Source IDs | I; B1; B2 |
| Availability rule | Define and pin before independent computation and independent_snapshot_frozen_at, using the rules/evidence versions legitimately available at cutoff T. |
| Missing-data rule | Missing or ambiguous target/counting/rules definition makes the dependent forecast UNSUPPORTED; never infer the target from prices. |
| Validation | All independent outputs link to this immutable version. Any later provider mapping must match the frozen statistic, phase, outcome support and rules; unsupported mappings fail closed. |
| Model use | Defines model labels, output meaning and projection support; not an ordinary model covariate |
| Readiness | DERIVATION_NOT_BUILT |

## Identity and state

### game_id

**Canonical game ID**

| Attribute | Definition |
|---|---|
| Field ID | game_id |
| Name | Canonical game ID |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Game / entity snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Canonical NHL game identity; provider IDs are crosswalks. |
| Data type | string |
| Unit | ID |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### season_game_type

**Season and game type**

| Attribute | Definition |
|---|---|
| Field ID | season_game_type |
| Name | Season and game type |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Game / entity snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Season plus PRESEASON/REGULAR/PLAYOFFS and rules version; never infer phase from calendar month. |
| Data type | object |
| Unit | category |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### entity_identity

**Entity identity and membership**

| Attribute | Definition |
|---|---|
| Field ID | entity_identity |
| Name | Entity identity and membership |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Game / entity snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Canonical team/skater/goalie/coach/venue IDs with membership or coaching-role valid_from/valid_to; trades and coaching changes do not rewrite prior attribution. Dated factual coaching context retains its source and availability; no numerical coaching effect is assumed. |
| Data type | object |
| Unit | IDs |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; A; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### game_status

**Game lifecycle**

| Attribute | Definition |
|---|---|
| Field ID | game_status |
| Name | Game lifecycle |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Game / entity snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Source-backed SCHEDULED/LIVE/FINAL/POSTPONED/CANCELLED or mapped equivalent plus raw code and revision. |
| Data type | enum |
| Unit | category |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### scheduled_start_utc

**Scheduled start**

| Attribute | Definition |
|---|---|
| Field ID | scheduled_start_utc |
| Name | Scheduled start |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Game / entity snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Latest target game start known at T; retain original start and reschedule lineage. |
| Data type | timestamp |
| Unit | UTC instant |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### actual_game_times

**Actual start/end**

| Attribute | Definition |
|---|---|
| Field ID | actual_game_times |
| Name | Actual start/end |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Game / entity snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Observed actual historical start/end instants; target future actual end is never available pregame. |
| Data type | object&#124;null |
| Unit | UTC instants |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### venue_context

**Venue context**

| Attribute | Definition |
|---|---|
| Field ID | venue_context |
| Name | Venue context |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Game / entity snapshot |
| Priority | FOUNDATION |
| Definition / calculation | Venue ID, IANA time zone, designated home/away role and neutral-site flag. Optional outdoor flag when verified. |
| Data type | object |
| Unit | IDs/categories |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### event_identity

**Event identity**

| Attribute | Definition |
|---|---|
| Field ID | event_identity |
| Name | Event identity |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Event / clock interval |
| Priority | FOUNDATION |
| Definition / calculation | Canonical event ID, source sequence, revision and raw event code; timestamps alone are not unique keys. |
| Data type | object |
| Unit | IDs |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### event_clock

**Event clock**

| Attribute | Definition |
|---|---|
| Field ID | event_clock |
| Name | Event clock |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Event / clock interval |
| Priority | FOUNDATION |
| Definition / calculation | Period number/type REG/OT/SO, elapsed and remaining seconds; order from source sequence with correction lineage. |
| Data type | object |
| Unit | seconds/category |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### pre_event_score_diff

**Score before event**

| Attribute | Definition |
|---|---|
| Field ID | pre_event_score_diff |
| Name | Score before event |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Event / clock interval |
| Priority | FOUNDATION |
| Definition / calculation | Own actual pre-event in-game scoreboard score minus opponent score, including awarded goals already credited, within the declared phase; exclude any later shootout score adjustment. Ordinary-shot goal counts remain a narrower population. |
| Data type | integer |
| Unit | goals |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### skater_counts

**Skater counts**

| Attribute | Definition |
|---|---|
| Field ID | skater_counts |
| Name | Skater counts |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Event / clock interval |
| Priority | FOUNDATION |
| Definition / calculation | Own and opposing skaters on ice immediately before event or throughout interval. |
| Data type | object |
| Unit | count |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### goalie_presence

**Goalie presence flags**

| Attribute | Definition |
|---|---|
| Field ID | goalie_presence |
| Name | Goalie presence flags |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Event / clock interval |
| Priority | FOUNDATION |
| Definition / calculation | Own and opposing goalie-present flags: true/false/unknown. A missing goalie ID does not mean empty net. |
| Data type | object |
| Unit | boolean/unknown |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### goalie_on_ice_id

**Goalie on-ice ID**

| Attribute | Definition |
|---|---|
| Field ID | goalie_on_ice_id |
| Name | Goalie on-ice ID |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Event / clock interval |
| Priority | FOUNDATION |
| Definition / calculation | Actual identified goalie assigned to each occupied interval/shot; unknown identity is distinct from absent. |
| Data type | string&#124;null |
| Unit | ID |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### penalty_state

**Penalty and extra-attacker context**

| Attribute | Definition |
|---|---|
| Field ID | penalty_state |
| Name | Penalty and extra-attacker context |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Event / clock interval |
| Priority | FOUNDATION |
| Definition / calculation | Penalty advantage for/against/none/unknown; delayed-penalty flag and goalie-pull reason when supported. Preserve together with skater/goalie fields. |
| Data type | object |
| Unit | category |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### special_event_class

**Special scoring class**

| Attribute | Definition |
|---|---|
| Field ID | special_event_class |
| Name | Special scoring class |
| Family | Identity and state |
| Role | EVIDENCE |
| Grain | Event / clock interval |
| Priority | FOUNDATION |
| Definition / calculation | Ordinary/penalty_shot/awarded_goal/shootout/score_adjustment/unknown, reconciled from source evidence. |
| Data type | enum |
| Unit | category |
| Population / exposure | All |
| Window | SNAPSHOT |
| Source IDs | E; S; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Preserve raw code and mapping version; state interval and event attribution must agree. |
| Model use | Independent source/state reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

## Shot and exposure primitives

### shot_outcome

**Ordinary shot outcome**

| Attribute | Definition |
|---|---|
| Field ID | shot_outcome |
| Name | Ordinary shot outcome |
| Family | Shot and exposure primitives |
| Role | EVIDENCE |
| Grain | Shot event |
| Priority | FOUNDATION |
| Definition / calculation | Mutually exclusive GOAL/SAVED_SOG/MISS/BLOCK for ordinary attempts; scoring exceptions retain separate class. |
| Data type | enum |
| Unit | category |
| Population / exposure | Ordinary events; exact phase/state |
| Window | EVENT |
| Source IDs | E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Reconcile event order, identity and eligible state; unknown remains explicit. |
| Model use | Shot-quality and participation reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### shot_type

**Shot type**

| Attribute | Definition |
|---|---|
| Field ID | shot_type |
| Name | Shot type |
| Family | Shot and exposure primitives |
| Role | EVIDENCE |
| Grain | Shot event |
| Priority | FOUNDATION |
| Definition / calculation | Preserve raw type plus normalized mapping (e.g. wrist, snap, slap, backhand, tip, deflection, wraparound, unknown). |
| Data type | enum |
| Unit | category |
| Population / exposure | Ordinary events; exact phase/state |
| Window | EVENT |
| Source IDs | E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Reconcile event order, identity and eligible state; unknown remains explicit. |
| Model use | Shot-quality and participation reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### shot_actors

**Shot actors**

| Attribute | Definition |
|---|---|
| Field ID | shot_actors |
| Name | Shot actors |
| Family | Shot and exposure primitives |
| Role | EVIDENCE |
| Grain | Shot event |
| Priority | FOUNDATION |
| Definition / calculation | Shooting team, shooter and goalie IDs plus blocker ID if relevant. A block event's team field must be resolved to shooting-team intent. |
| Data type | object |
| Unit | IDs |
| Population / exposure | Ordinary events; exact phase/state |
| Window | EVENT |
| Source IDs | E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Reconcile event order, identity and eligible state; unknown remains explicit. |
| Model use | Shot-quality and participation reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### shot_coordinates

**Shot coordinates**

| Attribute | Definition |
|---|---|
| Field ID | shot_coordinates |
| Name | Shot coordinates |
| Family | Shot and exposure primitives |
| Role | EVIDENCE |
| Grain | Shot event |
| Priority | FOUNDATION |
| Definition / calculation | Raw x/y plus coordinate units, attacking direction, origin-versus-block-location meaning and mapping version. |
| Data type | object&#124;null |
| Unit | feet after verified conversion |
| Population / exposure | Ordinary events; exact phase/state |
| Window | EVENT |
| Source IDs | E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Reconcile event order, identity and eligible state; unknown remains explicit. |
| Model use | Shot-quality and participation reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### shot_distance_ft

**Shot distance**

| Attribute | Definition |
|---|---|
| Field ID | shot_distance_ft |
| Name | Shot distance |
| Family | Shot and exposure primitives |
| Role | DESCRIPTIVE |
| Grain | Shot event |
| Priority | FOUNDATION |
| Definition / calculation | sqrt((goal_x-shot_x)^2+(goal_y-shot_y)^2) using verified goal-center geometry and shot-origin coordinates. |
| Data type | float&#124;null |
| Unit | feet |
| Population / exposure | Ordinary events; exact phase/state |
| Window | EVENT |
| Source IDs | E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Nonnegative within verified geometry; blocked location not assumed shot origin. |
| Model use | Shot-quality and participation reconstruction |
| Readiness | DERIVATION_NOT_BUILT |

### shot_angle_deg

**Shot angle**

| Attribute | Definition |
|---|---|
| Field ID | shot_angle_deg |
| Name | Shot angle |
| Family | Shot and exposure primitives |
| Role | DESCRIPTIVE |
| Grain | Shot event |
| Priority | FOUNDATION |
| Definition / calculation | Absolute atan2(lateral offset, forward distance to goal)*180/pi after offensive-direction normalization; behind-goal events retained if valid. |
| Data type | float&#124;null |
| Unit | degrees |
| Population / exposure | Ordinary events; exact phase/state |
| Window | EVENT |
| Source IDs | E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | 0..180; unit, goal geometry, coordinate meaning and direction verified. |
| Model use | Shot-quality and participation reconstruction |
| Readiness | DERIVATION_NOT_BUILT |

### previous_event_context

**Previous event context**

| Attribute | Definition |
|---|---|
| Field ID | previous_event_context |
| Name | Previous event context |
| Family | Shot and exposure primitives |
| Role | EVIDENCE |
| Grain | Shot event |
| Priority | SUPPORTING |
| Definition / calculation | Previous available event type, elapsed game-clock seconds and spatial displacement; strict ordering before this shot. |
| Data type | object&#124;null |
| Unit | seconds/feet/category |
| Population / exposure | Ordinary events; exact phase/state |
| Window | EVENT |
| Source IDs | E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Reconcile event order, identity and eligible state; unknown remains explicit. |
| Model use | Shot-quality and participation reconstruction |
| Readiness | SOURCE_MAPPING_REQUIRED |

### shift_age_seconds

**Shift age at event**

| Attribute | Definition |
|---|---|
| Field ID | shift_age_seconds |
| Name | Shift age at event |
| Family | Shot and exposure primitives |
| Role | DESCRIPTIVE |
| Grain | Shot event |
| Priority | SUPPORTING |
| Definition / calculation | Playing seconds since current shift began for participating skaters; require valid continuous participation. |
| Data type | object&#124;null |
| Unit | seconds |
| Population / exposure | Ordinary events; exact phase/state |
| Window | EVENT |
| Source IDs | S; E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Reconcile event order, identity and eligible state; unknown remains explicit. |
| Model use | Shot-quality and participation reconstruction |
| Readiness | DERIVATION_NOT_BUILT |

### shot_is_sog_label

**On-target training label**

| Attribute | Definition |
|---|---|
| Field ID | shot_is_sog_label |
| Name | On-target training label |
| Family | Shot and exposure primitives |
| Role | TRAINING_LABEL |
| Grain | Shot event |
| Priority | FOUNDATION |
| Definition / calculation | 1 for ordinary GOAL or SAVED_SOG, 0 for MISS, defined only on eligible unblocked attempts. Outcome is not a covariate. |
| Data type | boolean |
| Unit | 0/1 |
| Population / exposure | Eligible ordinary UA only (GOAL/SAVED_SOG/MISS) |
| Window | EVENT |
| Source IDs | E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Outcome belongs only in chronological training labels; no label-derived input. |
| Model use | Shot-model training target |
| Readiness | DERIVATION_NOT_BUILT |

### shot_is_goal_label

**Goal training label**

| Attribute | Definition |
|---|---|
| Field ID | shot_is_goal_label |
| Name | Goal training label |
| Family | Shot and exposure primitives |
| Role | TRAINING_LABEL |
| Grain | Shot event |
| Priority | FOUNDATION |
| Definition / calculation | 1 for ordinary physical GOAL and 0 for SAVED_SOG in the conditional-r training sample. Training target only, never a pre-outcome input. |
| Data type | boolean |
| Unit | 0/1 |
| Population / exposure | Eligible ordinary SOG for conditional r model |
| Window | EVENT |
| Source IDs | E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Outcome belongs only in chronological training labels; no label-derived input. |
| Model use | Shot-model training target |
| Readiness | DERIVATION_NOT_BUILT |

### eligible_playing_seconds

**Eligible playing exposure**

| Attribute | Definition |
|---|---|
| Field ID | eligible_playing_seconds |
| Name | Eligible playing exposure |
| Family | Shot and exposure primitives |
| Role | DESCRIPTIVE |
| Grain | Team / player / state interval |
| Priority | FOUNDATION |
| Definition / calculation | Duration of union of valid participant/state intervals in seconds; stoppages excluded and boundary events assigned once. |
| Data type | float |
| Unit | seconds |
| Population / exposure | Eligible playing intervals in declared phase/state, including zero-shot intervals |
| Window | INTERVAL |
| Source IDs | S; E; B1 |
| Availability rule | Use selected immutable revision with available_at <= forecast cutoff T; no future correction. |
| Missing-data rule | Null + MISSING/CONFLICT; block dependent feature or use a predeclared validated alternative. |
| Validation | Reconcile event order, identity and eligible state; unknown remains explicit. |
| Model use | Shot-quality and participation reconstruction |
| Readiness | DERIVATION_NOT_BUILT |

## Team counts

### team_goals_for

**Physical goals for**

| Attribute | Definition |
|---|---|
| Field ID | team_goals_for |
| Name | Physical goals for |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | Count ordinary physical goals credited to the team in the selected population. |
| Data type | integer&#124;null |
| Unit | goals |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_goals_against

**Physical goals against**

| Attribute | Definition |
|---|---|
| Field ID | team_goals_against |
| Name | Physical goals against |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | Count opponent ordinary physical goals in the same population. |
| Data type | integer&#124;null |
| Unit | goals |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_sog_for

**Shots on goal for**

| Attribute | Definition |
|---|---|
| Field ID | team_sog_for |
| Name | Shots on goal for |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | Count GOAL + SAVED_SOG by the team. |
| Data type | integer&#124;null |
| Unit | shots |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_sog_against

**Shots on goal against**

| Attribute | Definition |
|---|---|
| Field ID | team_sog_against |
| Name | Shots on goal against |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | Count opponent GOAL + SAVED_SOG. |
| Data type | integer&#124;null |
| Unit | shots |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_misses_for

**Missed shots for**

| Attribute | Definition |
|---|---|
| Field ID | team_misses_for |
| Name | Missed shots for |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | Count team MISS events; no SOG credit. |
| Data type | integer&#124;null |
| Unit | attempts |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_misses_against

**Missed shots against**

| Attribute | Definition |
|---|---|
| Field ID | team_misses_against |
| Name | Missed shots against |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | Count opponent MISS events. |
| Data type | integer&#124;null |
| Unit | attempts |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_blocked_attempts_for

**Offensive attempts blocked**

| Attribute | Definition |
|---|---|
| Field ID | team_blocked_attempts_for |
| Name | Offensive attempts blocked |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | Count BLOCK attempts shot by own team; different from defensive blocks by own players. |
| Data type | integer&#124;null |
| Unit | attempts |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_blocked_attempts_against

**Opposing attempts blocked**

| Attribute | Definition |
|---|---|
| Field ID | team_blocked_attempts_against |
| Name | Opposing attempts blocked |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | Count opponent BLOCK attempts stopped by own team. |
| Data type | integer&#124;null |
| Unit | attempts |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_corsi_for

**Corsi for**

| Attribute | Definition |
|---|---|
| Field ID | team_corsi_for |
| Name | Corsi for |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | SOG_for + misses_for + blocked_attempts_for. |
| Data type | integer&#124;null |
| Unit | attempts |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_corsi_against

**Corsi against**

| Attribute | Definition |
|---|---|
| Field ID | team_corsi_against |
| Name | Corsi against |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | SOG_against + misses_against + blocked_attempts_against. |
| Data type | integer&#124;null |
| Unit | attempts |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_fenwick_for

**Fenwick for**

| Attribute | Definition |
|---|---|
| Field ID | team_fenwick_for |
| Name | Fenwick for |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | SOG_for + misses_for. |
| Data type | integer&#124;null |
| Unit | attempts |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_fenwick_against

**Fenwick against**

| Attribute | Definition |
|---|---|
| Field ID | team_fenwick_against |
| Name | Fenwick against |
| Family | Team counts |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | FOUNDATION |
| Definition / calculation | SOG_against + misses_against. |
| Data type | integer&#124;null |
| Unit | attempts |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null if source population incomplete; known no events in complete eligible window is count 0. |
| Validation | SOG=GOAL+SAVE; FF=SOG+MISS; CF=FF+BLOCK in matching scope. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

## Team rates and shares

### team_gf_per60

**Goal production rate**

| Attribute | Definition |
|---|---|
| Field ID | team_gf_per60 |
| Name | Goal production rate |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * goals_for / eligible_team_seconds |
| Data type | float&#124;null |
| Unit | goals per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Nonnegative count rate with positive matching exposure. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_ga_per60

**Goal allowance rate**

| Attribute | Definition |
|---|---|
| Field ID | team_ga_per60 |
| Name | Goal allowance rate |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * goals_against / eligible_team_seconds |
| Data type | float&#124;null |
| Unit | goals per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Nonnegative count rate with positive matching exposure. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_sf_per60

**SOG production rate**

| Attribute | Definition |
|---|---|
| Field ID | team_sf_per60 |
| Name | SOG production rate |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * sog_for / eligible_team_seconds |
| Data type | float&#124;null |
| Unit | shots per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Nonnegative count rate with positive matching exposure. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_sa_per60

**SOG allowance rate**

| Attribute | Definition |
|---|---|
| Field ID | team_sa_per60 |
| Name | SOG allowance rate |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * sog_against / eligible_team_seconds |
| Data type | float&#124;null |
| Unit | shots per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Nonnegative count rate with positive matching exposure. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_cf_per60

**Attempt production rate**

| Attribute | Definition |
|---|---|
| Field ID | team_cf_per60 |
| Name | Attempt production rate |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * corsi_for / eligible_team_seconds |
| Data type | float&#124;null |
| Unit | attempts per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Nonnegative count rate with positive matching exposure. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_ca_per60

**Attempt allowance rate**

| Attribute | Definition |
|---|---|
| Field ID | team_ca_per60 |
| Name | Attempt allowance rate |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * corsi_against / eligible_team_seconds |
| Data type | float&#124;null |
| Unit | attempts per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Nonnegative count rate with positive matching exposure. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_ff_per60

**Unblocked-attempt production rate**

| Attribute | Definition |
|---|---|
| Field ID | team_ff_per60 |
| Name | Unblocked-attempt production rate |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * fenwick_for / eligible_team_seconds |
| Data type | float&#124;null |
| Unit | attempts per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Nonnegative count rate with positive matching exposure. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_fa_per60

**Unblocked-attempt allowance rate**

| Attribute | Definition |
|---|---|
| Field ID | team_fa_per60 |
| Name | Unblocked-attempt allowance rate |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * fenwick_against / eligible_team_seconds |
| Data type | float&#124;null |
| Unit | attempts per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Nonnegative count rate with positive matching exposure. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_cf_share

**Corsi share**

| Attribute | Definition |
|---|---|
| Field ID | team_cf_share |
| Name | Corsi share |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | corsi_for / (corsi_for + corsi_against) |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | 0..1 with positive matching denominator. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_ff_share

**Fenwick share**

| Attribute | Definition |
|---|---|
| Field ID | team_ff_share |
| Name | Fenwick share |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | fenwick_for / (fenwick_for + fenwick_against) |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | 0..1 with positive matching denominator. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_sf_share

**SOG share**

| Attribute | Definition |
|---|---|
| Field ID | team_sf_share |
| Name | SOG share |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | sog_for / (sog_for + sog_against) |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | 0..1 with positive matching denominator. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_shooting_fraction

**Team shooting fraction**

| Attribute | Definition |
|---|---|
| Field ID | team_shooting_fraction |
| Name | Team shooting fraction |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | goals_for / sog_for; same ordinary-shot universe |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | 0..1 with positive matching denominator. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_save_fraction

**Team save fraction**

| Attribute | Definition |
|---|---|
| Field ID | team_save_fraction |
| Name | Team save fraction |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | (sog_against - goals_against) / sog_against; both-goalie-present scope only |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | 0..1 with positive matching denominator. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_pdo_fraction

**PDO fraction**

| Attribute | Definition |
|---|---|
| Field ID | team_pdo_fraction |
| Name | PDO fraction |
| Family | Team rates and shares |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | SUPPORTING |
| Definition / calculation | team_shooting_fraction + team_save_fraction in identical state/window; store fraction-sum (near 1), display x100 only with label |
| Data type | float&#124;null |
| Unit | fraction sum |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | 0..2; both components known and scoped identically. Does not impose mandatory regression. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

## Team shot quality

### team_xgf_ua

**TDL xG for, unblocked basis**

| Attribute | Definition |
|---|---|
| Field ID | team_xgf_ua |
| Name | TDL xG for, unblocked basis |
| Family | Team shot quality |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | SUM(internal q_sog_i * internal r_goal_given_sog_i) over own eligible ordinary unblocked attempts. |
| Data type | float&#124;null |
| Unit | expected goals |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Eligible historical events rescored only by internal model permitted by fold/cutoff; retain model version. |
| Missing-data rule | Incomplete required xG coverage -> full-population model value null unless a validated missingness estimator applies. Partial sums are separate diagnostics with their own scored population. |
| Validation | Matching UA basis, state, exposure and model; expected-goal sum bounded by eligible UA count. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | MODEL_NOT_BUILT |

### team_xga_ua

**TDL xG against, unblocked basis**

| Attribute | Definition |
|---|---|
| Field ID | team_xga_ua |
| Name | TDL xG against, unblocked basis |
| Family | Team shot quality |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | SUM(internal q_sog_i * internal r_goal_given_sog_i) over opponent eligible ordinary unblocked attempts. |
| Data type | float&#124;null |
| Unit | expected goals |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Eligible historical events rescored only by internal model permitted by fold/cutoff; retain model version. |
| Missing-data rule | Incomplete required xG coverage -> full-population model value null unless a validated missingness estimator applies. Partial sums are separate diagnostics with their own scored population. |
| Validation | Matching UA basis, state, exposure and model; expected-goal sum bounded by eligible UA count. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | MODEL_NOT_BUILT |

### team_xgf_per60

**TDL xG production rate**

| Attribute | Definition |
|---|---|
| Field ID | team_xgf_per60 |
| Name | TDL xG production rate |
| Family | Team shot quality |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * team_xgf_ua / eligible_team_seconds. |
| Data type | float&#124;null |
| Unit | expected goals per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Eligible historical events rescored only by internal model permitted by fold/cutoff; retain model version. |
| Missing-data rule | Incomplete required xG coverage -> full-population model value null unless a validated missingness estimator applies. Partial sums are separate diagnostics with their own scored population. |
| Validation | Matching UA basis, state, exposure and model; expected-goal sum bounded by eligible UA count. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | MODEL_NOT_BUILT |

### team_xga_per60

**TDL xG allowance rate**

| Attribute | Definition |
|---|---|
| Field ID | team_xga_per60 |
| Name | TDL xG allowance rate |
| Family | Team shot quality |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * team_xga_ua / eligible_team_seconds. |
| Data type | float&#124;null |
| Unit | expected goals per 60 |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Eligible historical events rescored only by internal model permitted by fold/cutoff; retain model version. |
| Missing-data rule | Incomplete required xG coverage -> full-population model value null unless a validated missingness estimator applies. Partial sums are separate diagnostics with their own scored population. |
| Validation | Matching UA basis, state, exposure and model; expected-goal sum bounded by eligible UA count. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | MODEL_NOT_BUILT |

### team_xgf_share

**TDL xG share**

| Attribute | Definition |
|---|---|
| Field ID | team_xgf_share |
| Name | TDL xG share |
| Family | Team shot quality |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | team_xgf_ua / (team_xgf_ua + team_xga_ua). |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Eligible historical events rescored only by internal model permitted by fold/cutoff; retain model version. |
| Missing-data rule | Incomplete required xG coverage -> full-population model value null unless a validated missingness estimator applies. Partial sums are separate diagnostics with their own scored population. |
| Validation | 0..1; matching own/opponent xG basis and model version. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | MODEL_NOT_BUILT |

### team_xg_per_ua

**TDL quality per unblocked attempt**

| Attribute | Definition |
|---|---|
| Field ID | team_xg_per_ua |
| Name | TDL quality per unblocked attempt |
| Family | Team shot quality |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | team_xgf_ua / eligible_own_unblocked_attempt_count. |
| Data type | float&#124;null |
| Unit | expected goals per attempt |
| Population / exposure | REG5V5 default; explicit REG5V4/REG4V5/other-state variants |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Eligible historical events rescored only by internal model permitted by fold/cutoff; retain model version. |
| Missing-data rule | Incomplete required xG coverage -> full-population model value null unless a validated missingness estimator applies. Partial sums are separate diagnostics with their own scored population. |
| Validation | 0..1 with positive UA count. Complete scored population, or a validated missingness estimator; scored-subset diagnostics must be separately identified. Coverage metadata alone does not authorize a partial numerator over all UA. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | MODEL_NOT_BUILT |

## Special teams

### team_official_pp_opportunities

**Official PP opportunities**

| Attribute | Definition |
|---|---|
| Field ID | team_official_pp_opportunities |
| Name | Official PP opportunities |
| Family | Special teams |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Provider-defined official team power-play opportunity count with rule/scoring version; not penalties assessed. |
| Data type | float&#124;null |
| Unit | opportunities |
| Population / exposure | Official PP reporting domain |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D3 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Reconcile to official opportunity/goal attribution for the chosen rule version; positive denominator for ratios. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_official_pk_opportunities

**Official shorthanded situations**

| Attribute | Definition |
|---|---|
| Field ID | team_official_pk_opportunities |
| Name | Official shorthanded situations |
| Family | Special teams |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Official opponent power-play opportunities faced by team with identical reporting contract. |
| Data type | float&#124;null |
| Unit | situations |
| Population / exposure | Official PK reporting domain |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D3 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Reconcile to official opportunity/goal attribution for the chosen rule version; positive denominator for ratios. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_official_pp_fraction

**Official PP conversion**

| Attribute | Definition |
|---|---|
| Field ID | team_official_pp_fraction |
| Name | Official PP conversion |
| Family | Special teams |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Official power-play goals / official PP opportunities. Retain official PP goal attribution. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Official PP reporting domain |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D3 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Reconcile to official opportunity/goal attribution for the chosen rule version; positive denominator for ratios. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_official_pk_fraction

**Official PK success**

| Attribute | Definition |
|---|---|
| Field ID | team_official_pk_fraction |
| Name | Official PK success |
| Family | Special teams |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 1 - official PP goals allowed / official shorthanded situations. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Official PK reporting domain |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D3 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Reconcile to official opportunity/goal attribution for the chosen rule version; positive denominator for ratios. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_penalties_taken_rate

**Penalties taken rate**

| Attribute | Definition |
|---|---|
| Field ID | team_penalties_taken_rate |
| Name | Penalties taken rate |
| Family | Special teams |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * penalties_taken_of_declared_type / matching_team_seconds; identify manpower consequences separately. |
| Data type | float&#124;null |
| Unit | penalties per 60 |
| Population / exposure | Type-specific eligible regulation states |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D3 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Use exact penalty/manpower and clock exposure; preserve paired goalie presence. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_penalties_drawn_rate

**Penalties drawn rate**

| Attribute | Definition |
|---|---|
| Field ID | team_penalties_drawn_rate |
| Name | Penalties drawn rate |
| Family | Special teams |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * penalties_drawn_of_declared_type / matching_team_seconds; do not infer from total PIM. |
| Data type | float&#124;null |
| Unit | penalties per 60 |
| Population / exposure | Type-specific eligible regulation states |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D3 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Use exact penalty/manpower and clock exposure; preserve paired goalie presence. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

### team_pp_xgf_per60

**PP shot-quality production**

| Attribute | Definition |
|---|---|
| Field ID | team_pp_xgf_per60 |
| Name | PP shot-quality production |
| Family | Special teams |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * own internal UA xG in exact PP state / exact_PP_state_seconds. |
| Data type | float&#124;null |
| Unit | expected goals per 60 |
| Population / exposure | REG5V4 default; separate 5v3/4v3/etc |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Use exact penalty/manpower and clock exposure; preserve paired goalie presence. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | MODEL_NOT_BUILT |

### team_pk_xga_per60

**PK shot-quality concession**

| Attribute | Definition |
|---|---|
| Field ID | team_pk_xga_per60 |
| Name | PK shot-quality concession |
| Family | Special teams |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * opponent internal UA xG in exact PK state / exact_PK_state_seconds. |
| Data type | float&#124;null |
| Unit | expected goals per 60 |
| Population / exposure | REG4V5 default; separate 3v5/3v4/etc |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Use exact penalty/manpower and clock exposure; preserve paired goalie presence. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | MODEL_NOT_BUILT |

### team_pp_exposure_share

**PP exposure share**

| Attribute | Definition |
|---|---|
| Field ID | team_pp_exposure_share |
| Name | PP exposure share |
| Family | Special teams |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Seconds with verified penalty advantage / total eligible regulation seconds. Overlaps with extra-attacker flags are retained, not double-counted. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Regulation; penalty advantage dimension |
| Window | S2D; G10; G20 |
| Source IDs | E; B1; D3 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Null when denominator/input population is missing or zero exposure; retain counts, exposure and reason. Known zero over positive complete exposure is 0. |
| Validation | Use exact penalty/manpower and clock exposure; preserve paired goalie presence. |
| Model use | Candidate independent feature; selection requires chronological validation |
| Readiness | DERIVATION_NOT_BUILT |

## Team supporting features

### team_record_by_result_type

**Record by result type**

| Attribute | Definition |
|---|---|
| Field ID | team_record_by_result_type |
| Name | Record by result type |
| Family | Team supporting features |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | SUPPORTING |
| Definition / calculation | Counts of regulation wins/losses, OT wins/losses and SO wins/losses; completed games only. |
| Data type | object |
| Unit | object |
| Population / exposure | Completed games; explicit REGULAR/PLAYOFFS |
| Window | S2D; G10; G20 |
| Source IDs | E; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | DERIVATION_NOT_BUILT |

### team_goals_per_game

**Physical goals per game**

| Attribute | Definition |
|---|---|
| Field ID | team_goals_per_game |
| Name | Physical goals per game |
| Family | Team supporting features |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | SUPPORTING |
| Definition / calculation | Ordinary physical goals over chosen completed-game population / eligible completed games; name phase/empty-net exclusions explicitly. |
| Data type | float&#124;null |
| Unit | goals per game |
| Population / exposure | Declared whole-game or regulation domain |
| Window | S2D; G10; G20 |
| Source IDs | E; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | DERIVATION_NOT_BUILT |

### team_faceoff_win_share

**Faceoff win share**

| Attribute | Definition |
|---|---|
| Field ID | team_faceoff_win_share |
| Name | Faceoff win share |
| Family | Team supporting features |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | SUPPORTING |
| Definition / calculation | Faceoffs won / (faceoffs won + lost) in declared zone and strength. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Zone/state faceoff events |
| Window | S2D; G10; G20 |
| Source IDs | E; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | DERIVATION_NOT_BUILT |

### team_supporting_event_rate

**Supporting event rate**

| Attribute | Definition |
|---|---|
| Field ID | team_supporting_event_rate |
| Name | Supporting event rate |
| Family | Team supporting features |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | SUPPORTING |
| Definition / calculation | 3600 * chosen factual hits/takeaways/giveaways/defensive_blocks / matching seconds; event_type is part of feature key. |
| Data type | float&#124;null |
| Unit | events per 60 |
| Population / exposure | Declared state and source event taxonomy |
| Window | S2D; G10; G20 |
| Source IDs | E; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | DERIVATION_NOT_BUILT |

### team_score_state_exposure_share

**Score-state exposure share**

| Attribute | Definition |
|---|---|
| Field ID | team_score_state_exposure_share |
| Name | Score-state exposure share |
| Family | Team supporting features |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | SUPPORTING |
| Definition / calculation | Eligible seconds in leading/tied/trailing or exact-margin bin / total selected-state seconds; score before event. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | REG5V5 by pre-event score bin |
| Window | S2D; G10; G20 |
| Source IDs | E; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | DERIVATION_NOT_BUILT |

### team_opponent_adjusted_rate

**Opponent-adjusted rate**

| Attribute | Definition |
|---|---|
| Field ID | team_opponent_adjusted_rate |
| Name | Opponent-adjusted rate |
| Family | Team supporting features |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | SUPPORTING |
| Definition / calculation | Internal fitted rate standardized to a declared opponent/reference distribution; exact model and coefficient set versioned. |
| Data type | float&#124;null |
| Unit | rate in declared units |
| Population / exposure | State/metric matching underlying rate |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | MODEL_NOT_BUILT |

### team_score_adjusted_rate

**Score-adjusted rate**

| Attribute | Definition |
|---|---|
| Field ID | team_score_adjusted_rate |
| Name | Score-adjusted rate |
| Family | Team supporting features |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | SUPPORTING |
| Definition / calculation | Internal model standardizes event rate to declared score-state/reference mix. Fit only on permitted training history. |
| Data type | float&#124;null |
| Unit | rate in declared units |
| Population / exposure | State/metric matching underlying rate |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | MODEL_NOT_BUILT |

### team_danger_chance_rate

**TDL danger chance rate**

| Attribute | Definition |
|---|---|
| Field ID | team_danger_chance_rate |
| Name | TDL danger chance rate |
| Family | Team supporting features |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | LATER |
| Definition / calculation | 3600 * chances meeting future versioned TDL danger rule / matching seconds. Region/probability threshold not selected in v0.1. |
| Data type | float&#124;null |
| Unit | chances per 60 |
| Population / exposure | Declared chance rule and state |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | MODEL_NOT_BUILT |

### team_rebound_rush_rate

**TDL rebound/rush proxy rate**

| Attribute | Definition |
|---|---|
| Field ID | team_rebound_rush_rate |
| Name | TDL rebound/rush proxy rate |
| Family | Team supporting features |
| Role | DESCRIPTIVE |
| Grain | Team at forecast cutoff |
| Priority | LATER |
| Definition / calculation | Count or rate of future versioned observed/tagged/sequence-inferred category. Proxy definition and validation not selected in v0.1. |
| Data type | float&#124;null |
| Unit | events per 60 |
| Population / exposure | Declared sequence population |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | MODEL_NOT_BUILT |

### team_flurry_sequence_feature

**TDL flurry feature**

| Attribute | Definition |
|---|---|
| Field ID | team_flurry_sequence_feature |
| Name | TDL flurry feature |
| Family | Team supporting features |
| Role | INTERNAL_ESTIMATE |
| Grain | Team at forecast cutoff |
| Priority | LATER |
| Definition / calculation | Future sequence model distinguishes realized xG sum from conditional possession scoring probability. Sequence segmentation remains undecided. |
| Data type | float&#124;null |
| Unit | declared by model |
| Population / exposure | Declared sequence population |
| Window | S2D; G10; G20 |
| Source IDs | E; I; B1 |
| Availability rule | Aggregate only selected completed historical games and revisions available by T. |
| Missing-data rule | Missing source/denominator -> null. Undecided derived definitions stay inactive; do not assign arbitrary thresholds. |
| Validation | Matching entity/state/window and complete numerator/denominator; no average of per-game rates. |
| Model use | Diagnostic or later feature group; prove incremental value before selecting |
| Readiness | MODEL_NOT_BUILT |

## Goalie performance

### goalie_sog_faced

**Goalie SOG faced**

| Attribute | Definition |
|---|---|
| Field ID | goalie_sog_faced |
| Name | Goalie SOG faced |
| Family | Goalie performance |
| Role | DESCRIPTIVE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Count eligible ordinary GOAL + SAVED_SOG assigned to this goalie. |
| Data type | float&#124;null |
| Unit | shots |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | DERIVATION_NOT_BUILT |

### goalie_goals_allowed

**Goalie goals allowed**

| Attribute | Definition |
|---|---|
| Field ID | goalie_goals_allowed |
| Name | Goalie goals allowed |
| Family | Goalie performance |
| Role | DESCRIPTIVE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Count eligible physical goals from that same assigned SOG population. |
| Data type | float&#124;null |
| Unit | goals |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | DERIVATION_NOT_BUILT |

### goalie_saves

**Goalie saves**

| Attribute | Definition |
|---|---|
| Field ID | goalie_saves |
| Name | Goalie saves |
| Family | Goalie performance |
| Role | DESCRIPTIVE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | goalie_sog_faced - goalie_goals_allowed. |
| Data type | float&#124;null |
| Unit | saves |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | DERIVATION_NOT_BUILT |

### goalie_sv_fraction

**Goalie save fraction**

| Attribute | Definition |
|---|---|
| Field ID | goalie_sv_fraction |
| Name | Goalie save fraction |
| Family | Goalie performance |
| Role | DESCRIPTIVE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | goalie_saves / goalie_sog_faced. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | DERIVATION_NOT_BUILT |

### goalie_ga_per60

**Goalie goals allowed rate**

| Attribute | Definition |
|---|---|
| Field ID | goalie_ga_per60 |
| Name | Goalie goals allowed rate |
| Family | Goalie performance |
| Role | DESCRIPTIVE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * eligible goalie_goals_allowed / occupied eligible goalie_seconds. Declare ordinary-shot exclusions; this may differ from full official GAA. |
| Data type | float&#124;null |
| Unit | goals per 60 |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | DERIVATION_NOT_BUILT |

### goalie_xga_sog

**TDL goalie xGA on SOG**

| Attribute | Definition |
|---|---|
| Field ID | goalie_xga_sog |
| Name | TDL goalie xGA on SOG |
| Family | Goalie performance |
| Role | INTERNAL_ESTIMATE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | SUM(internal neutral r_goal_given_sog_i) over eligible actual SOG faced. Not SUM(q_sog_i*r_i) across misses. |
| Data type | float&#124;null |
| Unit | expected goals |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Incomplete xG scoring -> full-population value null absent a validated estimator. Any scored-subset diagnostic must use the same subset for xGA, SOG and GA and expose coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | MODEL_NOT_BUILT |

### goalie_gsax_sog

**TDL goalie GSAx on SOG**

| Attribute | Definition |
|---|---|
| Field ID | goalie_gsax_sog |
| Name | TDL goalie GSAx on SOG |
| Family | Goalie performance |
| Role | INTERNAL_ESTIMATE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | goalie_xga_sog - goalie_goals_allowed; positive means goals prevented above declared SOG baseline. |
| Data type | float&#124;null |
| Unit | goals saved |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Incomplete xG scoring -> full-population value null absent a validated estimator. Any scored-subset diagnostic must use the same subset for xGA, SOG and GA and expose coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | MODEL_NOT_BUILT |

### goalie_gsax_sog_per60

**TDL goalie GSAx per 60**

| Attribute | Definition |
|---|---|
| Field ID | goalie_gsax_sog_per60 |
| Name | TDL goalie GSAx per 60 |
| Family | Goalie performance |
| Role | INTERNAL_ESTIMATE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * goalie_gsax_sog / eligible occupied goalie_seconds. |
| Data type | float&#124;null |
| Unit | goals saved per 60 |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Incomplete xG scoring -> full-population value null absent a validated estimator. Any scored-subset diagnostic must use the same subset for xGA, SOG and GA and expose coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | MODEL_NOT_BUILT |

### goalie_gsax_sog_per100

**TDL goalie GSAx per 100 SOG**

| Attribute | Definition |
|---|---|
| Field ID | goalie_gsax_sog_per100 |
| Name | TDL goalie GSAx per 100 SOG |
| Family | Goalie performance |
| Role | INTERNAL_ESTIMATE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 100 * goalie_gsax_sog / goalie_sog_faced. |
| Data type | float&#124;null |
| Unit | goals saved per 100 SOG |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Incomplete xG scoring -> full-population value null absent a validated estimator. Any scored-subset diagnostic must use the same subset for xGA, SOG and GA and expose coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | MODEL_NOT_BUILT |

### goalie_xsv_fraction_sog

**TDL expected save fraction**

| Attribute | Definition |
|---|---|
| Field ID | goalie_xsv_fraction_sog |
| Name | TDL expected save fraction |
| Family | Goalie performance |
| Role | INTERNAL_ESTIMATE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 1 - goalie_xga_sog / goalie_sog_faced, using the conditional-on-SOG neutral baseline. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Incomplete xG scoring -> full-population value null absent a validated estimator. Any scored-subset diagnostic must use the same subset for xGA, SOG and GA and expose coverage. |
| Validation | Exclude empty net/SO/penalty-shot/awarded-goal exceptions by default. Match goalie ID, SOG population and exposure. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | MODEL_NOT_BUILT |

### goalie_sv_above_expected

**TDL save fraction above expected**

| Attribute | Definition |
|---|---|
| Field ID | goalie_sv_above_expected |
| Name | TDL save fraction above expected |
| Family | Goalie performance |
| Role | INTERNAL_ESTIMATE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | goalie_sv_fraction - goalie_xsv_fraction_sog = goalie_gsax_sog / goalie_sog_faced. |
| Data type | float&#124;null |
| Unit | fraction difference |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Incomplete xG scoring -> full-population value null absent a validated estimator. Any scored-subset diagnostic must use the same subset for xGA, SOG and GA and expose coverage. |
| Validation | Difference identity must hold on matching SOG population; do not multiply to percentage points twice. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | MODEL_NOT_BUILT |

### goalie_stopping_effect

**TDL goalie stopping effect**

| Attribute | Definition |
|---|---|
| Field ID | goalie_stopping_effect |
| Name | TDL goalie stopping effect |
| Family | Goalie performance |
| Role | INTERNAL_ESTIMATE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Hierarchically estimated stopping ability relative to neutral reference. Proposed positive effect reduces goal log-odds; model/link/prior undecided. |
| Data type | float&#124;null |
| Unit | model parameter |
| Population / exposure | Goalie-present ordinary SOG, assigned goalie, declared phase/state |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Training-only hierarchy; reference identified; not raw GSAx subtracted from next forecast. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | MODEL_NOT_BUILT |

### goalie_workload

**Goalie workload**

| Attribute | Definition |
|---|---|
| Field ID | goalie_workload |
| Name | Goalie workload |
| Family | Goalie performance |
| Role | DESCRIPTIVE |
| Grain | Goalie at forecast cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Starts, relief appearances, seconds and SOG faced in exact D7/D14 history; each component retained, not an unexplained composite score. |
| Data type | object |
| Unit | object |
| Population / exposure | Verified goalie appearances/occupied intervals; SOG component uses declared ordinary-shot population |
| Window | D7; D14 |
| Source IDs | E; S; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Counts refer to completed history; start and relief remain distinct; timestamps in UTC. |
| Model use | Independent goalie/player/context modeling candidate |
| Readiness | DERIVATION_NOT_BUILT |

## Lineup and confirmation

### goalie_candidate_status

**Goalie candidate status**

| Attribute | Definition |
|---|---|
| Field ID | goalie_candidate_status |
| Name | Goalie candidate status |
| Family | Lineup and confirmation |
| Role | EVIDENCE |
| Grain | Goalie candidate / target game |
| Priority | FOUNDATION |
| Definition / calculation | Candidate goalie ID plus CONFIRMED/PROBABLE/UNANNOUNCED/CONFLICTING/RULED_OUT, attributable source and time. Separate projected and confirmed IDs. |
| Data type | object |
| Unit | object |
| Population / exposure | Pregame state |
| Window | SNAPSHOT |
| Source IDs | A; B1 |
| Availability rule | Announcement/observation available by T and applicable to target game; late changes make new snapshots. |
| Missing-data rule | Unknown/conflict remains explicit. Restrict dependent projections or use documented scenarios. |
| Validation | Identity and source evidence agree; odds never establish confirmation. |
| Model use | Lineup state, conditional scenarios and opportunity allocation |
| Readiness | SOURCE_MAPPING_REQUIRED |

### goalie_scenario_weight

**TDL starter scenario weight**

| Attribute | Definition |
|---|---|
| Field ID | goalie_scenario_weight |
| Name | TDL starter scenario weight |
| Family | Lineup and confirmation |
| Role | INTERNAL_ESTIMATE |
| Grain | Goalie candidate / target game |
| Priority | FOUNDATION |
| Definition / calculation | Internally justified probability for a candidate starter. No arbitrary conversion of PROBABLE into a percentage; weights required only when making a mixture. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Pregame state |
| Window | SNAPSHOT |
| Source IDs | A; I; B1 |
| Availability rule | Announcement/observation available by T and applicable to target game; late changes make new snapshots. |
| Missing-data rule | Null -> retain named conditional forecasts, no mixture; do not silently use 0.5. |
| Validation | 0..1; candidate mixture weights sum to 1 only when valid and all live candidates represented. |
| Model use | Lineup state, conditional scenarios and opportunity allocation |
| Readiness | MODEL_NOT_BUILT |

### skater_availability_status

**Skater availability**

| Attribute | Definition |
|---|---|
| Field ID | skater_availability_status |
| Name | Skater availability |
| Family | Lineup and confirmation |
| Role | EVIDENCE |
| Grain | Skater / target game |
| Priority | FOUNDATION |
| Definition / calculation | ACTIVE/OUT/QUESTIONABLE/SCRATCHED/UNKNOWN or source-mapped categories, plus confirmed/reported/projected level and source times. |
| Data type | object |
| Unit | object |
| Population / exposure | Pregame state |
| Window | SNAPSHOT |
| Source IDs | A; B1 |
| Availability rule | Announcement/observation available by T and applicable to target game; late changes make new snapshots. |
| Missing-data rule | Unknown/conflict remains explicit. Restrict dependent projections or use documented scenarios. |
| Validation | Identity and source evidence agree; odds never establish confirmation. |
| Model use | Lineup state, conditional scenarios and opportunity allocation |
| Readiness | SOURCE_MAPPING_REQUIRED |

### line_pair_assignment

**Line/pair evidence**

| Attribute | Definition |
|---|---|
| Field ID | line_pair_assignment |
| Name | Line/pair evidence |
| Family | Lineup and confirmation |
| Role | EVIDENCE |
| Grain | Skater / target game |
| Priority | FOUNDATION |
| Definition / calculation | Skater combination membership and supporting observation, with phase/strength and effective time; a morning projection is not a confirmed game lineup. |
| Data type | object |
| Unit | object |
| Population / exposure | Pregame state |
| Window | SNAPSHOT |
| Source IDs | A; B1 |
| Availability rule | Announcement/observation available by T and applicable to target game; late changes make new snapshots. |
| Missing-data rule | Unknown/conflict remains explicit. Restrict dependent projections or use documented scenarios. |
| Validation | Identity and source evidence agree; odds never establish confirmation. |
| Model use | Lineup state, conditional scenarios and opportunity allocation |
| Readiness | SOURCE_MAPPING_REQUIRED |

### special_team_unit_assignment

**PP/PK unit evidence**

| Attribute | Definition |
|---|---|
| Field ID | special_team_unit_assignment |
| Name | PP/PK unit evidence |
| Family | Lineup and confirmation |
| Role | EVIDENCE |
| Grain | Skater / target game |
| Priority | FOUNDATION |
| Definition / calculation | Reported/confirmed power-play and penalty-kill unit membership with source/version; preserve uncertainty. |
| Data type | object |
| Unit | object |
| Population / exposure | Pregame state |
| Window | SNAPSHOT |
| Source IDs | A; B1 |
| Availability rule | Announcement/observation available by T and applicable to target game; late changes make new snapshots. |
| Missing-data rule | Unknown/conflict remains explicit. Restrict dependent projections or use documented scenarios. |
| Validation | Identity and source evidence agree; odds never establish confirmation. |
| Model use | Lineup state, conditional scenarios and opportunity allocation |
| Readiness | SOURCE_MAPPING_REQUIRED |

## Player opportunity

### skater_individual_events

**Individual event counts**

| Attribute | Definition |
|---|---|
| Field ID | skater_individual_events |
| Name | Individual event counts |
| Family | Player opportunity |
| Role | DESCRIPTIVE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Own physical goals, primary assists, secondary assists, SOG, misses and blocked attempts; each count has a distinct event/attribution definition. |
| Data type | object |
| Unit | object |
| Population / exposure | Individual ordinary events |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | DERIVATION_NOT_BUILT |

### skater_toi_seconds

**Skater TOI**

| Attribute | Definition |
|---|---|
| Field ID | skater_toi_seconds |
| Name | Skater TOI |
| Family | Player opportunity |
| Role | DESCRIPTIVE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Union of verified shift intervals in selected phase/state; no double-counted overlap. |
| Data type | float&#124;null |
| Unit | seconds |
| Population / exposure | Skater playing intervals |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | DERIVATION_NOT_BUILT |

### skater_sog_per60

**Individual SOG rate**

| Attribute | Definition |
|---|---|
| Field ID | skater_sog_per60 |
| Name | Individual SOG rate |
| Family | Player opportunity |
| Role | DESCRIPTIVE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * skater_individual_SOG / matching skater_toi_seconds. |
| Data type | float&#124;null |
| Unit | shots per 60 |
| Population / exposure | Individual ordinary SOG |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | DERIVATION_NOT_BUILT |

### skater_attempts_per60

**Individual attempt rate**

| Attribute | Definition |
|---|---|
| Field ID | skater_attempts_per60 |
| Name | Individual attempt rate |
| Family | Player opportunity |
| Role | DESCRIPTIVE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * (SOG+misses+blocked attempts) / matching skater_toi_seconds. |
| Data type | float&#124;null |
| Unit | attempts per 60 |
| Population / exposure | Individual ordinary attempts |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | DERIVATION_NOT_BUILT |

### skater_xg_ua_per60

**TDL individual xG rate**

| Attribute | Definition |
|---|---|
| Field ID | skater_xg_ua_per60 |
| Name | TDL individual xG rate |
| Family | Player opportunity |
| Role | INTERNAL_ESTIMATE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * SUM(internal neutral UA xG from own shots) / matching skater_toi_seconds. |
| Data type | float&#124;null |
| Unit | expected goals per 60 |
| Population / exposure | Individual unblocked attempts |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Incomplete required xG coverage -> full-population model value null unless a validated missingness estimator applies. Partial sums are separate diagnostics with their own scored population. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | MODEL_NOT_BUILT |

### skater_points_per60

**Individual point rate**

| Attribute | Definition |
|---|---|
| Field ID | skater_points_per60 |
| Name | Individual point rate |
| Family | Player opportunity |
| Role | DESCRIPTIVE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | 3600 * (eligible goals+primary assists+secondary assists) / matching skater_toi_seconds. |
| Data type | float&#124;null |
| Unit | points per 60 |
| Population / exposure | Declared ordinary scoring population |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | DERIVATION_NOT_BUILT |

### skater_onice_xg_rates

**TDL on-ice xG rates**

| Attribute | Definition |
|---|---|
| Field ID | skater_onice_xg_rates |
| Name | TDL on-ice xG rates |
| Family | Player opportunity |
| Role | INTERNAL_ESTIMATE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | xgf_per60=3600*onice_xGF/participant_seconds; xga_per60=3600*onice_xGA/participant_seconds. Own/opposing neutral UA xG and exposure share exact state/window. |
| Data type | object |
| Unit | object: expected goals per 60 |
| Population / exposure | Verified on-ice ordinary UA |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Incomplete required xG coverage -> full-population model value null unless a validated missingness estimator applies. Partial sums are separate diagnostics with their own scored population. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | MODEL_NOT_BUILT |

### skater_pp_toi_share

**Player PP ice-time share**

| Attribute | Definition |
|---|---|
| Field ID | skater_pp_toi_share |
| Name | Player PP ice-time share |
| Family | Player opportunity |
| Role | DESCRIPTIVE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Player seconds on ice during team's declared PP-state exposure / team seconds in that same PP state. Team-player shares need not sum to 1. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Exact PP state; verified shifts |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | 0..1 per player with matching exact PP exposure; do not use sum(player minutes) as team clock. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | DERIVATION_NOT_BUILT |

### skater_oz_faceoff_start_share

**Offensive faceoff-start share**

| Attribute | Definition |
|---|---|
| Field ID | skater_oz_faceoff_start_share |
| Name | Offensive faceoff-start share |
| Family | Player opportunity |
| Role | DESCRIPTIVE |
| Grain | Skater at cutoff |
| Priority | SUPPORTING |
| Definition / calculation | OZ shift starts at faceoff / (OZ + DZ faceoff shift starts). Neutral/on-the-fly excluded and retained separately. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Faceoff-start deployment |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | DERIVATION_NOT_BUILT |

### combination_shared_seconds

**Line/pair shared TOI**

| Attribute | Definition |
|---|---|
| Field ID | combination_shared_seconds |
| Name | Line/pair shared TOI |
| Family | Player opportunity |
| Role | DESCRIPTIVE |
| Grain | Line/pair at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Union of clock intervals when all named combination members participate in selected phase/state. |
| Data type | float&#124;null |
| Unit | seconds |
| Population / exposure | Exact named combination |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | DERIVATION_NOT_BUILT |

### skater_projected_toi

**TDL projected ice time**

| Attribute | Definition |
|---|---|
| Field ID | skater_projected_toi |
| Name | TDL projected ice time |
| Family | Player opportunity |
| Role | INTERNAL_ESTIMATE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Internal predictive distribution of playing seconds by phase/state, conditional on lineup and forecast manpower exposure. Display minutes only after explicit conversion. |
| Data type | distribution |
| Unit | seconds distribution |
| Population / exposure | Target game; state-specific |
| Window | TARGET |
| Source IDs | E; S; A; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | MODEL_NOT_BUILT |

### skater_finishing_effect

**TDL finishing effect**

| Attribute | Definition |
|---|---|
| Field ID | skater_finishing_effect |
| Name | TDL finishing effect |
| Family | Player opportunity |
| Role | INTERNAL_ESTIMATE |
| Grain | Skater at cutoff |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Hierarchically estimated scoring effect relative to neutral shot baseline, fitted with identified goalie/teammate context. Model/prior not selected. |
| Data type | float&#124;null |
| Unit | model parameter |
| Population / exposure | Eligible ordinary historical shots |
| Window | S2D; G10; G20; H2S |
| Source IDs | E; S; A; I; B1 |
| Availability rule | Use only historical source/model revisions permitted by forecast cutoff T. |
| Missing-data rule | Null with reason if required input or denominator missing; zero exposure -> null rate. Retain exposure and coverage. |
| Validation | Individual and on-ice events kept separate; assignment/exposure scope reconciled. |
| Model use | Player/lineup opportunities and props; on-ice measures are not automatically individual causal effects |
| Readiness | MODEL_NOT_BUILT |

## Rest travel and tracking

### team_recovery_hours

**Team recovery interval**

| Attribute | Definition |
|---|---|
| Field ID | team_recovery_hours |
| Name | Team recovery interval |
| Family | Rest travel and tracking |
| Role | MODEL_FEATURE |
| Grain | Team / target game |
| Priority | CORE_CANDIDATE |
| Definition / calculation | (target scheduled start - prior observed actual game end)/3600. Future target actual start/end cannot enter pregame. |
| Data type | float&#124;null |
| Unit | hours |
| Population / exposure | Known schedule/history |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Only evidence or schedule versions available by cutoff T. |
| Missing-data rule | Null plus missing reason; no invented substitute. Use only a predeclared validated fallback. |
| Validation | Nonnegative; end timestamp and basis observed; start-to-start must not be mislabeled. |
| Model use | Independent context feature candidate |
| Readiness | DERIVATION_NOT_BUILT |

### goalie_recovery_hours

**Goalie recovery interval**

| Attribute | Definition |
|---|---|
| Field ID | goalie_recovery_hours |
| Name | Goalie recovery interval |
| Family | Rest travel and tracking |
| Role | MODEL_FEATURE |
| Grain | Goalie / target game |
| Priority | CORE_CANDIDATE |
| Definition / calculation | (target scheduled start - end of goalie's last observed playing interval)/3600. If only game end exists, use separately labeled game-end proxy. |
| Data type | float&#124;null |
| Unit | hours |
| Population / exposure | Known schedule/history |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Only evidence or schedule versions available by cutoff T. |
| Missing-data rule | Null plus missing reason; no invented substitute. Use only a predeclared validated fallback. |
| Validation | Nonnegative; end timestamp and basis observed; start-to-start must not be mislabeled. |
| Model use | Independent context feature candidate |
| Readiness | DERIVATION_NOT_BUILT |

### start_to_start_hours

**Start-to-start interval**

| Attribute | Definition |
|---|---|
| Field ID | start_to_start_hours |
| Name | Start-to-start interval |
| Family | Rest travel and tracking |
| Role | MODEL_FEATURE |
| Grain | Team or goalie / target game |
| Priority | CORE_CANDIDATE |
| Definition / calculation | (target scheduled start - previous recorded game start)/3600. Retain rest_basis; this is not actual recovery duration. |
| Data type | float&#124;null |
| Unit | hours |
| Population / exposure | Known schedule/history |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Only evidence or schedule versions available by cutoff T. |
| Missing-data rule | Null plus missing reason; no invented substitute. Use only a predeclared validated fallback. |
| Validation | Versioned schedule/timezone or measurement definition, no market inputs. |
| Model use | Independent context feature candidate |
| Readiness | DERIVATION_NOT_BUILT |

### back_to_back_schedule_flag

**Back-to-back schedule flag**

| Attribute | Definition |
|---|---|
| Field ID | back_to_back_schedule_flag |
| Name | Back-to-back schedule flag |
| Family | Rest travel and tracking |
| Role | MODEL_FEATURE |
| Grain | Team / target game |
| Priority | CORE_CANDIDATE |
| Definition / calculation | True if prior played game schedule date and target game schedule date are consecutive under the source's declared schedule-date convention. |
| Data type | boolean&#124;null |
| Unit | boolean |
| Population / exposure | Known schedule/history |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Only evidence or schedule versions available by cutoff T. |
| Missing-data rule | Null plus missing reason; no invented substitute. Use only a predeclared validated fallback. |
| Validation | Versioned schedule/timezone or measurement definition, no market inputs. |
| Model use | Independent context feature candidate |
| Readiness | DERIVATION_NOT_BUILT |

### historical_schedule_load

**Recent team workload**

| Attribute | Definition |
|---|---|
| Field ID | historical_schedule_load |
| Name | Recent team workload |
| Family | Rest travel and tracking |
| Role | MODEL_FEATURE |
| Grain | Team / target game |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Count of completed games and played seconds in trailing D7/D14; upcoming games excluded from historical counts. |
| Data type | object |
| Unit | object |
| Population / exposure | Known schedule/history |
| Window | D7; D14 |
| Source IDs | V; E; B1 |
| Availability rule | Only evidence or schedule versions available by cutoff T. |
| Missing-data rule | Null plus missing reason; no invented substitute. Use only a predeclared validated fallback. |
| Validation | Versioned schedule/timezone or measurement definition, no market inputs. |
| Model use | Independent context feature candidate |
| Readiness | DERIVATION_NOT_BUILT |

### venue_distance_proxy_km

**Venue-distance proxy**

| Attribute | Definition |
|---|---|
| Field ID | venue_distance_proxy_km |
| Name | Venue-distance proxy |
| Family | Rest travel and tracking |
| Role | MODEL_FEATURE |
| Grain | Team / target game |
| Priority | SUPPORTING |
| Definition / calculation | Great-circle distance from prior game venue to target venue using verified coordinates. Describes schedule-implied displacement, not actual travel route. |
| Data type | float&#124;null |
| Unit | km |
| Population / exposure | Known schedule/history |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Only evidence or schedule versions available by cutoff T. |
| Missing-data rule | Null plus missing reason; no invented substitute. Use only a predeclared validated fallback. |
| Validation | 0..~20040 km; same venue can be known 0. No inference of home returns or flights. |
| Model use | Independent context feature candidate |
| Readiness | DERIVATION_NOT_BUILT |

### timezone_shift_hours

**Time-zone offset shift**

| Attribute | Definition |
|---|---|
| Field ID | timezone_shift_hours |
| Name | Time-zone offset shift |
| Family | Rest travel and tracking |
| Role | MODEL_FEATURE |
| Grain | Team / target game |
| Priority | SUPPORTING |
| Definition / calculation | UTC offset at destination for target start minus UTC offset at origin for prior game timestamp; date-specific offsets include DST. |
| Data type | float&#124;null |
| Unit | hours signed |
| Population / exposure | Known schedule/history |
| Window | SNAPSHOT |
| Source IDs | V; E; B1 |
| Availability rule | Only evidence or schedule versions available by cutoff T. |
| Missing-data rule | Null plus missing reason; no invented substitute. Use only a predeclared validated fallback. |
| Validation | Versioned schedule/timezone or measurement definition, no market inputs. |
| Model use | Independent context feature candidate |
| Readiness | DERIVATION_NOT_BUILT |

### tracking_measurement

**Optional tracking measure**

| Attribute | Definition |
|---|---|
| Field ID | tracking_measurement |
| Name | Optional tracking measure |
| Family | Rest travel and tracking |
| Role | MODEL_FEATURE |
| Grain | Player or team / source window |
| Priority | LATER |
| Definition / calculation | Specific observed speed/distance/shot-location/zone-time metric, with source unit, definition and aggregation; projected scoring rates excluded. |
| Data type | float&#124;null |
| Unit | declared per metric |
| Population / exposure | Verified tracking population |
| Window | Source-defined, cutoff-safe |
| Source IDs | T; D4; B1 |
| Availability rule | Only evidence or schedule versions available by cutoff T. |
| Missing-data rule | Null plus missing reason; no invented substitute. Use only a predeclared validated fallback. |
| Validation | Versioned schedule/timezone or measurement definition, no market inputs. |
| Model use | Independent context feature candidate |
| Readiness | OPTIONAL_FEED_UNVERIFIED |

## Internal model components

### shot_p_sog_given_ua

**TDL on-target probability**

| Attribute | Definition |
|---|---|
| Field ID | shot_p_sog_given_ua |
| Name | TDL on-target probability |
| Family | Internal model components |
| Role | INTERNAL_ESTIMATE |
| Grain | Historical shot or simulated future shot |
| Priority | CORE_CANDIDATE |
| Definition / calculation | q=P(SOG &#124; unblocked attempt, pre-outcome shot context). Fit on UA sample with on-target training label; no outcome covariates. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Declared ordinary shot/state universe |
| Window | Model training cutoff; TARGET |
| Source IDs | E; S; I; B1; B2 |
| Availability rule | Model, transforms and calibration fitted only on allowed earlier training data; future marks sampled by opportunity model. |
| Missing-data rule | No fitted/eligible internal model -> UNSUPPORTED for dependent xG component. Do not import external probabilities. |
| Validation | 0..1, no actual shot result or future information as covariates. |
| Model use | Independent context feature candidate |
| Readiness | MODEL_NOT_BUILT |

### shot_p_goal_given_sog

**TDL goal probability given SOG**

| Attribute | Definition |
|---|---|
| Field ID | shot_p_goal_given_sog |
| Name | TDL goal probability given SOG |
| Family | Internal model components |
| Role | INTERNAL_ESTIMATE |
| Grain | Any historical UA context or simulated UA; fitted on SOG only |
| Priority | CORE_CANDIDATE |
| Definition / calculation | r=P(goal &#124; SOG, pre-outcome context, reference shooter/goalie), fitted on SOG and evaluated on all eligible UA contexts. Predictors must be available for misses too. |
| Data type | float&#124;null |
| Unit | fraction |
| Population / exposure | Declared ordinary shot/state universe |
| Window | Model training cutoff; TARGET |
| Source IDs | E; S; I; B1; B2 |
| Availability rule | Model, transforms and calibration fitted only on allowed earlier training data; future marks sampled by opportunity model. |
| Missing-data rule | No fitted/eligible internal model -> UNSUPPORTED for dependent xG component. Do not import external probabilities. |
| Validation | 0..1; q and r use covariates defined before outcome on every UA. SOG-only placement/trajectory needs a separate integrated model. |
| Model use | Independent context feature candidate |
| Readiness | MODEL_NOT_BUILT |

### shot_xg_ua_neutral

**TDL neutral xG per unblocked attempt**

| Attribute | Definition |
|---|---|
| Field ID | shot_xg_ua_neutral |
| Name | TDL neutral xG per unblocked attempt |
| Family | Internal model components |
| Role | INTERNAL_ESTIMATE |
| Grain | Historical UA or simulated future UA |
| Priority | CORE_CANDIDATE |
| Definition / calculation | q*r for eligible unblocked attempt context, including historical misses in the UA aggregate; bounded by q. Future shot contexts are simulated, never observed pregame. |
| Data type | float&#124;null |
| Unit | expected goals per attempt |
| Population / exposure | Declared ordinary shot/state universe |
| Window | Model training cutoff; TARGET |
| Source IDs | E; S; I; B1; B2 |
| Availability rule | Model, transforms and calibration fitted only on allowed earlier training data; future marks sampled by opportunity model. |
| Missing-data rule | No fitted/eligible internal model -> UNSUPPORTED for dependent xG component. Do not import external probabilities. |
| Validation | 0<=q*r<=q<=1; r in 0..1; neutral baseline version identified. |
| Model use | Independent context feature candidate |
| Readiness | MODEL_NOT_BUILT |

### team_attempt_distribution

**TDL attempt/opportunity distribution**

| Attribute | Definition |
|---|---|
| Field ID | team_attempt_distribution |
| Name | TDL attempt/opportunity distribution |
| Family | Internal model components |
| Role | INTERNAL_ESTIMATE |
| Grain | Team / target game |
| Priority | CORE_CANDIDATE |
| Definition / calculation | Default UA opportunity/shot-context distribution by state. An all-attempt variant must first generate blocked vs unblocked outcomes before applying the UA on-target model. |
| Data type | distribution |
| Unit | distribution |
| Population / exposure | Default ordinary UA; all-attempt variant needs explicit unblock stage |
| Window | Model training cutoff; TARGET |
| Source IDs | E; S; I; B1; B2 |
| Availability rule | Model, transforms and calibration fitted only on allowed earlier training data; future marks sampled by opportunity model. |
| Missing-data rule | No fitted/eligible internal model -> UNSUPPORTED for dependent xG component. Do not import external probabilities. |
| Validation | Joint distribution and event universe documented; player totals and state exposure reconcile. |
| Model use | Independent context feature candidate |
| Readiness | MODEL_NOT_BUILT |

## Independent forecast outputs

### regulation_outcome_probabilities

**Regulation probabilities**

| Attribute | Definition |
|---|---|
| Field ID | regulation_outcome_probabilities |
| Name | Regulation probabilities |
| Family | Independent forecast outputs |
| Role | FORECAST_OUTPUT |
| Grain | Target game / independent sporting target / snapshot |
| Priority | OUTPUT_ONLY |
| Definition / calculation | P(home regulation win), P(tie), P(away regulation win) from calibrated internal distribution. |
| Data type | object |
| Unit | object |
| Population / exposure | Exact independent_target_ref fixed before freeze; provider market mapping is downstream |
| Window | TARGET |
| Source IDs | I; B1; B2 |
| Availability rule | Independent target and rules fixed before computation; seal outputs from cutoff-eligible non-market data with assumptions/scenarios and internal model lineage. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | Each in 0..1; home+tie+away=1. |
| Model use | Independent output or upstream distribution for permitted downstream TDL models |
| Readiness | MODEL_NOT_BUILT |

### completed_game_win_probability

**Completed-game win probability**

| Attribute | Definition |
|---|---|
| Field ID | completed_game_win_probability |
| Name | Completed-game win probability |
| Family | Independent forecast outputs |
| Role | FORECAST_OUTPUT |
| Grain | Target game / independent sporting target / snapshot |
| Priority | OUTPUT_ONLY |
| Definition / calculation | Regulation win probability + tie probability * conditional OT/SO win probability under rules version. |
| Data type | fraction |
| Unit | fraction |
| Population / exposure | Exact independent_target_ref fixed before freeze; provider market mapping is downstream |
| Window | TARGET |
| Source IDs | I; B1; B2 |
| Availability rule | Independent target and rules fixed before computation; seal outputs from cutoff-eligible non-market data with assumptions/scenarios and internal model lineage. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | Probabilities/distributions/interval method and scope documented; outputs cannot become inputs to their own prediction. |
| Model use | Independent output or upstream distribution for permitted downstream TDL models |
| Readiness | MODEL_NOT_BUILT |

### score_distribution

**Score distribution**

| Attribute | Definition |
|---|---|
| Field ID | score_distribution |
| Name | Score distribution |
| Family | Independent forecast outputs |
| Role | FORECAST_OUTPUT |
| Grain | Target game / independent sporting target / snapshot |
| Priority | OUTPUT_ONLY |
| Definition / calculation | Joint distribution of home/away scores under explicit phase, empty-net, OT and SO accounting. |
| Data type | distribution |
| Unit | distribution |
| Population / exposure | Exact independent_target_ref fixed before freeze; provider market mapping is downstream |
| Window | TARGET |
| Source IDs | I; B1; B2 |
| Availability rule | Independent target and rules fixed before computation; seal outputs from cutoff-eligible non-market data with assumptions/scenarios and internal model lineage. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | Probabilities/distributions/interval method and scope documented; outputs cannot become inputs to their own prediction. |
| Model use | Independent output or upstream distribution for permitted downstream TDL models |
| Readiness | MODEL_NOT_BUILT |

### player_outcome_distribution

**Player/goalie outcome distributions**

| Attribute | Definition |
|---|---|
| Field ID | player_outcome_distribution |
| Name | Player/goalie outcome distributions |
| Family | Independent forecast outputs |
| Role | FORECAST_OUTPUT |
| Grain | Target game / independent sporting target / snapshot |
| Priority | OUTPUT_ONLY |
| Definition / calculation | Joint/coherent SOG, goals, assists, points and saves distributions conditional on role, goalie, state exposure and target contract. |
| Data type | distribution |
| Unit | distribution |
| Population / exposure | Exact independent_target_ref fixed before freeze; provider market mapping is downstream |
| Window | TARGET |
| Source IDs | I; B1; B2 |
| Availability rule | Independent target and rules fixed before computation; seal outputs from cutoff-eligible non-market data with assumptions/scenarios and internal model lineage. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | Probabilities/distributions/interval method and scope documented; outputs cannot become inputs to their own prediction. |
| Model use | Independent output or upstream distribution for permitted downstream TDL models |
| Readiness | MODEL_NOT_BUILT |

### probability_uncertainty

**Probability-estimate uncertainty**

| Attribute | Definition |
|---|---|
| Field ID | probability_uncertainty |
| Name | Probability-estimate uncertainty |
| Family | Independent forecast outputs |
| Role | FORECAST_OUTPUT |
| Grain | Target game / independent sporting target / snapshot |
| Priority | OUTPUT_ONLY |
| Definition / calculation | Interval or scenario range for estimated probability, with method and nominal coverage where applicable. Scenario ranges carry no coverage claim; distinguish score variability. |
| Data type | object |
| Unit | object |
| Population / exposure | Exact independent_target_ref fixed before freeze; provider market mapping is downstream |
| Window | TARGET |
| Source IDs | I; B1; B2 |
| Availability rule | Independent target and rules fixed before computation; seal outputs from cutoff-eligible non-market data with assumptions/scenarios and internal model lineage. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | Probabilities/distributions/interval method and scope documented; outputs cannot become inputs to their own prediction. |
| Model use | Independent output or upstream distribution for permitted downstream TDL models |
| Readiness | MODEL_NOT_BUILT |

### internal_model_disagreement

**Internal-model disagreement**

| Attribute | Definition |
|---|---|
| Field ID | internal_model_disagreement |
| Name | Internal-model disagreement |
| Family | Independent forecast outputs |
| Role | FORECAST_OUTPUT |
| Grain | Target game / independent sporting target / snapshot |
| Priority | OUTPUT_ONLY |
| Definition / calculation | Declared dispersion among TDL component probabilities on the same target; diagnostic only, not a calibrated confidence interval. |
| Data type | object |
| Unit | object |
| Population / exposure | Exact independent_target_ref fixed before freeze; provider market mapping is downstream |
| Window | TARGET |
| Source IDs | I; B1; B2 |
| Availability rule | Independent target and rules fixed before computation; seal outputs from cutoff-eligible non-market data with assumptions/scenarios and internal model lineage. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | Probabilities/distributions/interval method and scope documented; outputs cannot become inputs to their own prediction. |
| Model use | Independent output or upstream distribution for permitted downstream TDL models |
| Readiness | MODEL_NOT_BUILT |

### independent_snapshot_frozen_at

**Independent freeze time**

| Attribute | Definition |
|---|---|
| Field ID | independent_snapshot_frozen_at |
| Name | Independent freeze time |
| Family | Independent forecast outputs |
| Role | CONTROL |
| Grain | Target game / independent sporting target / snapshot |
| Priority | OUTPUT_ONLY |
| Definition / calculation | Timestamp when independent evidence, probabilities, versions and assumptions were sealed before price join. |
| Data type | timestamp |
| Unit | timestamp |
| Population / exposure | Exact independent_target_ref fixed before freeze; provider market mapping is downstream |
| Window | TARGET |
| Source IDs | I; B1; B2 |
| Availability rule | Independent target and rules fixed before computation; seal outputs from cutoff-eligible non-market data with assumptions/scenarios and internal model lineage. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | Freeze after independent computation and before market join; timestamp immutable and linked to snapshot. |
| Model use | Freeze ordering, provenance and market-join eligibility; never an ordinary model covariate |
| Readiness | DERIVATION_NOT_BUILT |

## Market and gate outputs

### market_contract

**Provider market and settlement mapping**

| Attribute | Definition |
|---|---|
| Field ID | market_contract |
| Name | Provider market and settlement mapping |
| Family | Market and gate outputs |
| Role | MARKET_ONLY |
| Grain | Target game / contract / snapshot |
| Priority | POST_FREEZE |
| Definition / calculation | Post-freeze mapping from a provider market/selection to the immutable independent_target_ref and frozen distribution: phase, threshold, OT/SO inclusion, participation, push/void and fee rules with settlement version. Only supported deterministic projections of the frozen distribution are allowed; provider terms do not refit or redefine the independent model. |
| Data type | object |
| Unit | object |
| Population / exposure | Exact target/settlement contract |
| Window | TARGET |
| Source IDs | M; I; B1; B2 |
| Availability rule | Join only after independent snapshot is frozen; quote must match decision timestamp. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | Provider statistic, phase, event identity and rules match independent_target_ref and supported frozen output. No market column enters independent features. Unmatched contracts remain UNSUPPORTED; settlement and quote semantics reconcile. |
| Model use | Downstream comparison, price timing, gate and audit |
| Readiness | POST_FREEZE_ONLY |

### market_quote

**Market quote snapshot**

| Attribute | Definition |
|---|---|
| Field ID | market_quote |
| Name | Market quote snapshot |
| Family | Market and gate outputs |
| Role | MARKET_ONLY |
| Grain | Target game / contract / snapshot |
| Priority | POST_FREEZE |
| Definition / calculation | Observed price/payout, both sides if relevant, timestamp, liquidity/size context where available and fees; linked only after freeze. |
| Data type | object |
| Unit | object |
| Population / exposure | Exact target/settlement contract |
| Window | TARGET |
| Source IDs | M; I; B1; B2 |
| Availability rule | Join only after independent snapshot is frozen; quote must match decision timestamp. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | No market column allowed in independent model feature matrix. Settlement and quote semantics reconcile. |
| Model use | Downstream comparison, price timing, gate and audit |
| Readiness | POST_FREEZE_ONLY |

### market_probability_no_vig

**Market probability comparison**

| Attribute | Definition |
|---|---|
| Field ID | market_probability_no_vig |
| Name | Market probability comparison |
| Family | Market and gate outputs |
| Role | MARKET_ONLY |
| Grain | Target game / contract / snapshot |
| Priority | POST_FREEZE |
| Definition / calculation | Raw implied probability and separately normalized no-vig estimate when matching exhaustive outcomes and methodology permit. |
| Data type | object |
| Unit | object |
| Population / exposure | Exact target/settlement contract |
| Window | TARGET |
| Source IDs | M; I; B1; B2 |
| Availability rule | Join only after independent snapshot is frozen; quote must match decision timestamp. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | No market column allowed in independent model feature matrix. Settlement and quote semantics reconcile. |
| Model use | Downstream comparison, price timing, gate and audit |
| Readiness | POST_FREEZE_ONLY |

### edge_ev_price_threshold

**Edge EV and price requirements**

| Attribute | Definition |
|---|---|
| Field ID | edge_ev_price_threshold |
| Name | Edge EV and price requirements |
| Family | Market and gate outputs |
| Role | MARKET_ONLY |
| Grain | Target game / contract / snapshot |
| Priority | POST_FREEZE |
| Definition / calculation | Edge and EV from frozen independent probability and current matched contract/quote. For returned-stake push with p_win>0: fair d=(1-p_push)/p_win, EV=p_win*(d-1)-p_loss before explicit expected fees. p_win=0 has no finite fair win price; all-push means no action. |
| Data type | object |
| Unit | object |
| Population / exposure | Exact target/settlement contract |
| Window | TARGET |
| Source IDs | M; I; B1; B2 |
| Availability rule | Join only after independent snapshot is frozen; quote must match decision timestamp. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | No market column allowed in independent model feature matrix. Settlement and quote semantics reconcile. |
| Model use | Downstream comparison, price timing, gate and audit |
| Readiness | POST_FREEZE_ONLY |

### recommendation_gate_state

**Recommendation Gate result**

| Attribute | Definition |
|---|---|
| Field ID | recommendation_gate_state |
| Name | Recommendation Gate result |
| Family | Market and gate outputs |
| Role | MARKET_ONLY |
| Grain | Target game / contract / snapshot |
| Priority | POST_FREEZE |
| Definition / calculation | Sport-authoritative BET/LEAN/WATCH/PASS/AVOID plus reason/version; unsupported capability is a separate support status. |
| Data type | object |
| Unit | object |
| Population / exposure | Exact target/settlement contract |
| Window | TARGET |
| Source IDs | M; I; B1; B2 |
| Availability rule | Join only after independent snapshot is frozen; quote must match decision timestamp. |
| Missing-data rule | Unsupported target/model/contract is explicit; do not invent a probability, quote or gate. |
| Validation | No market column allowed in independent model feature matrix. Settlement and quote semantics reconcile. |
| Model use | Downstream comparison, price timing, gate and audit |
| Readiness | POST_FREEZE_ONLY |

## Decision register

| ID | Decision | Status | Detail |
|---|---|---|---|
| D01 | Statistical scope | PROPOSED DEFAULT | Separate regulation, overtime, shootout, penalty shots and awarded/scoring exceptions. |
| D02 | Primary shot universe | PROPOSED DEFAULT | Use ordinary unblocked attempts for neutral team xG; retain all attempts for volume/blocking. |
| D03 | Goalie xG convention | PROPOSED DEFAULT | Use explicitly named conditional-on-SOG xGA, expected SV and GSAx for goalie comparison. |
| D04 | Strength/exposure definition | PROPOSED DEFAULT | Orthogonal state fields, mutually exclusive intervals, both goalies present for REG5V5; matching seconds. |
| D05 | PP opportunities | PROPOSED DEFAULT | Use official opportunity counts as their own evidence. PP-state time remains a separate measure. |
| D06 | Availability clock | PROPOSED DEFAULT | Conservative first-observed/source publication availability; no backdated historical certainty without certified archive evidence. |
| D07 | Null and fallback rules | PROPOSED DEFAULT | Missing/zero-exposure stays null with reason; branch-local support and only validated predeclared fallbacks. |
| D08 | Goalie/lineup uncertainty | PROPOSED DEFAULT | Sourced status and named conditional forecasts; mixture only with justified internal weights. |
| D09 | Rolling windows / priors | CANDIDATES; TUNING PENDING | S2D, G5/G10/G20, H2S and D7/D14 are explicitly defined candidates. No chosen blend, half-life or minimum samples. |
| D10 | High-danger definition | UNDECIDED; INACTIVE | Choose/version geometric region or neutral-xG threshold only after source support and training-only research. |
| D11 | Rush / rebound / flurry definition | UNDECIDED; INACTIVE | Define observed vs proxy sequence labels, thresholds, termination and coverage before activation. |
| D12 | Opponent / score adjustment | MODEL CHOICE PENDING | Train internal adjustment and reference population chronologically; no third-party rating offsets. |
| D13 | Source adapters / coverage | UNVERIFIED | Event, shift, availability, schedule and optional tracking schemas/history/rights/freshness require acquisition verification. |
| D14 | Feature selection / model weights | UNDECIDED | Measure group contribution in chronological folds. Dictionary inclusion does not mean all columns enter each model. |
| D15 | Settlement / certification | PENDING | Specify independent sporting target/counting/rules contracts before freeze and validate downstream provider settlement mappings. Goalie-start support, calibration, PIT replay and manual end-to-end proof precede production. |

## Synthetic arithmetic examples

All numbers illustrate definitions; no actual team, fitted model, model performance or selected hyperparameter is represented.

| Example | Inputs | Derived result |
|---|---|---|
| Team attempts and xG | 48 minutes; SF 30, SA 24; misses 12/11; blocked attempts 8/15; UA xGF 2.4, xGA 1.8 | CF 50/50, CF share 50%; FF 42/35, FF share 54.545%; SF share 55.556%; xGF share 57.143%; xGF/60=3.00, xGA/60=2.25 |
| Goalie SOG baseline | Separate 60-minute sample: UA 45, SOG 30, GA 2; UA xGA 3.4; conditional SOG xGA 2.8 | SV=93.333%; xSV=90.667%; GSAx_SOG=+0.8; SV minus xSV=2.667 percentage points. Use 2.8, not UA xGA 3.4, in these goalie calculations. |
| Exposure pooling | 10 shots in 10 minutes, then 30 shots in 50 minutes | 40 shots in 60 minutes => 40 per 60; not the unweighted mean 48 of rates 60 and 36. |
| Zero vs missing | Known 0 count with 48 complete minutes; separate zero-exposure or missing-count case | First rate is 0. Zero exposure or unknown count yields null with a reason. |

## Source register

Reference review is distinct from acquisition validation. Empty source URLs or null verification dates are deliberate; no connection, provider endpoint, historical archive, license, freshness SLA or trained model is certified by this table.

| ID | Source / class | Reviewed | Verification status | Scope |
|---|---|---|---|---|
| B1 | [Daily NHL Build Boundary V1](https://github.com/OneVillage83/The-Daily-Line-Automation/blob/3dca321352194f636c8cf50cde1a927a4c74aabe/docs/GrokBot%20OpenAI%20Bridge/sport-build-boundaries/DAILY_NHL_BUILD_BOUNDARY_V1.md) | 2026-10-10 | ORIGINAL_REPOSITORY_DOCUMENT_READ | Canonical NHL feature families, internally computed xG, goalie/line/manpower semantics, modeling/market/live boundaries. Current document read; implementation not certified. URL pins the original planning evidence; see current_companion_path for the current companion document. |
| B2 | [Shared Sport Build Constitution V1](https://github.com/OneVillage83/The-Daily-Line-Automation/blob/3dca321352194f636c8cf50cde1a927a4c74aabe/docs/GrokBot%20OpenAI%20Bridge/sport-build-boundaries/SHARED_SPORT_BUILD_CONSTITUTION_V1.md) | 2026-10-10 | ORIGINAL_REPOSITORY_DOCUMENT_READ | Point-in-time evidence, model/market firewall, chronological evaluation, calibration, immutable snapshots and ownership. URL pins the original planning evidence; see current_companion_path for the current companion document. |
| D1 | [Evolving Hockey standard skater glossary](https://evolving-hockey.com/glossary/standard-skater-tables/) | 2026-10-10 | REFERENCE_DESCRIPTION_REVIEWED | Reference for conventional attempt/share terminology only. Formula conventions in this proposal are explicit; do not import ratings or blindly copy all glossary formulas. |
| D2 | [MoneyPuck glossary](https://www.moneypuck.com/glossary.htm) | 2026-10-10 | REFERENCE_DESCRIPTION_REVIEWED | Reference for xG/GSAx terminology. Its numeric model outputs and provider-specific danger thresholds are not TDL inputs. |
| D3 | [Official NHL hockey glossary](https://www.nhl.com/info/hockey-glossary) | 2026-10-10 | REFERENCE_DESCRIPTION_REVIEWED | Official terminology for goals, shots, saves and special teams. Source definitions must be reconciled to the event population. |
| D4 | [NHL EDGE current public description](https://www.nhl.com/nhl-edge/nhl-edge-whats-new) | 2026-10-10 | REFERENCE_DESCRIPTION_REVIEWED | Public curated tracking displays and daily update description. No production ingestion or live feed is claimed. |
| E | [Required event and box-score evidence](https://www.nhl.com/) | 2026-10-10 | ACQUISITION_UNVERIFIED | Proposed source class: official or authorized factual PBP/events/box scores. Exact endpoint, schema, rights, history, revisions and freshness remain to be verified. |
| S | Required shift and participation evidence | 2026-10-10 | ACQUISITION_UNVERIFIED | Proposed source class: factual shift intervals and on-ice participants. Availability and reconciliation are unverified. |
| A | Required availability and lineup evidence | 2026-10-10 | ACQUISITION_UNVERIFIED | Proposed source class: timestamped official team/league reports and attributable direct reporting. Confirmation remains separate from projection. |
| V | [Required schedule and venue evidence](https://www.nhl.com/schedule) | 2026-10-10 | ACQUISITION_UNVERIFIED | Proposed source class: schedules, venue identity/time zone, revisions and actual game times. Route distance is only a venue-to-venue proxy. |
| T | Optional measured tracking / documented video tags | 2026-10-10 | ACQUISITION_UNVERIFIED | Candidate source class only. Coverage, timing, calibration and access must be verified before use; no invented screens, pressure or entries. |
| I | TDL internal model and feature artifacts | 2026-10-10 | INTERNAL_ARTIFACTS_NOT_BUILT | Proposed artifacts trained and versioned internally under B1/B2. No NHL model has been implemented or validated. |
| M | DDC market evidence after independent freeze | 2026-10-10 | ACQUISITION_UNVERIFIED | Proposed source class for timestamped contract/quote/fee data. Forbidden as independent-model input. |
