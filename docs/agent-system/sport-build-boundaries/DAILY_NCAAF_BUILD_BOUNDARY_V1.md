# Daily NCAAF Build Boundary V1

**Status:** EXISTING REPOSITORY — LOCAL F-LAYER ARCHITECTURE GOVERNS  
**Repository:** `OneVillage83/Daily-NCAAF`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authority

Daily-NCAAF already documents full production architecture and a TDL Unified Ensemble overlay. Preserve that authority. Do not prematurely extract shared NFL/NCAAF code until both implementations prove the semantics are genuinely shared.

## Mission

Model college football with explicit handling of extreme team count, roster turnover, conference/subdivision imbalance, transfers/recruiting uncertainty, and uneven data quality while preserving the same PIT and independent-line discipline as the rest of The Daily Line.

## Canonical sport truth

- institutions/teams, players, rosters, coaches, conferences, subdivisions, games, venues and schedules
- transfer/eligibility, depth/QB roles and coaching changes are time-versioned
- conference membership and postseason/rule context are season-effective
- provider IDs remain crosswalks

## Factual evidence

- PBP, box score, participation/usage and tracking/charting where available
- roster, transfer portal, recruiting/talent, returning production, injuries/availability and depth/QB information
- opponent/conference/subdivision strength context, pace, garbage-time state and schedule strength
- venue, travel, altitude, weather, rest, rivalry, neutral-site and postseason context

## Feature families

- opponent-adjusted efficiency, explosiveness, success, havoc/pressure and finishing drives
- neutral pace and game-state splits
- QB/skill/OL/defense continuity and returning production
- transfers and talent/recruiting priors with uncertainty/decay
- conference/subdivision hierarchical strength
- garbage-time treatment and unequal opponent-quality adjustment
- travel/weather/altitude/neutral-site and data-quality/confidence features

## Target/market universe

- moneyline, spread, total, team totals
- half/quarter markets when explicitly supported
- player props only where reliable player identity, participation, provider coverage, settlement and calibration exist
- scorer/TD markets require participant certainty and explicit opportunity modeling

## Model Zoo direction

- hierarchical team-strength/EPA models with conference/subdivision partial pooling
- Bayesian shrinkage for sparse early-season and high-turnover states
- transfer/talent/returning-production priors that yield to current evidence under validated rules
- nonlinear game models and drive/play simulation
- QB, pace, explosiveness and finishing-drive specialists
- player-usage models only where data supports them
- dynamic learned ensemble from frozen OOS base predictions, with context/data-quality-aware weights

## Full build outline

| Phase | NCAAF requirement |
|---|---|
| SB-0 | Honor existing F-layer architecture/current status; no generic rewrite. |
| SB-1 | Version teams/conferences/rosters/coaches/eligibility/schedules/rules across seasons/subdivisions. |
| SB-2 | Acquire PIT PBP/roster/transfer/recruiting/availability/weather/venue evidence with quality grades. |
| SB-3 | Reconstruct team/QB/depth/availability and event state without importing NFL assumptions blindly. |
| SB-4 | Build opponent-adjusted efficiency, talent/continuity, pace, game-state, travel/weather and quality features. |
| SB-5 | Certify game/player target support and settlement; sparse-data props fail closed. |
| SB-6 | Establish hierarchical power/efficiency baselines and early-season shrinkage benchmarks. |
| SB-7 | Add QB/explosiveness/pace/finishing-drive/talent-continuity specialists with OOS proof. |
| SB-8 | Simulate score/drive/player outcomes and college-specific joint dependencies. |
| SB-9 | Calibrate/freeze independent NCAAF Unified Line with data-quality-aware uncertainty. |
| SB-10 | Join DDC quotes only after freeze; run value/line-timing/risk logic. |
| SB-11 | Apply NCAAF Recommendation Gate and export SportDecisionPackage/support state. |
| SB-12 | Evaluate by conference, season phase, favorite band, total band, data quality and market class. |
| SB-13 | Prove large-slate manual publication/DLC handoff and batch-safe processing. |
| SB-14 | Later live sibling with football state plus variable feed-quality handling. |
| SB-15 | Automate only after manual certification and large-slate recovery/idempotency proof. |

## Simulation / joint evidence

- account for larger team-strength gaps, pace variance and garbage-time behavior
- same-event/player correlations require college-specific evidence, not borrowed NFL coefficients
- propagate sparse-team/player and depth/QB uncertainty through distributions

## Uncertainty

Early season, FCS matchups, new coaches/QBs, transfer-heavy rosters and incomplete player feeds receive wider uncertainty. Data-quality state is an input to model trust and gating.

## Live boundary

Live NCAAF may share football concepts with NFL where semantically valid, but feed reliability, roster identity and variance remain college-specific. Shared code is extracted only after demonstrated equivalence.

## Anti-drift rules

- no wholesale NFL clone
- no forced player-prop support where provider/data quality is insufficient
- no rankings, betting lines, public picks or predictive ratings as independent truth
- no EdgeStack implementation here

## Bridge stop conditions

Stop/escalate if an abstraction assumes NFL=NCAAF without proof, player identity/participation is unreliable, recruiting/transfer/talent inputs lack PIT reconstruction, or market evidence would leak into the independent ensemble.

## Exit criteria

- local NCAAF architecture/manual pipeline certified
- large-slate throughput, sparse-data degradation and PIT replay proven
- supported markets show OOS calibration and settlement evidence
- DLC receives sealed sport decisions without reconstructing college-specific truth
