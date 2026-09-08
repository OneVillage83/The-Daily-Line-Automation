# The Daily Line Video Engine — V-14 Analytics Ingestion / Attribution V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define normalized performance evidence for published videos while preserving raw platform metrics and their varying semantics.

## 2. Principle

Platform metrics are observations, not universal truth. The system stores raw source metric names/values plus normalized metrics only when the mapping is defensible and versioned.

## 3. PerformanceObservation

Includes:
- platform/account/post receipt ref;
- observation timestamp;
- metric window/age since publication;
- raw metrics payload hash/reference;
- normalized metrics;
- API/provider/version;
- collection status;
- correction/supersession lineage.

## 4. Initial normalized dimensions

When available:
- impressions/reach;
- views/engaged views;
- total watch time;
- average watch duration;
- average percent viewed;
- completion rate;
- rewatch proxy;
- likes;
- comments;
- shares;
- saves;
- follows/subscribers attributable where exposed;
- profile actions;
- link/site actions where instrumented.

Missing metrics remain missing; they are not zero-filled unless semantics explicitly say zero.

## 5. Cohort windows

Metrics are collected at versioned observation windows such as early, 24h, 72h, 7d, 30d where platform/API limits permit. Exact windows are policy-configured, not hard-coded as universal truth.

## 6. Attribution

Every observation links to exact creative/template/hook/sting/caption/voice/asset/platform/post-time experiment metadata. Content performance must not be attributed only to sport or pick outcome.

## 7. Outcome separation

Prediction correctness and audience performance are separate dimensions. A losing pick with excellent retention is a successful creative treatment but not a successful prediction; the system must never conflate them.

## 8. Raw evidence

Store raw API response provenance or durable normalized source evidence sufficient to re-evaluate mappings later. Platform corrections may create superseding observations.

## 9. Rate limits/failures

Analytics collection follows provider budgeting, retry, and freshness policies. Missing analytics cannot block the already-completed historical publication record.

## 10. Tests

- absent metric vs zero;
- renamed platform metric mapping;
- duplicate observation;
- corrected metric supersession;
- post identity linkage;
- multi-platform same-video separation;
- prediction-outcome vs creative-performance separation.

## 11. Definition of done

V-14 is implementation-ready when every supported platform can feed auditable raw/normalized observations into a common model without pretending incompatible metrics are identical.