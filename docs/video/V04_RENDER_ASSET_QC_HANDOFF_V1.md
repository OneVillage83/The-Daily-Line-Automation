# V-4 — Rendering, Asset Provenance, QC, and Publication Handoff V1

Status: **ARCHITECTURE BASELINE**  
Date: 2026-09-08

## 1. Purpose

V-4 defines how a resolved creative plan becomes a reproducible video artifact and then a validated publication package. It deliberately stops before the external social-platform side effect; A-18 will own actual posting/retry/edit/delete/receipt semantics.

## 2. Render stages

```text
CreativePlan
  -> ScriptPackage
  -> FactIntegrityReport PASS
  -> AssetPlan
  -> AssetManifest
  -> VoicePackage (optional)
  -> CaptionPackage
  -> VideoRenderSpec
  -> Render
  -> RenderManifest
  -> VideoQcReport
  -> VideoPublicationPackage
  -> A-18 boundary
```

No authoritative render may fetch or reinterpret sport truth after `VideoRenderSpec` is frozen.

## 3. Initial renderer

The first renderer is Remotion.

### Remotion responsibilities

- consume the immutable render spec;
- map canonical scenes to React/Remotion compositions;
- compose shared brand/data components;
- load only resolved assets;
- render deterministic timeline animation from frame/time;
- emit the requested media artifact;
- emit render metadata/probe information.

### Remotion does not own

- story identity;
- fact validity;
- sport meaning;
- external publication identity;
- logical retry/idempotency semantics;
- canonical asset rights decisions.

A future renderer may replace Remotion behind the same `VideoRenderSpec`/artifact manifest boundary.

## 4. Renderer adapter

Conceptual interface:

```text
capabilities()
validate_render_spec(spec)
prepare(spec)
render(spec, execution_context)
probe(output)
collect_manifest(output)
```

The actual invocation may be local Node, Docker, a dedicated render worker, or another A-10 backend. Backend-native IDs are provenance only.

## 5. Asset resolution

A render spec references only resolved assets.

An authoritative render may not say:

```text
"find a baseball stadium image"
```

It must say, conceptually:

```text
asset_id = asset_...
content_hash = sha256:...
artifact_ref = ...
rights_policy = ...
```

This prevents a retry/replay from silently receiving a different asset.

## 6. Asset source classes

### `owned`
Daily Line / One Village-owned artwork, audio, templates, photos, or motion.

### `licensed`
Third-party asset with explicit license/usage metadata.

### `stock`
Stock provider asset with provider record and usage terms reference.

### `generated`
AI-generated image/audio/visual asset with provider/model/prompt provenance.

### `public_domain`
Asset whose usage basis is recorded and validated.

### `platform_supplied`
Platform-native music/effects or other media whose permitted use may be restricted to that platform.

### `data_visualization`
Renderer-created graphics from approved facts, such as charts/cards/gauges.

## 7. Asset provenance requirements

Every production asset requires:

- stable asset ID;
- content hash;
- source class;
- origin/provider ref;
- license/rights policy ref;
- allowed target platforms or equivalent policy;
- attribution requirement if any;
- expiration/revocation state if applicable;
- generation metadata if generated;
- dimensions/duration/media type;
- policy validation status.

Unknown rights status fails closed for automatic publication.

## 8. Generated-image policy

Generated still imagery is a cost-effective primary visual option because Remotion can add motion through pan/scale/parallax/masks/data overlays.

### Preferred generated subjects

- generic sports atmospheres;
- stadium/field/court/diamond environments;
- equipment/macros;
- weather scenes;
- data/analytics abstractions;
- generic crowd/tunnel lighting;
- city/location atmosphere when it does not imply a false documentary capture.

### Restricted-by-default creative behavior

The automatic asset planner should not fabricate a depiction that could reasonably be interpreted as an authentic photograph/video of a specific real athlete/event unless an explicit rights/content policy authorizes it.

The planner also should not add official logos, trademarks, uniforms, or league marks merely because a prompt generator thinks they improve realism.

## 9. Generated-asset caching

Generated assets should enter a reusable library when policy permits.

Cache lookup dimensions may include:

- sport;
- visual role;
- mood;
- aspect ratio;
- background/foreground utility;
- rights/policy class;
- prompt family;
- generation model/version;
- content hash.

A new generation call should occur only when the creative plan requires something not satisfied by the approved library/fallback chain.

## 10. Asset fallback chain

Each asset slot defines an ordered fallback chain, for example:

```text
owned branded visual
  -> approved cached generated still
  -> approved stock still
  -> data-only background
  -> fail candidate if imagery is semantically required
```

An unavailable asset provider must not block a video that can validly render as a data-led composition.

## 11. Voice/TTS

Voice providers are adapters.

The voice stage receives the approved `ScriptPackage`, not raw facts.

Required voice provenance:

- voice profile ref;
- provider/model ref;
- source script digest;
- generated audio hash;
- segment/timing mapping;
- usage/license policy where applicable.

If the provider fails and the template allows caption-led content, the planner may produce a new explicit creative variant with `voice=none`. It may not silently remove voice from the same immutable render spec.

## 12. Captions

Captions are structured artifacts.

Required checks:

- text matches approved script meaning;
- protected values are correct;
- cues do not overlap illegally under the selected caption policy;
- cue timing falls within video duration;
- caption layout fits the profile safe zone;
- the caption style version is recorded.

Caption generation/transcription is not allowed to become a new source of sport truth.

## 13. Audio/music

Music and SFX require asset provenance exactly like imagery.

An audio profile declares:

- target speech/music balance policy;
- peak/clipping policy;
- optional loudness target policy;
- ducking policy;
- fade policy;
- mono/stereo/channel requirements;
- platform-specific restrictions where applicable.

Exact numeric mix targets are configuration/versioned implementation policy, not hard-coded architecture truth.

## 14. Render reproducibility

A production render must pin:

- render spec digest;
- renderer adapter release;
- Remotion/app release or future renderer release;
- Node/runtime/container image digest where authoritative;
- template release;
- brand release;
- component release;
- all asset hashes;
- script digest;
- caption digest;
- voice/audio hashes;
- render profile;
- execution identity/provenance.

The goal is reproducibility/auditability. If an external model/provider cannot guarantee byte-identical regeneration, the exact generated asset is stored and reused by hash rather than regenerated during replay.

## 15. Render output storage

Object storage is the intended artifact abstraction.

Conceptual namespace:

```text
video/
  stories/{video_story_id}/
    variants/{creative_variant_id}/
      specs/{render_spec_digest}.json
      renders/{render_artifact_hash}.mp4
      manifests/{render_manifest_digest}.json
      qc/{qc_report_digest}.json
      publication/{publication_package_digest}.json
```

This is a logical organization, not A-13 database/retention authority.

## 16. QC gates

### Gate 1 — schema/contract

Checks all referenced schemas/versions/required fields.

### Gate 2 — fact integrity

Requires passed `FactIntegrityReport` and verifies the render spec references the same immutable script/facts.

### Gate 3 — asset integrity

Checks every asset exists and matches its recorded content hash/media metadata.

### Gate 4 — rights/policy

Checks target platform intent is allowed for every asset and required attribution/disclosure metadata exists.

### Gate 5 — layout/safe zone

Checks critical elements remain within the appropriate safe zones.

### Gate 6 — text overflow

Checks titles, captions, team labels, numbers, CTAs, and disclaimers do not clip or fall below allowed readability thresholds.

### Gate 7 — caption integrity

Checks caption presence/timing/text/layout according to template/profile policy.

### Gate 8 — audio

Checks decode, duration alignment, clipping/missing tracks, and configured mix-profile conditions.

### Gate 9 — render probe

Checks:

- media decodes;
- expected dimensions;
- fps/profile compatibility;
- duration bounds;
- non-empty file;
- expected audio/video streams;
- selected frame probes do not indicate missing-asset/blank-frame failure.

### Gate 10 — metadata/disclaimer

Checks required brand, CTA, disclosure, disclaimer, expiration, and source metadata policy.

### Gate 11 — publication package

Ensures the final package references exactly the passed artifact/QC/facts/creative variant.

## 17. Visual regression testing

For implementation testing, important compositions should retain approved golden stills or image-diff baselines at representative frames.

Examples for `single_pick_v1`:

- first hook frame;
- micro-sting peak frame;
- stat/reason frame;
- probability/comparison frame;
- pick reveal;
- outro.

Golden tests detect accidental layout/brand regressions but cannot validate sport truth by themselves.

## 18. Render smoke tests

CI should eventually run small/low-cost render tests using fixtures:

- one short complete video;
- one no-image fallback;
- one no-voice fallback;
- one long-text stress case;
- one disclaimer case;
- one intentional missing asset that must fail;
- one protected-token mismatch that must fail before render.

Full production-resolution rendering in every PR is not required if an equivalent tiered test strategy is documented.

## 19. Publication package handoff

`VideoPublicationPackage` is the only normal V-series output permitted to approach the A-18 publication subsystem.

It carries:

- exact media artifact ref/hash;
- target account/platform intent;
- post copy/metadata;
- thumbnail/poster;
- creative/fact provenance;
- required disclosures/disclaimers;
- expiry/embargo policy;
- side-effect class;
- QC PASS reference.

A platform worker may not construct its own replacement caption/pick/stat from raw data.

## 20. A-18 boundary

Deferred to A-18:

- account authorization;
- platform API adapter contracts;
- rate limits;
- create/update/delete semantics;
- external idempotency keys;
- duplicate-post prevention;
- post receipts;
- retry/reconciliation after unknown acknowledgement;
- scheduled publishing semantics;
- platform-native media processing states;
- comment/pin/community actions;
- removal/correction workflows.

The video architecture intentionally does not guess these semantics before A-18.

## 21. Corrections and stale content

A video package includes content validity/expiry.

If a sport fact package is superseded before publication:

- the old publication package becomes ineligible;
- a fresh creative/render may be required depending on the changed claim;
- publication may not proceed merely because the old video already rendered.

If a correction occurs after publication, A-18/A-12/A-19 must eventually define correction/removal operator policy. Historical provenance remains retained.

## 22. Render failure and retry

V-4 does not create its own retry semantics.

A failed render is an execution failure under the appropriate TDLA stage. A-11 determines when a new physical attempt is legal and how logical idempotency is preserved. A render retry reuses the same immutable render spec unless an explicit replan/reprocess creates a new variant/spec.

## 23. Cost controls

Every provider-consuming stage should emit generic cost/resource evidence for future A-15 budgeting:

- image generations requested/completed;
- TTS characters/seconds;
- stock asset API calls/licenses;
- render CPU/GPU duration;
- storage bytes;
- optional generative-video seconds.

Creative code must not silently make high-cost provider calls outside an approved asset/resource policy.

## 24. Production acceptance criteria

A V-4 implementation is production-ready only when:

- renderer consumes immutable V-1 render specs;
- no sport facts are fetched during authoritative render;
- all assets are hash/provenance bound;
- generated assets are stored/reused rather than silently regenerated;
- required QC gates block invalid outputs;
- publication packages require QC PASS;
- renderer/backend IDs remain provenance only;
- publication side effects are still gated by A-18;
- replay/retry semantics defer to certified A-11/A-14 authority.