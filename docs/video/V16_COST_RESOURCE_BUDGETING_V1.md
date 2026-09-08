# The Daily Line Video Engine — V-16 Cost / Resource / Provider Budgeting V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Control generation/rendering cost and provider usage without degrading factual integrity or production safety.

## 2. Cost centers

- LLM/script generation;
- image generation;
- stock licensing;
- generative video if ever used;
- TTS;
- music/SFX licensing;
- render compute;
- object storage/egress;
- analytics API usage;
- publication API usage.

## 3. BudgetPolicy

Versioned policies define:
- per-video soft/hard cost caps;
- daily/monthly provider caps;
- sport/platform/template budgets;
- concurrency;
- quota reserve;
- fallback order;
- alert thresholds;
- premium-asset authorization.

## 4. Quality-first fallback

Cost controls may choose cheaper creative implementations but may not:
- lower fact validation;
- bypass rights checks;
- remove mandatory disclosures;
- publish a broken render;
- invent content to avoid an unavailable provider.

## 5. Reuse first

The asset broker checks first-party/cached assets before paid generation. Similarity/dedup rules prevent repeated generation of effectively identical backgrounds.

## 6. Cost evidence

Each VideoJob accumulates estimated and actual cost entries by provider/service, with currency, unit, quantity, timestamp, pricing-policy version, and uncertainty when the provider only exposes estimates.

## 7. Provider abstraction

Fallback across providers requires capability/policy compatibility. A cheaper provider cannot silently change quality/safety/rights assumptions.

## 8. Admission control

Under quota/cost pressure, low-priority videos may be deferred/skipped or rendered data-only. Candidate prioritization can use expected business/content value only under declared policy.

## 9. Tests

- hard cap rejection;
- soft cap fallback;
- provider quota exhaustion;
- cache reuse;
- unavailable image provider -> data-only fallback;
- cost accounting reconciliation;
- premium asset requires authorization.

## 10. Definition of done

V-16 is implementation-ready when the system can explain expected/actual cost of every video and safely degrade creative richness without degrading truth or compliance.