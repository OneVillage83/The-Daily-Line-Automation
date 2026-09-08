# V-0 — The Daily Line Social Video Engine Architecture V1

Status: **ARCHITECTURE BASELINE**  
Date: 2026-09-08  
Subsystem name: **DLVE — Daily Line Video Engine**

## 1. Mission

DLVE converts certified, publishable Daily Line outputs into branded audiovisual artifacts for TikTok, Instagram Reels, YouTube Shorts, longer YouTube content, and future distribution surfaces.

DLVE is a presentation/rendering subsystem inside TDLA. It is not a sports-analysis repository and is not permitted to create sport truth.

## 2. Non-negotiable principles

1. **Facts before narrative.** Every sport-specific claim must trace to an approved fact/explanation record.
2. **Presentation is separable from intelligence.** Video templates may change without changing prediction/model truth.
3. **No blocking logo intro by default.** Short-form content begins with a hook; branding is integrated rather than inserted as dead time.
4. **Reusable components over one-off edits.** Every production video is generated from versioned contracts and reusable components/templates.
5. **Renderer independence at the system boundary.** Remotion is the first renderer, not canonical identity authority.
6. **Asset provenance is mandatory.** Generated, licensed, stock, owned, and user-supplied assets retain origin/rights metadata.
7. **Rendered does not equal publishable.** Fact, contract, visual, audio, rights, policy, and publication-package QC must pass.
8. **Performance learning is evidence, not automatic authority.** Metrics may recommend creative policy changes; A-24 must govern any production self-optimization.
9. **External posting is a side effect.** V-series architecture produces a publication package; A-18 will govern actual publish/retry/idempotency semantics.
10. **Immutable release references.** Production artifacts identify exact template, brand, render, asset, prompt/model, and source-fact versions.

## 3. Ownership boundary

### Sport repositories own

- canonical event/team/player identities;
- predictions and probabilities;
- Recommendation Gate results;
- sport-specific statistical interpretation;
- reasons why a matchup/weather/injury/line condition matters;
- sport-specific report prose or explanation claims when required;
- settlement and post-event evaluation meaning;
- correctness of `PublishableFactPackage` sport claims.

### Daily-Data-Core owns

Shared sport-agnostic fact/provider infrastructure under its certified contract. DLVE may consume DDC-backed facts only when they have entered an approved publishable package or a separately authorized non-sport content source.

### DLVE/TDLA may own

- candidate orchestration and generic content prioritization over already publishable items;
- creative-format selection;
- script compression/rephrasing that preserves approved meaning;
- scene planning;
- asset selection/generation orchestration;
- brand components and motion language;
- voice/TTS/caption generation;
- rendering;
- render/QC manifests;
- publication-package assembly;
- performance measurement and creative experiment evidence;
- generic creative-policy configuration.

### DLVE/TDLA must not

- calculate a betting edge from raw odds/model outputs;
- decide that weather, injuries, rest, travel, a player, or a matchup causes an advantage unless an authoritative input explicitly says so;
- invent a confidence percentage, line, market price, statistical value, record, trend, quote, injury status, or source;
- silently round/change values where that changes meaning;
- convert a `PASS`, `AVOID`, `NO_PLAY`, or other recommendation state into another state;
- publish externally without the future A-18 gate.

## 4. System topology

```text
Daily-MLB / Daily-NFL / Daily-NCAAF / future sport authority
                        |
                        | versioned publishable artifacts
                        v
               PublishableFactPackage
                        |
                        v
              Content Candidate Intake
                        |
                        v
         Generic Story/Template Eligibility
                        |
                        v
                 Creative Planner
          (format, hook style, scene order)
                        |
                        v
                 Script Transformer
          (fact-bound presentation only)
                        |
                        v
                 Fact Integrity Gate
                        |
              fail closed on mismatch
                        v
                   Asset Planner
             /          |           \
            /           |            \
   owned/licensed   generated AI      stock
            \           |            /
             \          |           /
                 Asset Manifest
                        |
              +---------+----------+
              |                    |
              v                    v
          Voice/TTS             Captions
              |                    |
              +---------+----------+
                        v
                VideoRenderSpec
                        |
                        v
                Renderer Adapter
                  (Remotion V1)
                        |
                        v
                 Render Artifact
                        |
                        v
                    QC Gates
                        |
                        v
              VideoPublicationPackage
                        |
                        v
              A-18 Publication Boundary
                        |
                        v
         TikTok / Reels / Shorts / YouTube
                        |
                        v
              Performance Adapters
                        |
                        v
            Normalized Metric Evidence
                        |
                        v
       Experiment Analysis / Recommendations
                        |
                        v
          A-24 adaptive policy boundary
```

## 5. Proposed repository layout

Implementation is architecture-first and should eventually follow this shape unless superseded by an ADR:

```text
The-Daily-Line-Automation/
├── apps/
│   └── video-renderer/
│       ├── src/
│       │   ├── compositions/
│       │   ├── scenes/
│       │   ├── components/
│       │   ├── captions/
│       │   ├── audio/
│       │   ├── brand/
│       │   ├── adapters/
│       │   └── Root.tsx
│       └── public/
│           ├── branding/
│           ├── music/
│           ├── sfx/
│           └── local-assets/
│
├── packages/
│   ├── video-contracts/
│   │   ├── schemas/
│   │   ├── fixtures/
│   │   └── generated-types/
│   ├── video-brand/
│   ├── video-components/
│   └── video-templates/
│
├── services/
│   └── video-planner/
│       ├── candidate_intake/
│       ├── script/
│       ├── asset_planning/
│       ├── qc/
│       └── metrics/
│
├── tests/
│   └── video/
│
└── docs/video/
```

The actual TDLA orchestrator may invoke the planner/renderer as A-6 stages through A-10 workers. The directory layout does not define runtime authority.

## 6. Canonical cross-language contract strategy

The V1 wire boundary is JSON with explicit schema versions.

Canonical schemas should live as versioned JSON Schema documents. Python and TypeScript validators/types must be generated or mechanically checked against those schemas so the repository does not acquire separate meanings in Pydantic and Zod.

Remotion composition props may use Zod internally, but they are an adapter projection of a canonical `VideoRenderSpec`, not the canonical external contract itself.

## 7. Primary identities

The V-series defines semantic video identities without preempting A-11/A-13 persistence mechanics.

### `VideoStoryId`

One logical publishable story derived from one or more explicitly referenced publishable fact packages.

It is independent of:

- render attempt;
- platform;
- output file name;
- external post ID;
- Remotion composition ID.

### `CreativeVariantId`

One exact creative treatment of a story, including at minimum:

- template version;
- hook variant;
- scene order;
- brand-sting mode/placement;
- caption style;
- voice profile;
- asset-plan version;
- CTA variant;
- target render profile.

### `VideoRenderSpecId`

Identity/digest of the complete immutable render instruction after all assets, timings, narration, captions, template versions, and render profile are resolved.

### `RenderArtifactId`

Content-addressed identity for a completed encoded output plus manifest.

### `VideoPublicationPackageId`

Identity for the exact artifact + metadata + platform intent package handed to A-18.

### External platform post IDs

TikTok/Instagram/YouTube IDs are external provenance only. They never replace canonical Daily Line story, creative, render, or publication-package identity.

## 8. Required provenance chain

A published video must eventually allow reconstruction of:

```text
platform post
  -> publication package
  -> rendered artifact
  -> render spec
  -> creative variant
  -> script + captions + voice + asset manifest
  -> fact integrity report
  -> publishable fact package(s)
  -> exact sport run/output manifest(s)
  -> immutable sport/model/config/release provenance
```

No layer may silently sever this chain.

## 9. Content candidate model

Sport systems should not hand DLVE raw unbounded state and ask it to discover a betting thesis. Instead they should expose a publishable candidate package containing approved statements and optional presentation hints.

A candidate may declare:

- eligible story families;
- canonical headline topic;
- approved claims;
- approved numeric facts;
- approved explanation/reason claims;
- recommendation state;
- event start/cutoff timing;
- priority/timeliness hints;
- embargo/expiry timestamp;
- allowed CTAs;
- sensitivity/compliance flags;
- required disclaimer profile;
- asset restrictions.

DLVE may rank candidates using generic publication factors and historical creative evidence, but may not create sport-specific causal meaning to improve the rank.

## 10. Narrative transformation contract

The script transformer receives only approved facts/claims plus presentation policy.

Every narrative sentence/segment must be either:

1. a near-verbatim rendering of an approved claim;
2. a meaning-preserving paraphrase linked to one or more approved claim IDs;
3. non-factual brand/transition/CTA language allowed by policy.

Numeric tokens that originate from facts are protected values. Transformations must not change them except through an explicitly approved formatting policy (for example, `0.618` -> `61.8%` when the source schema declares the conversion).

Unsupported sports claims fail the fact gate.

## 11. Scene architecture

A video is a declarative scene list, not a hand-edited timeline.

Core scene families:

- `hook`
- `matchup`
- `stat`
- `comparison`
- `line_movement`
- `weather`
- `model_probability`
- `reason`
- `pick_reveal`
- `results`
- `data_story`
- `brand_transition`
- `outro`

A template constrains which scene types may occur and in what broad order. The creative planner fills a template using approved content.

## 12. Brand architecture

The Daily Line brand should be implemented as reusable components rather than baked assets.

Core components:

- `DailyLineLogo`
- `DailyLineWatermark`
- `DailyLineBrandSting`
- `DailyLineOutro`
- `SportBadge`
- `DataGridBackground`
- `OddsTicker`
- `StatCard`
- `ProbabilityMeter`
- `LineMovementChart`
- `PickReveal`
- `CaptionLayer`

The `DailyLineBrandSting` is one parameterized component supporting `micro`, `opener`, `transition`, and `outro` modes.

## 13. Rendering model

### Initial runtime

Remotion + React + TypeScript.

### Requirements

- all deterministic timeline motion is frame-driven;
- no CSS/browser animation semantics that cannot be reproduced reliably in render;
- all externally required assets are resolved before authoritative rendering;
- render specs pin composition/template/brand versions;
- render specs pin exact assets and hashes;
- render profile declares width, height, fps, codec/container policy, duration limits, safe zones, and audio/caption requirements;
- a renderer may not fetch fresh sports facts during render.

### Initial social master

`vertical_social_v1`

- 1080 x 1920
- 9:16
- 30 fps baseline
- platform-specific export/package policy remains configurable

This is a starting production profile, not a claim that every platform or future video must use the same profile.

## 14. Asset model

Assets are immutable references with provenance.

Supported source classes:

- `owned`
- `licensed`
- `generated`
- `stock`
- `public_domain`
- `platform_supplied`
- `data_visualization`

Every external visual/audio asset must record sufficient rights/origin metadata for policy checks.

Generated visual policy defaults to non-deceptive generic sports imagery, data environments, stadium atmospheres, equipment, weather, and abstract scenes rather than fabricated depictions of identifiable real athletes. Any exception requires an explicit asset policy/approval path.

Generated imagery should be cached and reused when appropriate. Generation is not required for every video.

## 15. Voice and captions

Voice is optional per template/profile. Voice providers are replaceable adapters.

Caption data is structured and timestamped. The implementation may map canonical caption cues to Remotion's caption primitives, but the source transcript/caption manifest remains part of the video provenance.

All voiceover factual segments must retain script/fact linkage.

## 16. QC model

QC has independent gates:

1. contract/schema validation;
2. fact integrity;
3. asset availability/provenance/rights policy;
4. template/layout validation;
5. safe-zone/text-overflow validation;
6. caption timing/presence validation;
7. audio validation;
8. render integrity (duration, dimensions, frame probes, no missing/black/corrupt output);
9. metadata/disclaimer/CTA policy validation;
10. publication-package completeness.

A failure in a required gate blocks publication-package approval.

## 17. Publication boundary

V-series architecture ends at `VideoPublicationPackage`.

That package may include:

- artifact reference/hash;
- platform target intent;
- title/caption/description draft;
- hashtags/tags where configured;
- thumbnail/poster reference;
- disclosure/disclaimer requirements;
- scheduled-window intent;
- creative/fact provenance;
- content expiry;
- external-side-effect policy class.

A-18 must later define external API posting, retries, deduplication, receipts, edits/deletes, and platform-specific side-effect behavior.

## 18. Performance architecture

Performance adapters normalize platform-native metrics into a versioned evidence model while retaining raw/source semantics.

Initial dimensions include:

- platform;
- sport;
- story family;
- template version;
- hook type;
- brand-sting placement;
- video duration;
- caption style;
- voice profile;
- CTA;
- post time/window;
- creative variant.

Initial outcomes include where available:

- impressions/views;
- engaged/qualified views;
- watch time;
- average view duration;
- average percentage viewed;
- completion;
- rewatches/loops;
- likes;
- comments;
- shares;
- saves;
- follows/subscribers attributed where available;
- profile/channel actions;
- link/site actions where available.

Raw platform metrics are not assumed semantically identical. Normalization must preserve source metric names and calculation notes.

## 19. Experiment model

Creative experiments are explicit objects, not undocumented template drift.

An experiment declares:

- hypothesis;
- eligible population;
- variant set;
- allocation method;
- primary metric(s);
- guardrail metric(s);
- minimum evidence rule;
- start/end or stopping policy;
- analysis method/version;
- result/confidence;
- rollout recommendation.

No experiment result silently edits production creative policy.

## 20. Failure/fallback philosophy

The engine should degrade safely instead of inventing content.

Examples:

- image provider unavailable -> use approved cached/stock/data-graphic fallback;
- TTS unavailable -> render caption-led/no-voice variant if template permits;
- non-critical music unavailable -> render without music if policy permits;
- unsupported fact mapping -> fail candidate rather than invent prose;
- render failure -> retry only under future A-11 rules;
- metrics API unavailable -> retain publication provenance and backfill metrics later under appropriate policy;
- platform publication unavailable -> publication package remains valid/unpublished; no blind duplicate post.

## 21. Security and secrets

No provider credentials, social tokens, TTS keys, image-generation keys, storage credentials, or platform secrets belong in video contracts/manifests. Contracts reference logical provider/config IDs only. A-20 will define service-identity/secrets authority.

## 22. Cost/resource architecture

DLVE is designed to minimize expensive generative media calls.

Preferred order:

1. reusable vector/HTML/data graphics;
2. cached owned/generated/stock stills;
3. newly generated still images where needed;
4. licensed/stock motion where useful;
5. generative video only when a template demonstrates enough incremental value to justify cost.

Provider usage/cost should later be governed by A-15 resource budgeting.

## 23. Initial template strategy

The first production reference implementation should be `single_pick_v1` using a fixture package, followed by a real MLB shadow candidate after the relevant MLB outputs are certified for this handoff.

The first shared brand component should be `DailyLineBrandSting` because every subsequent template inherits it.

## 24. Deferred authority

V1 intentionally does not freeze:

- A-11 idempotency-key formula;
- A-13 PostgreSQL DDL;
- A-18 external platform publication semantics;
- A-20 credential/service identity implementation;
- provider choice for TTS/image/stock APIs;
- adaptive policy mutation under A-24;
- final legal/compliance rules for every platform/jurisdiction.

No implementation may fill those gaps silently.

## 25. Architecture acceptance criteria

V-0 is satisfied when implementations can prove:

- sport truth never moves into DLVE;
- every factual narrative claim traces to approved inputs;
- renderer/runtime IDs remain non-canonical;
- the same contract can render multiple sports/templates;
- assets retain provenance;
- render outputs are content-addressed and reproducible from pinned inputs to the extent supported by the renderer/toolchain;
- publication is separated from render success;
- performance evidence can be tied to the exact creative variant;
- optimization cannot bypass governance.