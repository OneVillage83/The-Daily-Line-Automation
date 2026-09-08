# The Daily Line — Social Video Engine Architecture Index

Status: **V1 ARCHITECTURE BASELINE**  
Date: 2026-09-08  
Repository: `The-Daily-Line-Automation` (TDLA)

## Purpose

This directory defines the architecture for The Daily Line Social Video Engine (DLVE): the subsystem that turns certified, publishable sport outputs into reusable branded short-form and long-form video artifacts without moving sport intelligence into TDLA.

The video engine is intentionally housed in TDLA because TDLA owns orchestration, artifact coordination, publication/distribution coordination, operational audit, and future adaptive automation. The sport repositories remain the authority for sport-specific facts, model results, recommendations, interpretations, and explanation claims.

## Core boundary

> **DLVE may transform approved facts into presentation. DLVE may not create new sport truth.**

A sport pipeline (or another certified content-authority producer) must emit a versioned `PublishableFactPackage`. DLVE may select, order, shorten, narrate, caption, visualize, and brand those approved claims, but it may not change numeric values, infer a new recommendation, reinterpret weather/injuries/matchups, or invent supporting reasons.

## Governing documents

| ID | Topic | Authority document |
|---|---|---|
| V-0 | System boundary, topology, ownership, identity | `V00_SOCIAL_VIDEO_ENGINE_ARCHITECTURE_V1.md` |
| V-1 | Wire contracts and canonical schemas | `V01_VIDEO_JOB_AND_FACT_CONTRACTS_V1.md` |
| V-2 | Brand, title sting, motion, captions, audio | `V02_BRAND_MOTION_SYSTEM_V1.md` |
| V-3 | Reusable template/component library | `V03_TEMPLATE_LIBRARY_V1.md` |
| V-4 | Rendering, asset provenance, QC, publication-package handoff | `V04_RENDER_ASSET_QC_HANDOFF_V1.md` |
| V-5 | Performance measurement, experiments, adaptive-selection boundary | `V05_PERFORMANCE_EXPERIMENTATION_V1.md` |

Implementation sequence: `../implementation/VIDEO_ENGINE_IMPLEMENTATION_ROADMAP_V1.md`  
Architecture review: `../implementation/VIDEO_ENGINE_ARCHITECTURE_CONFORMANCE_REVIEW_20260908.md`

Durable technology decision: `../adr/ADR-0008_PARAMETERIZED_VIDEO_RENDERER_AND_FACT_AUTHORITY.md`

## Relationship to the A-0 through A-24 TDLA sequence

The V-series is a **supplemental product subsystem architecture**, not a replacement for the canonical A-series control-plane architecture.

- A-5 / sport adapters provide the eventual certified inter-repository boundary.
- A-6 governs workflow/stage plan authority.
- A-10 governs replaceable worker/execution backend semantics.
- A-11 will govern logical retries/idempotency; DLVE must bind to it rather than inventing a parallel retry identity.
- A-13 will govern authoritative persistence/audit DDL.
- A-14 will govern artifact/replay/reprocess semantics.
- A-15 will govern resource/provider budgets, including image/TTS/render budgets.
- A-16/A-17 will govern telemetry/alerts.
- A-18 will govern actual external publication/distribution side effects. V-4 ends at a validated `VideoPublicationPackage` handoff.
- A-19/A-20 govern approval, security, secrets, and service identities.
- A-22 governs immutable release execution.
- A-24 will govern any adaptive/intelligent automation. V-5 may compute evidence and recommendations but cannot self-authorize production policy changes before A-24.

## Initial implementation technology

The initial renderer is **Remotion + React + TypeScript**, using parameterized compositions and frame-driven animation. Remotion is an implementation runtime, not canonical Daily Line artifact or workflow identity. A future renderer may replace it if it can consume the same canonical video contract and reproduce the required artifact/QC semantics.

The orchestration/control side remains compatible with TDLA's Python baseline. Cross-language video contracts are JSON-based and versioned; implementation code must not create competing Python-only and TypeScript-only meanings for the same field.

## Initial video families

1. `single_pick`
2. `top_three`
3. `model_explainer`
4. `line_movement`
5. `weather_edge`
6. `results_audit`
7. `data_story`

The initial master profile is vertical social video. Additional profiles (horizontal long-form, square, platform-specific variants) are explicit render profiles rather than ad-hoc crop steps.

## Brand-sting rule

The reusable `DailyLineBrandSting` supports `micro`, `opener`, `transition`, and `outro` modes.

Default short-form policy:

- hook/content begins immediately;
- subtle Daily Line watermark may be visible from frame 0;
- the micro sting normally appears **after or within the hook**, not as a blocking multi-second logo intro;
- the full branded close may contain the recommendation/summary so it is not dead screen time;
- placement and timing are experimentable fields recorded in the creative manifest.

## Definition of done for a production video

A video is not publishable merely because an MP4 rendered. It must have:

- a valid versioned input contract;
- approved fact provenance;
- script-to-fact traceability;
- immutable asset provenance and rights metadata;
- a pinned template/brand/render release;
- captions when required by policy;
- passed structural/visual/audio/fact QC;
- a content hash and render manifest;
- a validated publication package;
- production publication authorization through future A-18 policy.

## No implementation authority implied

These documents define the architecture baseline. They do not declare a production video pipeline, social-platform publisher, generated-image provider, TTS provider, or analytics adapter operational until the corresponding implementation/certification milestones pass.