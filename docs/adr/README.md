# Architecture Decision Records (ADR)

This directory records durable architecture decisions, alternatives, tradeoffs, and supersession history for The-Daily-Line-Automation.

## Authority relationship

ADRs explain durable decisions. They do not silently override governing architecture. If an ADR changes a certified contract, the affected architecture and certification/status documentation must be versioned/updated in the same logical change.

## Index

- `ADR-0001_CONTROL_PLANE_AND_VENDOR_NEUTRAL_IDENTITY.md` — TDLA canonical automation identity/audit; Prefect is replaceable runtime.
- `ADR-0002_TRANSPORT_NEUTRAL_SPORT_ADAPTER_PROTOCOL.md` — transport-neutral Sport Automation Adapter.
- `ADR-0003_IMMUTABLE_PLAN_FRAGMENTS_AND_EXPLICIT_COMPOSITION.md` — immutable plan fragments and explicit composition.
- `ADR-0004_DURABLE_TRIGGER_EVIDENCE_AND_REEVALUATION_ONLY_AUTHORITY.md` — triggers are durable reevaluation evidence, not execution authority.
- `ADR-0005_STABLE_SCHEDULE_SLOTS_AND_RESOLVED_TIME_AUTHORITY.md` — stable schedule slots and immutable resolved-time authority.
- `ADR-0006_VERSION_BOUND_DISPATCH_ELIGIBILITY_AND_FINAL_REVALIDATION.md` — version-bound eligibility and mandatory final current-authority revalidation.
- `ADR-0007_IMMUTABLE_EXECUTION_ENVELOPE_AND_RECONCILABLE_BACKEND_DISPATCH.md` — immutable execution envelope and reconciliable backend dispatch.
- `ADR-0008_PARAMETERIZED_VIDEO_RENDERER_AND_FACT_AUTHORITY.md` — DLVE uses a parameterized replaceable renderer with sport-owned fact authority and Remotion as V1 implementation.
- `ADR-0009_RIGHTS_FIRST_MEDIA_PROVENANCE_AND_NON_DOCUMENTARY_GENERATIVE_VISUALS.md` — every media asset retains exact-use rights/provenance; generated visuals cannot masquerade as documentary evidence.
- `ADR-0010_BOUNDED_ADAPTIVE_CREATIVE_SELECTION.md` — future optimization can select only among certified creative actions and cannot mutate sport truth/compliance/QC.

## Required ADR content

An ADR should include context, decision, alternatives, consequences, compatibility/migration, operational/security impact where relevant, validation requirements, and related architecture sections. Superseded decisions remain historical evidence.