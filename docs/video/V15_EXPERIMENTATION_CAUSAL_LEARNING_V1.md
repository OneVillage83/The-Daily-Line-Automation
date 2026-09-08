# The Daily Line Video Engine — V-15 Experimentation / Causal Learning V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Turn creative decisions into measurable experiments without allowing optimization to alter sport facts or silently chase noisy metrics.

## 2. Experimentable dimensions

- hook family/text variant;
- hook duration;
- brand-sting placement/duration;
- template family/version;
- scene order where semantically equivalent;
- caption style;
- voice profile;
- background/asset style;
- music/SFX treatment;
- CTA style;
- duration band;
- posting window when publication policy permits.

Facts, picks, source probabilities, odds, and source-owned explanations are not experimental creative variables.

## 3. ExperimentDefinition

Includes:
- hypothesis;
- unit of assignment;
- eligible population;
- variants;
- allocation policy;
- primary/secondary/guardrail metrics;
- minimum observation rule;
- start/end/stop policy;
- multiple-testing/sequential policy where relevant;
- platform/sport/template scope;
- analysis version;
- approval/status.

## 4. Assignment

Assignments are immutable and recorded before publication. Opportunistically relabeling a winning post after seeing results is prohibited.

## 5. Primary metrics

Experiments should optimize behavior aligned with business/content goals, usually retention, engaged watch, completion/share/save/follow conversion, not raw views alone.

## 6. Guardrails

At minimum:
- factual integrity failure rate;
- QC failure rate;
- rights/policy incidents;
- negative user-signal thresholds where available;
- render/generation cost;
- production latency;
- publication failure rate.

## 7. Confounding

Sport, event prominence, team popularity, prediction strength, day/time, platform, account age, and posting frequency can confound results. Analysis must preserve these covariates rather than declaring a creative winner from naive aggregate means.

## 8. Small-sample discipline

No automatic production switch based on one viral post or tiny samples. Bayesian/sequential or frequentist methods may be used, but method/version and decision threshold must be declared before authority changes.

## 9. Promotion

Experiment results produce `CreativeRecommendationEvidence`; they do not directly mutate production policy. Promotion to a new default is a versioned approved policy change under V-24/A-24.

## 10. Tests

- immutable pre-assignment;
- invalid fact-changing variant rejection;
- missing primary metric;
- sample-ratio mismatch detection;
- tiny-sample no-promotion;
- confounder-aware reporting;
- cost/latency guardrails;
- reproducible analysis.

## 11. Definition of done

V-15 is implementation-ready when experiment assignment, metrics, analysis, and promotion evidence are versioned and auditable.