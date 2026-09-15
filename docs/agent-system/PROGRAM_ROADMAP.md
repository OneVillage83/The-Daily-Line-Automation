# Daily Line Program Roadmap

This is the cross-repository macro sequence. Repository-local roadmaps remain authoritative inside their domains.

## Phase 0 — DL-AGENT: Development control system

Goal: make the program resumable and delegable without chat-history reconstruction.

- DL-AGENT-0: baseline system, roles, state, skills, schemas — **ESTABLISHED**.
- DL-AGENT-1: reconcile live repository heads/status documents into program state — **ACTIVE NEXT**.
- DL-AGENT-2: exercise the `daily-line-continue` skill on one bounded real task and record an eval.
- DL-AGENT-3: publish reusable OpenAI Skills when desired.
- DL-AGENT-4: publish reusable Agents API supervisor/specialists only after cost/tool policy and runtime integration are approved.

## Phase 1 — Shared data authority

Goal: stable point-in-time shared facts/providers with sport ownership boundaries preserved.

Primary repository: `Daily-Data-Core`.

Required outcomes include odds, weather, provider evidence, temporal/as-of semantics, data quality/change detection, reproducible releases, and lossless consumer contracts.

Exit gate: MLB/NFL/NCAAF can consume certified shared facts without duplicating generic provider infrastructure.

## Phase 2 — First production sport pipelines

Priority sports: **MLB -> NFL -> NCAAF**.

Each sport must independently own and certify:

- canonical sport identity and state reconstruction;
- point-in-time features and leakage controls;
- sport-specific models/simulation inputs;
- predictions and fair prices;
- value/EV semantics;
- Recommendation Gate reasoning;
- publication-safe explanation packages;
- settlement/outcome semantics;
- reproducibility and audit evidence.

Automation may not hide an unfinished manual pipeline.

## Phase 3 — Daily-Model-Core reusable model families

Primary repository: `Daily-Model-Core`.

Current durable direction:

- DMC-0/DMC-1/DMC-2 foundations are frozen in repository history;
- DMC-3 begins reusable reference/statistical model families and optional-backend architecture;
- later DMC phases add governed calibration, ensembles, evaluation, registry/promotion, replay, and cross-sport reuse.

DMC owns reusable model lifecycle infrastructure; sport repositories own sport truth and sport-specific feature meaning.

## Phase 4 — Sport model integration

For each priority sport, integrate multiple independent model families rather than replacing sport logic with one model.

Target families may include:

- power/Elo-style ratings;
- boosted-tree models;
- Bayesian/hierarchical models;
- sport-specific statistical/physics models;
- simulation models;
- sequence/state models where justified.

Every model retains independent OOS evaluation and provenance.

## Phase 5 — Calibration

Build governed calibration against true OOS prediction evidence.

Required metrics depend on target type and may include Brier score, log loss, reliability/calibration error, coverage, sharpness, interval scoring, and sport/market stratification.

Never calibrate on future information or reuse holdout truth as training evidence.

## Phase 6 — Learned ensemble / Unified Line

Goal: learn the contribution of each model without discarding narrow useful signal.

Architecture:

```text
individual model predictions
        + opening market context where allowed
        + pre-event movement/context features where allowed
        -> governed stacker / learned ensemble
        -> calibrated Unified Line
```

A model may receive low global weight while retaining meaningful conditional importance in a narrow state. Preserve component outputs for attribution, ablation, drift, and audit.

## Phase 7 — Market Intelligence

Integrate the model-derived Unified Line with market information as a separate comparison/intelligence layer.

Includes:

- opening consensus/no-vig market;
- movement history and disagreement;
- sportsbook markets;
- prediction markets when available and contractually appropriate;
- consensus confidence/disagreement;
- price/edge/EV comparisons;
- stale-market and data-quality handling.

Market information must not contaminate model independence where a model is intended to be market-independent.

## Phase 8 — Recommendation and publication outputs

Finalize:

- PASS/AVOID Recommendation Gate;
- complete reasoning/evidence package;
- daily report/PDF;
- infographic;
- final QC;
- Human Review;
- immutable publication artifact provenance;
- searchable historical predictions/results.

## Phase 9 — Website product integration

Primary repository: `The-Daily-Line-website`.

The website should expose simple navigation while supporting:

- daily slate and recommendations;
- model/Unified Line vs market comparison;
- Recommendation Gate and reasoning;
- historical searchable prediction record;
- daily report and infographic access;
- transparent result/audit pages;
- subscription/product integration.

## Phase 10 — Automation

Primary repository: `The-Daily-Line-Automation`.

Automation wraps certified sport behavior and provides scheduling, readiness/dependency checks, workers, retries/idempotency, observability, approval coordination, replay/backfill/reprocess, distribution, and production execution audit.

## Phase 11 — Social/video automation

Use the existing Daily Line Video Engine architecture and VM implementation roadmap.

Content generation may transform approved facts into presentation, but may not invent sport truth or bypass publication review.

## Phase 12 — One Village Command integration

Expose Daily Line status, agent operations, analytics, artifacts, review requests, actions, incidents, communications, and publication through One Village Command contracts/MCP without moving sport authority into Command.

## Phase 13 — Cross-sport expansion

After the priority production pattern is proven, continue to NBA, NCAAB, NHL, women's sports, soccer, tennis, golf, combat sports, motorsports, esports, and other supported markets using shared cores plus sport-owned intelligence.

## Roadmap invariant

Completion order may interleave bounded dependency work, but no later phase may be treated as production-authoritative while a required upstream certification gate is unresolved.