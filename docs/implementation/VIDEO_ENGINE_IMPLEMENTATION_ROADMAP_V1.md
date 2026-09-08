# Daily Line Video Engine — Implementation Roadmap V1

Date: 2026-09-08  
Subsystem: DLVE — Daily Line Video Engine

## Purpose

This roadmap converts the V-0 through V-5 architecture into an implementation sequence that preserves TDLA's architecture-first/manual-first discipline.

No milestone below grants production social-publication authority by itself. External posting remains blocked on the future A-18 publication architecture and the normal TDLA certification gates.

## VM-0 — Contract and Fixture Foundation

### Goal

Create the cross-language canonical contract package before building renderer behavior.

### Deliverables

- `packages/video-contracts/schemas/`
- JSON Schemas for:
  - `PublishableFactPackage`
  - `ContentCandidate`
  - `CreativePlan`
  - `ScriptPackage`
  - `FactIntegrityReport`
  - `AssetManifest`
  - `VoicePackage`
  - `CaptionPackage`
  - `VideoRenderSpec`
  - `RenderManifest`
  - `VideoQcReport`
  - `VideoPublicationPackage`
  - metric/experiment contracts
- valid/invalid fixtures for MLB/NFL/NCAAF-neutral examples;
- Python validator/type adapter;
- TypeScript generated/validated types;
- fixture parity tests.

### Exit gate

The same fixtures validate identically in Python and TypeScript. Invalid fact/protected-token cases fail closed.

## VM-1 — Remotion Renderer Scaffold

### Goal

Create `apps/video-renderer` as a replaceable renderer adapter.

### Deliverables

- Remotion blank project;
- root composition registry;
- canonical render-spec adapter;
- local Studio preview;
- basic render command wrapper;
- render-profile handling;
- one fixture composition;
- test/CI skeleton.

### Exit gate

A valid fixture renders. The renderer cannot render from raw sport data or unvalidated arbitrary props.

## VM-2 — Brand Foundation

### Goal

Build The Daily Line's reusable motion/visual identity.

### Deliverables

- brand token package;
- typography tokens;
- layout/safe-zone tokens;
- `DailyLineLogo`;
- `DailyLineWatermark`;
- `DataGridBackground`;
- `DailyLineBrandSting` `micro` mode;
- `DailyLineBrandSting` `outro` mode;
- initial sound-sting slot;
- golden still fixtures.

### Exit gate

The same component renders both micro and outro modes, supports sport accents, and has no sport calculations.

## VM-3 — Shared Data Component Library

### Goal

Create reusable primitives used by every sport.

### Deliverables

- `StatCard`
- `ComparisonCard`
- `ProbabilityMeter`
- `LineMovementChart`
- `WeatherPanel`
- `PickReveal`
- `ResultBadge`
- `SectionLabel`
- `CTAChip`
- `DisclaimerLayer`
- caption layers
- text-fit/overflow utilities
- visual regression fixtures.

### Exit gate

Long labels, negative/positive odds, percentages, decimals, and disclaimer stress fixtures pass layout checks.

## VM-4 — `single_pick_v1` Reference Template

### Goal

Prove the end-to-end renderer architecture using synthetic/fixture facts.

### Deliverables

- hook scene;
- brand micro transition;
- reason/stat scene;
- model/comparison scene;
- pick reveal;
- branded outro;
- no-image fallback;
- no-voice fallback;
- dynamic duration calculation;
- fixture MP4 render and QC manifest.

### Exit gate

A fully synthetic V-1 package passes fact/QC validation and renders a publication-package-ready artifact without any live sport dependency.

## VM-5 — Fact-Bound Script Planner

### Goal

Add LLM-assisted presentation without allowing sport hallucination.

### Deliverables

- prompt/template registry;
- claim/fact reference injection;
- protected-token handling;
- factual vs non-factual segment classification;
- deterministic validation after generation;
- unsupported-claim rejection;
- exact transformation audit;
- provider abstraction.

### Exit gate

Mutation tests show changed odds/probabilities/team values and unsupported reasons are rejected. A provider failure does not corrupt approved fact packages.

## VM-6 — Asset Broker / Generated-Still Pipeline

### Goal

Resolve visuals cheaply and reproducibly.

### Deliverables

- asset slot resolver;
- owned/cached asset library;
- generic generated-image provider adapter;
- stock adapter interface;
- provenance/right metadata;
- content-hash storage;
- generated-image caching;
- data-only fallback;
- prompt-template versioning.

### Exit gate

A video can render successfully with cached/generic stills and without generative video. Unknown-rights assets are blocked.

## VM-7 — Voice, Captions, and Audio

### Goal

Add optional voice/TTS and structured captions.

### Deliverables

- replaceable TTS adapter;
- voice profile registry;
- script-segment timing mapping;
- canonical caption package;
- Remotion caption adapter;
- kinetic/lower/stat-focus caption styles;
- music/SFX asset policy;
- no-voice fallback path.

### Exit gate

Caption text/protected values match approved script; voice and no-voice variants are separately identified creative variants.

## VM-8 — Render Worker + QC Pipeline

### Goal

Integrate rendering with TDLA execution semantics without making Remotion a control-plane authority.

### Deliverables

- A-10 worker class/adapter plan for video renders;
- immutable render spec handoff;
- render manifest;
- media probe;
- layout/overflow/safe-zone checks;
- asset rights checks;
- audio/caption checks;
- publication package builder;
- cost/resource evidence.

### Dependencies

- A-11 retry/idempotency must be integrated before production authority;
- A-13 persistence mechanics remain deferred until certified.

### Exit gate

A failed render cannot trigger uncontrolled duplicate work. QC failure blocks publication package approval.

## VM-9 — First Real MLB Shadow Input

### Goal

Consume a real MLB publishable fact package in **shadow** mode.

### Preconditions

- source MLB workflow/output required for the video is certified;
- an explicit publishable fact contract exists;
- no production social side effects;
- V-1 contract adapter passes certification.

### Deliverables

- MLB `PublishableFactPackage` adapter/output;
- one real `single_pick_v1` render;
- fact trace audit;
- human comparison to source report;
- no external post.

### Exit gate

Video matches certified source meaning exactly and no sport interpretation was added by DLVE.

## VM-10 — Template Expansion

Build in order:

1. `top_three_v1`
2. `results_audit_v1`
3. `line_movement_v1`
4. `weather_edge_v1`
5. `model_explainer_v1`
6. `data_story_v1`

Each template receives fixture, fallback, protected-token, layout, and render tests.

## VM-11 — NFL/NCAAF Shadow Compatibility

### Goal

Prove that the same contracts/components work for football without branching generic renderer logic around football semantics.

### Exit gate

NFL/NCAAF adapters can populate the same canonical fact/render contracts; sport-specific explanations remain source-owned.

## VM-12 — Publication Integration

### Blocker

**A-18 Publication / Distribution Architecture must be certified first.**

### Future deliverables

- platform adapters;
- account/service identity;
- upload/create-post flows;
- external idempotency/reconciliation;
- receipts;
- schedule/window handling;
- edit/delete/correction operations;
- publication audit.

The V-series `VideoPublicationPackage` is the input contract.

## VM-13 — Performance Metric Adapters

### Goal

Ingest per-post metrics and bind them to exact creative variants.

### Deliverables

- raw snapshot adapters;
- normalized metric model;
- observation windows;
- creative feature manifests;
- reporting tables/dashboard feed;
- platform metric semantic notes.

## VM-14 — Experiment Framework

### Goal

Run deliberate creative experiments.

### Deliverables

- experiment registry;
- deterministic variant allocation;
- primary/guardrail metrics;
- analysis reports;
- template/hook/sting/caption/voice test support;
- cost-aware performance analysis.

### Policy

Human/config release remains required for production creative-policy changes before A-24.

## VM-15 — Adaptive Creative Selection

### Blocker

**A-24 Future Adaptive / Intelligent Automation Architecture must explicitly authorize it.**

Potential future scope:

- bandit/online allocation among already approved creative variants;
- sport/platform-specific hook selection;
- duration/pacing selection;
- asset-style selection;
- posting-window recommendation.

Never in scope:

- changing sport facts;
- changing recommendations;
- changing model thresholds;
- bypassing disclaimers/compliance.

## Initial implementation priority

If implementation begins before the broader TDLA core sequence reaches A-18, the safe local development path is:

```text
VM-0 contracts
 -> VM-1 renderer scaffold
 -> VM-2 brand foundation
 -> VM-3 components
 -> VM-4 synthetic single-pick reference
```

That path creates no external publication side effects and does not require Daily-MLB/NFL/NCAAF production automation.

## Definition of implementation readiness

A video milestone is not considered complete until:

- tests pass;
- documentation/change record is current;
- exact contract/release versions are recorded;
- visual/fact/QC evidence is retained;
- rollback/recovery behavior is understood;
- resume point names the next exact task;
- no A-series ownership/deferred-authority boundary was silently implemented early.