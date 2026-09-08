# ADR-0008 — Parameterized Social Video Renderer and Fact-Authority Boundary

Date: 2026-09-08  
Status: **ACCEPTED**

## Context

The Daily Line needs an automated social-video system capable of producing high-volume MLB/NFL/NCAAF and future multi-sport content for short-form and long-form channels.

Several implementation approaches are possible:

1. manually edit every video;
2. use a proprietary generative-video platform for most/all scenes;
3. build fixed pre-rendered templates in traditional video software;
4. generate motion through FFmpeg/custom canvas code;
5. use a programmatic React video renderer such as Remotion;
6. combine a programmatic renderer with reusable still/generated/stock assets, voice, captions, data graphics, and an external orchestration layer.

The repository also has a strict ownership rule: TDLA coordinates automation/publication but may not absorb sport intelligence. A video system that hands raw model/odds/weather/state data to an LLM and asks it to invent a compelling sports story would violate that boundary and make factual provenance difficult to audit.

## Decision

### 1. Use a parameterized render architecture

The Daily Line Social Video Engine (DLVE) will produce videos from explicit versioned data contracts and reusable template/components rather than editing each video manually or generating every scene as unconstrained AI video.

### 2. Remotion is the initial renderer

Remotion + React + TypeScript is the initial rendering runtime because it supports reusable component composition, frame-driven deterministic animation, parameterized compositions, image/audio/video integration, captions, and programmatic rendering.

Remotion is **not** canonical Daily Line workflow/story/render identity authority. A renderer adapter consumes a canonical `VideoRenderSpec`; a future renderer may replace Remotion if it can satisfy the same contract and artifact/QC semantics.

### 3. Approved facts precede script generation

Sport repositories or other certified content authorities emit a versioned `PublishableFactPackage` containing approved facts, claims, explanations, recommendation state, validity/expiry, and provenance.

The DLVE script layer may shorten, order, paraphrase, or narrate approved content but may not derive new sport conclusions or modify protected numeric values.

### 4. Generated stills/stock/data motion are preferred before generative video

Routine videos should primarily combine:

- reusable Daily Line data/motion components;
- cached owned/generated/stock still imagery;
- light pan/zoom/parallax/masks;
- charts/cards/tickers;
- captions;
- optional voice/TTS;
- music/SFX where rights permit.

Generative video remains an optional later asset class used when performance evidence justifies the added cost/complexity.

### 5. Branding is integrated into the hook/body

A parameterized `DailyLineBrandSting` supports `micro`, `opener`, `transition`, and `outro` modes.

The default short-form policy is hook-first with subtle frame-0 brand presence and a micro sting after/within the initial hook, rather than a multi-second blocking logo opener. Brand placement/timing remains experimentable creative data.

### 6. Rendering and publication are separate

A successful MP4 render does not authorize an external post. V-series architecture produces a passed `VideoPublicationPackage`; future A-18 architecture governs platform-side effects, retries, deduplication, receipts, edits/deletes, and correction workflows.

## Alternatives considered

### Manual editing

**Pros:** maximum per-video creative control.  
**Cons:** high labor, weak scalability, inconsistent provenance, difficult experimentation.

Decision: retain as an exceptional/special-project option, not the primary architecture.

### Proprietary AI video for the full pipeline

**Pros:** potentially high visual novelty and low editing labor.  
**Cons:** higher variable cost, provider lock-in, visual/factual drift risk, weak deterministic repeatability, harder template-level experimentation, unnecessary for data-led content.

Decision: not the default renderer. May be plugged into the asset layer later.

### Pre-rendered motion templates only

**Pros:** predictable visuals.  
**Cons:** limited dynamic data flexibility, difficult multi-sport variation, brittle text/number handling.

Decision: reusable motion concepts should be code components instead.

### FFmpeg/custom rendering only

**Pros:** strong media-processing primitives and low-level control.  
**Cons:** more engineering effort for complex responsive typography/layout/component authoring.

Decision: FFmpeg/media tooling may support probing/transcoding, but not serve as the primary composition authoring model in V1.

### Put video generation in each sport repo

**Pros:** sport data is nearby.  
**Cons:** duplicates brand/render/publication infrastructure, fragments experiments, increases drift, violates the desired cross-sport automation separation.

Decision: rejected. Sport repositories provide publishable facts/claims; TDLA/DLVE owns generic presentation/render coordination.

## Consequences

### Positive

- one renderer/template library supports every sport;
- fact authority remains in the sport systems;
- every script/video can retain provenance;
- videos can be generated cheaply from stills + motion;
- brand changes are centralized/versioned;
- creative variables are measurable;
- provider swaps do not require rewriting sport pipelines;
- future adaptive creative selection can operate on presentation metadata only.

### Costs/tradeoffs

- repository becomes polyglot (Python control plane + TypeScript/React renderer);
- cross-language schemas require disciplined versioning/testing;
- programmatic templates require initial engineering effort;
- generated/stock asset rights/provenance become first-class data;
- visual design quality depends on a deliberately built brand component library;
- platform publication still requires later A-18 architecture.

## Compatibility / migration impact

No existing production automation is changed because no TDLA production implementation is authoritative yet.

Future Daily-MLB/NFL/NCAAF integrations do not need to embed Remotion. They must emit or adapt to certified publishable fact contracts.

If Remotion is replaced later:

- canonical story/creative/fact/publication IDs remain unchanged;
- existing render manifests retain the renderer/release actually used;
- a new renderer adapter must pass the same fixture/QC contract tests;
- visual output changes create new creative/render releases rather than rewriting history.

## Security / operational impact

- image/TTS/stock/platform credentials are logical secret references only and remain under A-20;
- generated/stock/licensed assets require provenance/rights policy;
- external posting remains an A-18 side effect;
- render retries must use future A-11 semantics;
- resource/provider budgets remain A-15 authority;
- adaptive policy changes remain A-24 authority.

## Validation required

Before production use, implementation must prove:

1. cross-language contract parity;
2. protected numeric/claim validation;
3. no raw sport-reasoning path in the renderer/planner;
4. exact asset hash/provenance capture;
5. one parameterized brand sting supports multiple modes;
6. `single_pick_v1` renders from synthetic fixtures;
7. no-image/no-voice fallbacks work when allowed;
8. visual/safe-zone/text-overflow QC works;
9. publication package cannot be approved on QC failure;
10. real sport shadow rendering preserves source meaning before publication authority.

## Related architecture

- A-0/A-1 ownership boundary
- A-5 Sport Automation Adapter
- A-6 Pipeline/Stage contracts
- A-10 Worker/Execution Backend
- A-11 Retry/Timeout/Idempotency (future integration)
- A-13 Persistence/Audit (future integration)
- A-15 Resource Budgeting (future integration)
- A-18 Publication/Distribution (future integration)
- A-20 Security/Service Identity (future integration)
- A-24 Adaptive Automation (future integration)
- `docs/video/V00_SOCIAL_VIDEO_ENGINE_ARCHITECTURE_V1.md`
- `docs/video/V01_VIDEO_JOB_AND_FACT_CONTRACTS_V1.md`
- `docs/video/V02_BRAND_MOTION_SYSTEM_V1.md`
- `docs/video/V03_TEMPLATE_LIBRARY_V1.md`
- `docs/video/V04_RENDER_ASSET_QC_HANDOFF_V1.md`
- `docs/video/V05_PERFORMANCE_EXPERIMENTATION_V1.md`

## Supersession

Supersedes: none.  
Superseded by: none.