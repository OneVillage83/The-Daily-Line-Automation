# Shared Sport Build Constitution V1

**Status:** PROGRAM-LEVEL BUILD GUARDRAIL  
**Established:** 2026-09-23

This document defines common boundaries every `Daily-*` sport pipeline must preserve. It does not supersede repository-local certified architecture.

## 1. Authority precedence

Use this order:

1. explicit current owner instruction
2. target repo `AGENTS.md` / local constitution
3. target repo exact resume/status/certification/architecture documents
4. immutable Git/PR/CI evidence
5. this sport-boundary pack
6. DLADS roadmap/program state
7. old chat summaries or memory

If this pack conflicts with certified local sport architecture, the local repository wins and the conflict must be recorded.

## 2. Repository ownership map

### Daily-Data-Core
Owns shared provider acquisition, immutable raw evidence/provenance, generic odds/exchange/prediction-market observations, sport-neutral market math, and shared venue/weather/travel/rest facts.

### Daily-Data-Live-Core
Owns shared live acquisition/transport/freshness infrastructure. It does not own sport interpretation or live predictive semantics.

### Daily-Model-Core
Owns reusable **independent/non-market** model lifecycle and research governance through the calibrated fair-view boundary. It does not own sport identity, feature, target, state, or simulation semantics.

### Daily-* sport repository
Owns canonical sport identity/state, features/targets, training/inference, simulations, TDL Unified Line outputs, individual-market fair probabilities, sport-specific market-aware decisions, Line Timing Models where applicable, Recommendation Gate semantics, explanations, same-event joint evidence, and sport settlement.

### Daily-Line-Core
Consumes sealed `SportDecisionPackage` artifacts plus PIT DDC market evidence. It owns All Bets cross-sport assembly, 2-5 leg EdgeStack optimization, cross-sport product ranking/indexing, and immutable `DailyLinePublicationPackage` sealing. It may not reconstruct sport truth or alter sport gates.

### The-Daily-Line-Automation
Owns orchestration/control-plane behavior, scheduling, retries/idempotency, worker execution, publication coordination, and video/social/content operations. It does not own sport intelligence.

### Website/report/infographic
Own presentation, search/archive UX, and rendering only. They consume sealed product truth.

## 3. Independent-prediction market firewall

The sport's independent forecast must be created and frozen **before** sportsbook, exchange, prediction-market, consensus, line-movement, closing-price, third-party picks, third-party power ratings, or third-party predictive probabilities can influence the independent estimate.

Allowed independent inputs are factual/statistical evidence: raw box score/PBP/event/tracking data, Statcast/Next Gen-type measures, injuries, availability, usage, lineups, weather, venue, rest/travel, coaching/tactical context, and other PIT facts.

Required lineage:

- `INDEPENDENT` — non-market sport evidence only
- `MARKET_ONLY` — market evidence only
- `MARKET_AWARE` — starts from frozen independent forecast, then compares with market
- `UNIFIED_LINE` — calibrated independent fair view
- `RECOMMENDATION` — downstream value/risk/gate state

Third-party predictive outputs may be used only for explicitly isolated retrospective benchmarking.

## 4. Point-in-time discipline

Historical replay at time `T` behaves as though `T` is the present.

- Preserve meaningful `effective_at`, `published_at`, `observed_at`, `ingested_at`, and defensible `available_at`.
- Pregame evidence is eligible when legitimately available by cutoff and before event start.
- Late same-day pregame evidence is allowed when PIT-valid.
- Post-start information never enters an earlier pregame snapshot.
- Corrections/revisions create traceable lineage instead of rewriting historical knowledge.
- PIT ambiguity fails closed.

## 5. Predict every supported market before gating

For every supported/modelable market:

1. create fair probability/distribution
2. preserve uncertainty, calibration, model/config/data provenance
3. attach PIT market evidence only after independent freeze
4. calculate sport-authoritative market-aware value/timing fields
5. apply sport Recommendation Gate
6. store, settle, and evaluate the result regardless of `BET`, `LEAN`, `PASS`, or `AVOID`

A gate never erases a forecast. Unsupported markets are explicit.

## 6. Model Zoo and learned ensemble

- Preserve multiple justified model families rather than one universal algorithm.
- Final validation is chronological/walk-forward.
- Stackers/mixtures train only on frozen OOF/forward base predictions.
- Calibration evidence is separated from final holdout evidence.
- Target/context specialists may retain weight even if aggregate ranking is mediocre.
- Disagreement and uncertainty are first-class outputs.
- Promotion is reproducible and versioned.
- W/L or ROI alone is not model-quality proof.

## 7. TDL Unified Line

The TDL Unified Line is the calibrated independent fair view and remains free of sportsbook/exchange/prediction-market prices. Market-aware comparison, EV, timing, and gating occur only after the Unified Line is frozen.

## 8. SportDecisionPackage boundary

Each sport ultimately emits immutable versioned PIT-correct `SportDecisionPackage` artifacts containing supported individual-market decisions, fair probabilities, uncertainty/calibration, gate state, settlement version, explanation refs, provenance, and same-event joint evidence where certified.

Daily-Line-Core consumes the sealed package and may not infer missing sport truth.

## 9. Pregame vs live separation

Live capability is a sibling pipeline, not a mutation of pregame:

- pregame predictions remain immutable
- live transport comes from Daily-Data-Live-Core
- sport repo owns live state/features/models/gates
- live has separate identity/versioning/cutoffs/evaluation
- live may compare with pregame but cannot revise it
- pregame completion must not be delayed just to add live betting

## 10. Common build phases

Existing repos may use different phase names/numbers; local architecture remains authoritative.

- **SB-0 Governance/bootstrap:** constitution, authority map, roadmap, status/resume, change journal
- **SB-1 Identity/rules:** canonical entities, schedule revisions, rule/settlement versions
- **SB-2 Evidence/PIT:** immutable evidence, adapters, availability clocks, reconciliation
- **SB-3 State reconstruction:** deterministic sport-native state snapshots
- **SB-4 Features/context:** sport features, availability, venue/weather/rest/travel, data quality
- **SB-5 Target/market contracts:** taxonomy, thresholds, settlement, support matrix
- **SB-6 Baseline Model Zoo:** reproducible baselines/generic families
- **SB-7 Sport specialists:** target/context-specific specialists
- **SB-8 Simulation/joint engine:** full distributions and same-event dependency evidence
- **SB-9 Calibration/Unified Line:** calibrated independent fair probabilities + uncertainty
- **SB-10 Market-aware layer:** DDC market join only after SB-9 freeze; value/EV/timing
- **SB-11 Recommendation Gate/export:** deterministic gate + sealed SportDecisionPackage
- **SB-12 Settlement/evaluation/learning:** immutable outcomes, calibration, downstream CLV/EV/ROI, miss attribution
- **SB-13 Manual publication proof:** sport -> DLC/report/infographic validated manually
- **SB-14 Live sibling pipeline:** only after pregame authority is stable enough to prevent contamination
- **SB-15 Automation onboarding:** manual -> shadow -> supervised -> explicit TDLA production authority

## 11. Bridge/Codex rules

- one repository per Codex turn
- read shared constitution + exact sport file before sport-expansion work
- for existing repos, read local authority docs before selecting work
- do not rewrite certified architecture for implementation convenience
- do not create cross-repo contracts silently from one repo
- do not opportunistically refactor adjacent phases
- do not create/register a future repo merely because an outline exists
- ownership/science/PIT/settlement/production-authority ambiguity is escalated, not guessed
- every material work unit leaves durable change/resume evidence

## 12. Minimum production-authority evidence

A sport is not production-authoritative without applicable proof for:

- canonical identity and settlement correctness
- PIT leakage protection
- deterministic/reproducible features/targets
- walk-forward/OOS model evaluation
- calibration and uncertainty
- simulation/joint-dependency validation where published
- market reconciliation/freshness
- Recommendation Gate determinism
- supported-market inventory completeness
- immutable prediction ledger
- settlement/evaluation replay
- sealed SportDecisionPackage compatibility
- manual end-to-end publication proof
- automation equivalence/failure/idempotency proof before TDLA production authority

## 13. Exclusions

These outlines do not authorize bankroll sizing, personalized Kelly/stake recommendations, stop-loss/chase logic, wallet/account integration, automatic wager placement, or autonomous wagering.
