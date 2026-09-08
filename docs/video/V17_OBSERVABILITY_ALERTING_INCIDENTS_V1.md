# The Daily Line Video Engine — V-17 Observability / Alerting / Incident Architecture V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Make the video pipeline diagnosable across candidate selection, scripting, assets, audio, rendering, QC, publication handoff, and analytics.

## 2. Tracing

A logical trace links:
`VideoJob -> creative/script -> asset/audio/caption -> RenderJob/attempt -> QC -> publication package -> A-18 receipt -> analytics observations`.

External provider request IDs are child provenance, not canonical trace identity.

## 3. Structured logs

Logs include stable entity refs, stage, attempt, provider, duration, outcome, reason code, and safe diagnostics. No secrets, raw credentials, or unnecessary personal data.

## 4. Metrics

Initial families:
- job counts/outcomes;
- stage latency;
- provider latency/error/rate-limit;
- generation cost;
- render queue/latency/failure;
- QC failures by reason;
- publication-package readiness;
- rights blocks;
- stale-source blocks;
- analytics collection freshness;
- experiment assignment health.

## 5. Alerts

Alert classes include:
- factual-integrity validation anomaly;
- repeated rights/policy blocks;
- render failure spike;
- publication handoff failure;
- source staleness blocking a slate;
- provider quota exhaustion;
- analytics outage;
- unusual cost increase;
- asset/object loss;
- experiment assignment imbalance.

## 6. Incident severity

Suggested classes:
- SEV-1: harmful/widespread incorrect publication or security compromise;
- SEV-2: major production publication outage or repeated invalid-content risk;
- SEV-3: degraded provider/template/platform path with fallback;
- SEV-4: isolated non-user-visible defect.

Exact operational severity policy is versioned.

## 7. Kill switches

Operators need scoped switches by platform/account/sport/template/provider/publication mode. Disabling publication must not erase in-flight evidence.

## 8. Incident evidence

Incidents retain timeline, impacted jobs/posts, root cause, mitigation, corrective actions, related releases/config, and any correction/retraction receipts.

## 9. Tests

- correlation across stages;
- secret sanitization;
- alert dedup;
- provider outage alert;
- kill switch;
- published-wrong-content incident reconstruction;
- monitoring failure not treated as business success/failure.

## 10. Definition of done

V-17 is implementation-ready when operators can determine what failed, where, why, what was affected, and what authority produced each published artifact.