# Architecture Decision Records (ADR)

This directory records durable architecture decisions, alternatives, tradeoffs, and supersession history for The-Daily-Line-Automation.

## When an ADR is required

Create an ADR when a change materially affects one or more of:

- repository/system ownership boundaries;
- canonical identity semantics;
- persistence authority;
- orchestration/runtime technology with architectural consequences;
- deployment model;
- security/service identity;
- public/inter-repository contracts;
- compatibility/migration strategy;
- failure/recovery/idempotency guarantees;
- publication side-effect model;
- significant technology selection where replacement cost/tradeoffs matter.

Routine implementation details that simply conform to certified architecture do not require an ADR, but they still require a `CHANGE_JOURNAL.md` record when material.

## ADR format

Each ADR should include:

- title and stable number;
- date;
- status (`PROPOSED`, `ACCEPTED`, `SUPERSEDED`, `REJECTED`);
- context/problem;
- decision;
- alternatives considered;
- consequences/tradeoffs;
- compatibility/migration impact;
- security/operational impact when relevant;
- validation required;
- related architecture sections;
- supersedes/superseded-by links.

## Authority relationship

An ADR explains a decision. It does not silently override governing architecture.

If an accepted ADR changes a certified architecture contract, the same logical change must:

1. update/version the affected architecture document;
2. update the architecture certification log;
3. append the change journal;
4. update the current resume point;
5. include migration/compatibility notes.

## Index

- `ADR-0001_CONTROL_PLANE_AND_VENDOR_NEUTRAL_IDENTITY.md` — TDLA owns canonical automation identity/audit; Prefect is an initial replaceable runtime.
- `ADR-0002_TRANSPORT_NEUTRAL_SPORT_ADAPTER_PROTOCOL.md` — Sport Automation Adapter is a versioned transport-neutral protocol boundary; TDLA does not canonically depend on sport Python imports, HTTP, or Prefect-specific integration semantics.
- `ADR-0003_IMMUTABLE_PLAN_FRAGMENTS_AND_EXPLICIT_COMPOSITION.md` — sport/platform plan fragments remain immutable and separately owned; cross-fragment bindings are explicit and typed; conflicts fail closed; the immutable `ResolvedAutomationPlan` is the canonical executable plan authority.
