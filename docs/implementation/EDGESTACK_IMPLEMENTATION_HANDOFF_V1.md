# EdgeStack Implementation Handoff V1

**Date:** 2026-09-17  
**Status:** FUTURE IMPLEMENTATION PLAN — DOES NOT SUPERSEDE A-11  
**Governing architecture:** `docs/architecture/EDGESTACK_PARLAY_OPTIMIZER_V1.md`

## Purpose

This handoff gives GrokBot-OpenAI-Bridge / Codex a bounded implementation sequence for The Daily Line's **EdgeStack Parlay Optimizer** without requiring future agents to reconstruct the product intent from chat history.

Product positioning:

> **The Daily Line EdgeStack Parlay Optimizer**  
> **Stack the Edge. Not the Odds.**

EdgeStack is a 2-5 leg probability-first optimizer built on top of The Daily Line's calibrated individual-bet predictions and Recommendation Gates. The same broader product surface also includes an **All Bets Prediction Scanner** that evaluates and publishes every supported/modelable bet known to the system for the slate.

## Hard scope constraints

V1 must include:

- exhaustive supported-market evaluation;
- per-bet fair probability + market price/probability + edge + Recommendation Gate;
- 2-5 leg candidate generation;
- cross-game and cross-sport combinations;
- same-game combinations only with certified correlation treatment;
- Kalshi Combo/RFQ quote evaluation;
- sportsbook parlay quote evaluation where supported;
- Core / Value / Upside EdgeStack classes;
- report publication;
- website publication contract;
- historical point-in-time evaluation and settlement audit.

V1 must **not** include:

- bankroll management;
- Kelly sizing;
- stake recommendations;
- stop-loss / daily-loss rules;
- chase-prevention logic;
- wallet/account integration;
- automated betting/order placement.

Do not silently add those deferred features while implementing EdgeStack.

## Ownership rule

The-Daily-Line-Automation is **not** allowed to own EdgeStack probability/value logic.

Before production code begins, the bridge must preserve these boundaries:

- DDC -> normalized point-in-time market observations / quote provenance;
- sport repos -> calibrated fair probabilities, sport-specific market semantics, Recommendation Gate, settlement meaning;
- EdgeStack logical component -> cross-sport combination generation, joint probability, quote comparison, ranking/classification;
- website -> presentation/history/search;
- TDLA -> later orchestration/publication coordination only after manual certification.

The physical repository/package home for the EdgeStack Engine itself must be frozen by a dedicated ADR before implementation. Do not place the optimizer inside TDLA merely because this architecture document lives here.

## Bridge execution rule

The GrokBot-OpenAI-Bridge currently executes one repository per Codex turn. EdgeStack is cross-repository work.

Therefore:

- do not silently modify multiple repositories in one development turn;
- route each phase to exactly one authorized repository/workstream;
- stop for architecture/human clarification if a phase requires unresolved cross-repository authority;
- preserve immutable versioned interfaces between repos rather than direct database coupling.

## Proposed implementation sequence

### ES-0 — Ownership ADR + canonical contracts

Goal: freeze where the EdgeStack runtime lives and define its public contracts before business logic.

Deliverables:

- ADR for physical owner/repository/package placement;
- `BetMarketKey` / canonical market identity compatibility decision;
- `BetCandidate` contract;
- `AllBetsSnapshot` contract;
- `EdgeStackLeg` contract;
- `EdgeStackQuote` contract;
- `EdgeStackCandidate` contract;
- `EdgeStackRecommendation` contract;
- `EdgeStackPublicationPackage` contract;
- schema versioning / deterministic identity rules;
- valid/invalid fixtures;
- cross-language schemas if website/runtime require different languages.

Acceptance:

- no sport-specific logic duplicated in shared contracts;
- all fields bind to model/data cutoff and quote provenance;
- unsupported/stale/unpriceable states are explicit;
- bankroll/stake fields are absent from V1 contracts.

### ES-1 — All Bets market-universe scanner

Goal: enumerate every supported/modelable betting market for a slate and join sport fair probabilities with normalized market observations.

Deliverables:

- supported market registry;
- market enumerator;
- quote join/reconciliation;
- fee-aware break-even abstraction where provider data supports it;
- Recommendation Gate adapter;
- `AllBetsSnapshot` builder;
- deterministic sorting/filtering independent of provider UI order.

Acceptance:

- every supported priceable market appears exactly once by canonical identity;
- unsupported markets are explicit rather than guessed;
- no post-start data enters pregame snapshots;
- every row includes probability, market price, edge, gate, reason refs, quote time, and provenance.

### ES-2 — Leg eligibility engine

Goal: create the candidate leg pool from All Bets.

Deliverables:

- eligibility policy schema;
- gate/freshness/calibration checks;
- settlement-definition checks;
- provider executable-quote checks;
- exclusion reason taxonomy.

Acceptance:

- a leg that fails individually never enters a combination;
- every rejection has a deterministic reason code;
- stale quotes fail closed.

### ES-3 — 2-5 leg candidate generator

Goal: enumerate valid combinations reproducibly without combinatorial explosion.

Deliverables:

- deterministic candidate identity;
- 2/3/4/5-leg generation;
- contradiction/dedup detection;
- same-event exposure rules;
- bounded pruning/top-K mechanism;
- cross-game and cross-sport support.

Acceptance:

- no 1-leg or >5-leg EdgeStack in V1;
- no weak leg is injected solely to raise multiplier;
- repeated runs over identical inputs produce identical candidate identities.

### ES-4 — Joint probability / correlation engine

Goal: assign defensible joint probabilities.

Deliverables:

- independence path for unrelated events;
- simulation/joint-sample adapter;
- correlation metadata contract;
- same-game dependency support;
- uncertainty/confidence output;
- fail-closed behavior for unsupported correlation.

Acceptance:

- same-game legs are never multiplied as independent when dependency is material;
- cross-game independence assumptions are visible/auditable;
- published joint probabilities include method/version/provenance.

### ES-5 — Provider Combo/parlay pricing adapters

Goal: compare model joint probability against actual combo/parlay price.

Initial provider priority:

1. Kalshi Combo/RFQ;
2. supported sportsbook parlay quote sources where lawful/available.

Deliverables:

- provider quote identity;
- quote request/response normalization;
- quote timestamp/expiry;
- multiplier / contract-price normalization;
- raw and fee-aware break-even calculations;
- quote-vs-standalone diagnostic fields;
- stale/expired rejection.

Acceptance:

- real Combo quote overrides any diagnostic product of standalone prices;
- RFQ quote provenance is retained;
- expired quotes cannot remain PLAY-qualified.

### ES-6 — EdgeStack optimizer + classes

Goal: rank qualifying combos without hiding the underlying dimensions.

Deliverables:

- `CORE`, `VALUE`, `UPSIDE` classification;
- ranking views: `HIGHEST_HIT_RATE`, `BEST_VALUE`, `BEST_BALANCE`, `BEST_UPSIDE`;
- probability edge;
- gross/net EV where calculable;
- calibration/correlation quality;
- uncertainty width;
- quote freshness;
- configurable minimum gates.

Acceptance:

- ranking does not use payout alone;
- ranking does not use hit probability alone;
- underlying metrics remain visible even if a composite score is added;
- no stake/bankroll recommendation is emitted.

### ES-7 — Daily report publication

Goal: make All Bets + EdgeStack first-class report sections.

Required report sections:

1. **All Bets** — every supported analyzed market with fair probability, market probability/price, edge, Recommendation Gate, reason, quote timestamp, and confidence metadata.
2. **EdgeStack Parlay Optimizer** — Core, Value, Upside, plus optional ranked alternates.

Each EdgeStack display should show:

- legs;
- class;
- joint hit probability;
- quoted multiplier/price;
- break-even probability;
- edge;
- gross/net EV where available;
- correlation method/status;
- quote timestamp;
- concise reason.

Acceptance:

- historical reports preserve the exact published quote/model snapshot;
- report generation remains possible when EdgeStack is degraded/unavailable; valid singles still publish.

### ES-8 — Website ingestion + archive

Goal: expose the same artifacts on The Daily Line website.

Deliverables:

- publication contract versioning;
- searchable All Bets page/table;
- EdgeStack cards/section;
- filters by sport, game, market class, gate, edge, date;
- historical prediction/result archive;
- exact quote-at-publication display;
- settlement/result state after events complete.

Acceptance:

- website does not recalculate sport probability/value logic;
- website consumes sealed versioned publication artifacts;
- historical prices are not silently replaced by live prices.

### ES-9 — Historical PIT evaluation + calibration

Goal: prove the feature before production-authoritative recommendation.

Deliverables:

- point-in-time replay dataset;
- per-market calibration metrics;
- combo calibration by class and leg count;
- same-game vs cross-game results;
- cross-sport vs same-sport results;
- predicted vs realized hit-rate bins;
- quote break-even vs realized performance;
- gross and fee-aware EV analyses;
- settlement correctness checks;
- model/market regime drift diagnostics.

Acceptance:

- no hindsight/post-start contamination;
- published calibration claims are reproducible;
- minimum promotion thresholds are explicitly defined before production authority.

### ES-10 — Manual certification and TDLA orchestration onboarding

Goal: automate only after the manual EdgeStack workflow is stable and certified.

Deliverables:

- manual workflow certification;
- A-5/A-6 compatible invocation/output contracts;
- TDLA stage fragment;
- readiness/dependency policy;
- retries/idempotency integration;
- publication coordination through certified A-18 authority when available;
- shadow -> supervised -> production equivalence evidence.

Acceptance:

- TDLA orchestrates; it does not calculate sport fair probabilities or EdgeStack value logic;
- automation output is equivalent to the certified manual workflow;
- no external betting/order side effects exist in V1.

## Product copy to preserve

Primary feature name:

> **EdgeStack Parlay Optimizer**

Primary tagline:

> **Stack the Edge. Not the Odds.**

Preferred concise explanation:

> EdgeStack scans every supported bet The Daily Line models, filters individual markets through calibrated probability and Recommendation Gates, then searches 2-5 leg combinations for the strongest relationship between hit probability, market price, correlation, and expected value.

## Required architectural principles

1. Prediction != Market != Value != Recommendation.
2. All supported bets are analyzed before combos are optimized.
3. A combo is built from approved legs; combos do not rescue bad legs.
4. Real combo/parlay quote beats a synthetic multiplication proxy.
5. Same-game dependency requires correlation treatment.
6. Cross-game/cross-sport combinations are first-class candidates.
7. EdgeStack is constrained to 2-5 legs in V1.
8. Hit probability and value are separate ranking dimensions.
9. Every result binds to point-in-time model + quote provenance.
10. Unsupported markets fail closed.
11. Reports publish the entire supported bet universe, not only winners/highlights.
12. EdgeStack never becomes an excuse to add low-quality legs for payout optics.
13. Bankroll/stake logic remains deferred.
14. No automated wagering/order placement in V1.

## Exact future resume point

When the owner explicitly asks to begin EdgeStack implementation:

> **Start ES-0: freeze the EdgeStack runtime ownership/physical repository through ADR and implement the canonical V1 contracts/fixtures in the authorized repository.**

Do not jump directly to UI, Kalshi RFQ automation, or candidate-ranking code before ES-0 contracts and ownership are frozen.

## Current TDLA resume point remains unchanged

This supplemental future-product plan does **not** supersede the repository's current core continuation point:

> **A-11 Retry / Timeout / Idempotency Architecture remains next for core TDLA work.**
