# EdgeStack Parlay Optimizer V1

**Status:** DOCUMENTED — IMPLEMENTATION NOT YET AUTHORIZED  
**Date:** 2026-09-17  
**Product:** The Daily Line  
**Feature name:** **EdgeStack**  
**Tagline:** **Stack the Edge. Not the Odds.**

## 1. Purpose

EdgeStack is The Daily Line's probability-first, market-aware **parlay/combo optimizer**.

The feature exists to turn The Daily Line's calibrated individual-bet predictions into short, disciplined 2-5 leg combinations chosen for the relationship between:

- model-estimated probability;
- market-implied probability;
- offered combo/parlay payout;
- cross-leg correlation;
- expected value;
- uncertainty/calibration quality; and
- recommendation-gate eligibility.

EdgeStack is explicitly **not** a lottery-ticket generator. It must not add weak legs merely to increase a displayed multiplier.

The core product promise is:

> **Stack the Edge. Not the Odds.**

The Daily Line should first evaluate the full supported betting market universe, publish its model view and Recommendation Gate for every supported bet, and only then optimize short combinations from eligible legs.

## 2. Product differentiation

Most parlay products start with payout size and search for legs that create an attractive multiplier.

EdgeStack reverses that process:

1. model the game/event/player;
2. generate a calibrated fair probability for every supported priceable market;
3. compare the fair probability with the observed market price;
4. apply the Recommendation Gate;
5. create a pool of individually admissible legs;
6. generate candidate 2-5 leg combinations;
7. estimate correlation-adjusted joint probability;
8. compare joint probability with the actual offered combo/parlay price;
9. rank the combinations by probability, value, uncertainty, and correlation quality; and
10. publish only combinations that satisfy configured quality gates.

This creates a market-facing feature that can be explained as both:

- an **all-bets prediction scanner**, and
- a **parlay optimizer** built on top of The Daily Line's model stack.

## 3. Architectural boundary

This document is stored in The-Daily-Line-Automation because TDLA is the cross-repository coordination/control-plane repository and will eventually orchestrate the workflow and publication lifecycle.

TDLA **must not** absorb the betting intelligence defined here.

Existing ownership boundaries remain authoritative:

- **Daily-Data-Core (DDC)** owns sport-agnostic market observations, provider normalization, quote provenance, timestamps, and generic market-data contracts.
- **Daily-MLB, Daily-NFL, Daily-NCAAF, and future Daily-* sport repositories** own sport-specific prediction features/models, fair probabilities, sport-specific market interpretation, Recommendation Gate semantics, and settlement interpretation.
- **EdgeStack Engine** is the logical cross-sport optimization component that consumes versioned model/gate/market outputs and produces combination recommendations. Its final physical repository/package home must be frozen by ADR before implementation. It must not be implemented as hidden TDLA sport intelligence.
- **The Daily Line website/app** owns presentation, discovery, filtering, historical browsing, and user-facing product state.
- **TDLA** later owns scheduling, dependency/readiness checks, orchestration, publication coordination, retries/idempotency, and immutable run provenance after the manual EdgeStack workflow is certified.

## 4. V1 scope

EdgeStack V1 covers:

- exhaustive evaluation of **every supported and modelable bet known to the system** for a slate/event;
- standardized publication of each supported bet's model probability, market probability/price, model edge, recommendation gate, reason/evidence, and quote timestamp;
- 2-5 leg candidate generation;
- cross-game combinations;
- cross-sport combinations;
- same-game combinations only when correlation is explicitly modeled;
- Kalshi Combo/RFQ price evaluation;
- traditional sportsbook parlay price evaluation where a supported provider exposes a valid quote;
- Core, Value, and Upside EdgeStack classifications;
- immutable publication artifacts suitable for reports, website ingestion, and later automation;
- historical evaluation and calibration of both legs and combinations.

## 5. Explicit V1 non-goals

The following are deliberately **out of scope** for this architecture version:

- bankroll management;
- Kelly sizing;
- stake recommendations;
- daily loss limits or stop-loss rules;
- chase-prevention logic;
- wallet/account integration;
- automatic bet placement;
- autonomous wagering;
- personalized wagering amounts.

A future bankroll/risk-management architecture may consume EdgeStack outputs, but it must be designed separately and must not be silently added to V1.

## 6. Supported betting-market universe

The pipeline should evaluate every market class that is both available from a supported provider and supported by a certified model/settlement contract.

Initial classes include, where the sport supports them:

- moneyline / winner;
- spread / run line / puck line;
- game total;
- team total;
- player passing/rushing/receiving/hitting/pitching and other certified player props;
- alternate thresholds/ladder markets;
- touchdown / scoring markets when a calibrated probability model exists;
- first-five / first-half / period markets when explicitly modeled;
- other derivative markets only after their prediction and settlement semantics are certified.

The phrase **every possible bet** means every currently supported, priceable, settlement-defined market for which The Daily Line has sufficient model authority. Unsupported markets must be labeled unsupported rather than assigned guessed probabilities.

## 7. All-Bets Prediction Scanner

Before EdgeStack optimization, each slate must produce an `AllBetsSnapshot` containing all supported market candidates.

Each bet row should include at minimum:

- `bet_id` / canonical market key;
- sport / league / event / participant identity refs;
- market class and side;
- threshold/line;
- provider / venue;
- observed quote and timestamp;
- market-implied probability;
- fee-aware break-even probability where applicable;
- Daily Line calibrated fair probability;
- probability uncertainty interval or calibration-quality metadata;
- edge in percentage points;
- expected value where the payout contract permits deterministic calculation;
- Recommendation Gate state (`PLAY`, `PASS`, `AVOID`, or the certified equivalent);
- concise model reasoning/evidence refs;
- model/config/version/provenance IDs;
- data-cutoff timestamp;
- settlement-rule version;
- freshness / stale-quote status.

The public report and website should expose this scanner so users can inspect the model view for the entire supported slate, not only highlighted picks.

## 8. EdgeStack leg eligibility

A market may enter the EdgeStack candidate pool only when all required gates pass.

V1 eligibility requirements:

1. market has a canonical settlement definition;
2. market quote is current enough under provider-specific freshness policy;
3. sport model emits a calibrated fair probability;
4. data cutoff is valid and contains no post-start leakage;
5. Recommendation Gate permits use as an EdgeStack leg;
6. model/calibration quality is above configured minimums;
7. provider quote is executable/realistic enough for the chosen publication mode;
8. required correlation metadata is available for any same-event dependency; and
9. no explicit exclusion/policy block applies.

A leg that fails individually cannot be rescued by placing it inside a high-payout combination.

## 9. Candidate generation

The optimizer enumerates combinations from the eligible leg pool with a hard V1 range of **2 through 5 legs**.

Candidate-generation rules:

- generate cross-game combinations by default;
- allow cross-sport combinations;
- allow same-game legs only with supported correlation treatment;
- reject logically contradictory legs;
- reject duplicate/equivalent market exposure;
- reject combinations containing stale/expired quotes;
- reject combinations that require unsupported settlement dependencies;
- apply configurable limits to repeated exposure to the same event/player/root outcome;
- retain deterministic candidate identity so the same inputs produce the same candidate key;
- do not add a leg solely because it increases the displayed multiplier.

The combinatorial search must be bounded and reproducible. Production implementation may use pruning/branch-and-bound/top-K search, but pruning may not depend on presentation order or provider UI ordering.

## 10. Joint probability and correlation

### 10.1 Independent or effectively independent legs

For legs from unrelated events with no modeled dependency, joint probability may begin with:

`P(combo) = product(P(leg_i))`

provided each leg probability is calibrated and the independence assumption is documented.

### 10.2 Correlated legs

Same-game and otherwise dependent legs must not be priced as independent.

Preferred V1 authority order:

1. joint samples from a certified game/sport simulation model;
2. empirically calibrated joint-distribution model;
3. approved pairwise/higher-order correlation model with documented limitations;
4. otherwise **do not publish the correlated combination as an authoritative EdgeStack**.

Positive correlation commonly appears in relationships such as quarterback passing yards and a receiver's receiving yards. Negative or nonlinear dependencies also occur and must be modeled rather than assumed.

### 10.3 Uncertainty

EdgeStack should retain uncertainty around the joint probability. Ranking may use both a point estimate and a conservative/lower-confidence estimate so unstable model disagreement is not presented as false precision.

## 11. Pricing and value

For a decimal combo multiplier `M`:

`break_even_probability = 1 / M`

Before fees/slippage:

`gross_expected_return = P(combo) * M`

`gross_EV = (P(combo) * M) - 1`

For Kalshi or other venues with fees, spread, RFQ behavior, or nontrivial execution cost, the engine must calculate a fee-aware/net break-even and EV when the fee schedule/quote is available.

Required comparison fields:

- quoted multiplier / contract price;
- raw break-even probability;
- net break-even probability when calculable;
- Daily Line joint probability;
- probability edge;
- gross EV;
- net EV when calculable;
- quote timestamp / expiry/freshness;
- correlation method and confidence;
- model/provenance IDs.

## 12. Kalshi Combo behavior

Kalshi Combos may be generated through live RFQ-style pricing and may apply correlation adjustments similar to a sportsbook same-game parlay.

EdgeStack must therefore treat a Kalshi combo quote as a **market observation**, not as the mechanical product of standalone prices.

Workflow:

1. generate a candidate from model-approved legs;
2. obtain/ingest the actual Kalshi Combo quote when available;
3. calculate the Combo's break-even probability from the quote;
4. compare it with the model's correlation-adjusted joint probability;
5. reject the combo if the quote has expired/staled or no longer passes the configured value gate;
6. store quote provenance and timestamp in the publication artifact.

The engine may use the product of standalone prices as a diagnostic reference, but never as a substitute for an available real Combo quote.

## 13. EdgeStack classes

### 13.1 Core EdgeStack

Purpose: prioritize **highest realistic hit probability while retaining positive model-vs-price value**.

Typical properties:

- 2-3 legs;
- lower alternate thresholds may be preferred when their combined price remains favorable;
- usually lower variance than other EdgeStack classes;
- may use cross-game/cross-sport legs to avoid unnecessary correlation haircuts.

### 13.2 Value EdgeStack

Purpose: optimize the balance of probability, net EV, payout, and model confidence.

Typical properties:

- 2-4 legs;
- positive net model edge required;
- moderate payout;
- preferred default showcase when probability and price both grade strongly.

### 13.3 Upside EdgeStack

Purpose: retain favorable pricing while accepting higher variance for a larger payout.

Typical properties:

- 3-5 legs;
- stronger payout requirement;
- stricter minimum EV and confidence requirements than an ordinary longshot;
- still composed only of individually approved legs.

A giant lottery parlay is not automatically an EdgeStack merely because its theoretical EV is positive.

## 14. Ranking model

EdgeStack must publish separate metrics rather than collapsing everything into one opaque score.

Required ranking dimensions:

- joint hit probability;
- net EV / expected return;
- probability edge versus break-even;
- correlation quality;
- calibration quality;
- uncertainty width;
- quote freshness;
- leg count;
- payout/multiplier.

A derived ranking score may be introduced later, but the underlying dimensions must remain visible and auditable.

Recommended ranking views:

- `HIGHEST_HIT_RATE`;
- `BEST_VALUE`;
- `BEST_BALANCE`;
- `BEST_UPSIDE`.

This avoids pretending that a 65% 1.9x Core EdgeStack and a 22% 6.3x Value/Upside EdgeStack solve the same user objective.

## 15. Publication contract

Each published EdgeStack should contain:

- stable `edgestack_id`;
- slate/date/sport scope;
- class (`CORE`, `VALUE`, `UPSIDE`);
- ordered display legs plus canonical unordered/semantic leg set identity where needed;
- each leg's fair probability, market price, edge, gate, and provenance;
- quoted combo multiplier/price;
- break-even probability;
- joint model probability;
- uncertainty/confidence metadata;
- gross/net EV fields where calculable;
- correlation method/summary;
- quote timestamp and freshness/expiry;
- concise explanation;
- model/config/data-cutoff IDs;
- publication timestamp;
- result/settlement fields after completion.

Reports and website pages must preserve the exact quote/model snapshot used at publication rather than silently replacing historical prices with current prices.

## 16. Report and website experience

The Daily Line report should include two first-class sections.

### 16.1 All Bets

A searchable/filterable table of every supported analyzed bet for the slate, including:

- fair probability;
- market probability/price;
- edge;
- Recommendation Gate;
- concise reason;
- quote time;
- model confidence/calibration metadata.

### 16.2 EdgeStack Parlay Optimizer

Recommended presentation:

- **Core EdgeStack** — highest-probability qualifying combination;
- **Value EdgeStack** — strongest probability/value balance;
- **Upside EdgeStack** — larger payout that still clears strict model/value gates;
- additional ranked candidates where product design permits;
- clear display of hit probability, break-even probability, multiplier, edge, EV, leg count, correlation status, and quote timestamp.

Marketing/product copy may describe EdgeStack as:

> **The Daily Line EdgeStack Parlay Optimizer**  
> **Stack the Edge. Not the Odds.**

## 17. Historical evaluation and calibration

EdgeStack must be evaluated historically before production-authoritative publication.

Required evaluation includes:

- point-in-time market snapshots only;
- no post-start data contamination;
- per-leg calibration by market class;
- joint probability calibration by combo class/leg count;
- Brier/log-loss or other approved probability metrics;
- predicted-versus-realized hit-rate bins;
- quoted break-even versus realized performance;
- gross and fee-aware EV tracking;
- same-game versus cross-game performance;
- cross-sport versus single-sport performance;
- calibration drift and model-regime monitoring;
- settlement correctness;
- stale-quote / unavailable-quote audit.

Historical results must distinguish what was actually available at the prediction cutoff from what became known later.

## 18. Failure/degradation behavior

EdgeStack should fail closed when:

- a required leg probability is missing;
- a quote is stale or malformed;
- settlement semantics are ambiguous;
- model/config/data-cutoff provenance is incomplete;
- a same-game correlation cannot be modeled safely;
- Recommendation Gate authority is missing;
- a provider's Combo quote cannot be reconciled with the candidate identity;
- a required input comes from post-start information.

A failed EdgeStack generation step must not invalidate the underlying single-bet report. The All Bets scanner may still publish valid singles while EdgeStack is marked unavailable/degraded.

## 19. Cross-repository pipeline placement

Conceptual flow:

```text
Sport raw/derived data
        |
        v
Sport-specific prediction models
        |
        v
Calibrated fair probabilities / Unified Line
        |
        +--------------------+
        |                    |
        v                    v
Recommendation Gate     DDC market observations
        |                    |
        +---------+----------+
                  v
          All Bets Snapshot
                  |
                  v
          EdgeStack Engine
      2-5 leg candidate search
       correlation adjustment
        real quote comparison
          ranking / classes
                  |
                  v
    EdgeStack Publication Package
                  |
          +-------+-------+
          |               |
          v               v
      Daily Report      Website/App
```

Later, once the manual workflow is certified, TDLA may orchestrate this pipeline through normal A-series scheduling/readiness/execution/publication contracts. TDLA never becomes the authority for sport probabilities, Recommendation Gate semantics, or EdgeStack value mathematics.

## 20. Required invariants

1. Prediction != market != value != recommendation.
2. A high payout is not evidence of value.
3. A high hit probability is not evidence of value unless the price is favorable enough.
4. A positive-value individual leg is not automatically a positive-value combination after correlation and provider pricing.
5. Same-game correlation must be modeled or the combo is not authoritative.
6. Cross-game independence is an assumption that must be explicit and testable.
7. Every published number binds to a point-in-time quote and model/data cutoff.
8. No weak leg is added merely to increase multiplier.
9. V1 EdgeStacks contain 2-5 legs only.
10. Every EdgeStack leg must independently satisfy eligibility and Recommendation Gate requirements.
11. Unsupported markets are labeled unsupported, not guessed.
12. Historical evaluation must use point-in-time inputs only.
13. Publication history is immutable/auditable.
14. EdgeStack may optimize combinations; it does not place bets.
15. Bankroll/stake management is outside V1.

## 21. Acceptance criteria before production-authoritative use

EdgeStack cannot become production-authoritative until all of the following are true:

- canonical market and leg contracts exist;
- each supported sport emits calibrated per-market fair probabilities;
- Recommendation Gate integration is versioned and deterministic;
- DDC supplies point-in-time normalized market quote provenance;
- deterministic 2-5 leg candidate generation is implemented;
- correlation/joint-probability method is validated for every published dependency class;
- Kalshi/provider quote ingestion/RFQ identity is preserved;
- gross and fee-aware break-even/EV calculations are tested;
- historical point-in-time backtests pass defined calibration thresholds;
- same-game/cross-game/cross-sport evaluation is separately reported;
- publication contracts are stable;
- report and website consumers display model probability and market break-even distinctly;
- settlement/audit pipeline verifies outcomes correctly;
- manual workflow is certified before TDLA automation becomes authoritative.

## 22. Future extensions intentionally deferred

Potential later additions include:

- bankroll/risk manager;
- user-specific risk preferences;
- stake sizing;
- portfolio-level exposure optimization;
- cross-book execution routing;
- liquidity-aware sizing;
- automated order placement where legally/operationally appropriate;
- adaptive candidate-search policy;
- learned combination-ranking models.

These require separate architecture/certification and are not part of EdgeStack V1.
