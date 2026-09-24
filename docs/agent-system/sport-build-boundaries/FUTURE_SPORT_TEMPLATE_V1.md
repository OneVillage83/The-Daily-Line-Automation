# Future Daily-* Sport Build Boundary Template V1

Use this template only after explicit owner direction to add a new sport/league.

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## 1. Identity / authorization

- Product name:
- Proposed repository:
- Sport / league / competition scope:
- Existing repository?:
- Bridge registered?:
- Local authority docs:
- Current certification state:

The outline itself does not authorize repository creation, Bridge access or coding.

## 2. Mission

Define exactly what probability distributions and individual markets the sport pipeline will own.

## 3. Canonical sport truth

Document sport-native entities, rules, schedule/event revisions, roster/participant semantics and settlement-rule versions. Provider IDs remain crosswalks.

## 4. Factual evidence inventory

List raw/PBP/event/tracking/availability/venue/weather/travel/context evidence with:

- source/provider role
- PIT clocks / available-at semantics
- revision/correction behavior
- licensing/usage constraints
- data-quality/degradation states
- immutable raw/provenance expectations

## 5. State reconstruction

Define deterministic pregame state and which late pregame changes produce new immutable snapshots.

## 6. Feature/context architecture

Define sport-owned feature families, versions, leakage tests, uncertainty inputs and data-quality state.

## 7. Market/target support matrix

For every market class document:

- target semantics
- event/participant identity
- side/threshold
- provider settlement variations
- data requirements
- model support
- calibration evidence
- unsupported/degraded behavior

Every supported/modelable market is predicted before gate filtering.

## 8. Model Zoo

Specify:

- simple baselines
- hierarchical/Bayesian families
- nonlinear/tabular families
- sport specialists
- simulation/joint models
- calibration
- learned ensemble/mixture-of-experts

All independent model lineage remains non-market.

## 9. TDL Unified Line

Define calibrated independent fair probabilities/distributions and uncertainty. Freeze before any market evidence enters market-aware logic.

## 10. Market-aware layer

Join Daily-Data-Core point-in-time quotes after the independent freeze. Define:

- implied/no-vig/consensus evidence refs
- edge/EV where defensible
- quote freshness
- timing
- sport-specific risk
- Recommendation Gate inputs

## 11. SportDecisionPackage

Define the sealed sport-to-Daily-Line-Core handoff:

- package identity/version/digest
- prediction/data cutoff
- all supported markets
- fair probabilities/lines
- uncertainty/calibration
- Recommendation Gate state/reasons
- settlement version
- explanation refs
- same-event joint evidence refs
- support/degradation state
- supersession lineage

## 12. Settlement/evaluation/learning

Define immutable result truth, settlement, Brier/log-loss/calibration where appropriate, downstream CLV/EV/ROI, miss attribution, walk-forward champion/challenger and promotion gates.

## 13. Manual publication proof

Prove sport -> sealed SportDecisionPackage -> Daily-Line-Core -> report/infographic/web handoff manually before automation authority.

## 14. Live sibling

Define Daily-Data-Live-Core inputs and sport-owned live state/features/models/gates. Live must have separate identity/versioning and may not mutate pregame predictions.

## 15. Automation

Manual -> shadow -> supervised -> production through TDLA, with failure/retry/idempotency/equivalence evidence.

## 16. Bridge stop conditions

List decisions that require owner/architecture escalation rather than inference.

## 17. Definition of done

List architecture, identity, PIT, data, model, calibration, simulation/joint, settlement, package, manual-publication, live and automation certification gates.
