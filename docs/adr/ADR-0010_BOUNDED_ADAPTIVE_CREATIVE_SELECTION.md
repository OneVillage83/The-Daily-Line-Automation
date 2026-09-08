# ADR-0010 — Bounded Adaptive Creative Selection

Date: 2026-09-08
Status: ACCEPTED

## Context

The Daily Line should learn from retention, completion, shares, saves, follows, costs, and other performance evidence. An unconstrained optimizer could accidentally mutate facts, overfit tiny samples, exploit misleading claims, hide losing outcomes, or bypass compliance/rights/QC to chase engagement.

## Decision

Adaptive optimization is limited to selection among an enumerated set of already-certified creative treatments. Facts, recommendations, probabilities, odds, source explanations, disclosures, rights decisions, and QC requirements are immutable inputs outside the action space.

The maturity path is offline analysis -> recommendation -> shadow -> supervised -> bounded automatic selection. Any automatic authority remains subordinate to TDLA A-24. A static certified fallback and kill switch are mandatory.

## Alternatives considered

1. Let an LLM freely optimize the entire video — rejected because it collapses fact and creative authority.
2. Use a black-box engagement optimizer — rejected because guardrails/provenance would be inadequate.
3. Never adapt automatically — safe but prevents later performance gains; bounded adaptation preserves upside without surrendering authority.

## Consequences

- Creative options must be explicitly versioned/certified.
- Experiment design and promotion evidence become first-class artifacts.
- Some potentially high-performing but unapproved ideas remain human-reviewed until certified.

## Compatibility

Aligns with V-5/V-15/V-24 and TDLA A-24.

## Validation required

Action-space enforcement, fact immutability, sample-size/guardrail behavior, drift, rollback, policy-version provenance, and kill-switch scenarios are mandatory.