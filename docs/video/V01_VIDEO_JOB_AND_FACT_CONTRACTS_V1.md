# V-1 — Video Job and Fact Contracts V1

Status: **ARCHITECTURE BASELINE**  
Date: 2026-09-08

## 1. Purpose

This document defines the canonical semantic contracts between sport/content authorities, the Daily Line video planner, asset/voice/caption stages, the renderer, QC, and the future publication subsystem.

The wire format is versioned JSON. Canonical schemas should be expressed in JSON Schema and mechanically validated by both Python and TypeScript implementations.

## 2. Contract chain

```text
PublishableFactPackage
        -> ContentCandidate
        -> CreativePlan
        -> ScriptPackage
        -> FactIntegrityReport
        -> AssetPlan / AssetManifest
        -> VoicePackage / CaptionPackage
        -> VideoRenderSpec
        -> RenderManifest
        -> VideoQcReport
        -> VideoPublicationPackage
```

No stage may silently enrich a contract with new sport truth.

## 3. `PublishableFactPackage`

Minimum semantic fields:

```text
schema_version
package_id
producer
producer_release
source_run_refs[]
created_at
valid_from
expires_at
sport
scope_ref
content_authority
recommendation_state
allowed_story_families[]
approved_claims[]
approved_facts[]
approved_explanations[]
presentation_hints
asset_restrictions
disclaimer_profile_ref
embargo_policy
provenance_manifest_ref
package_digest
```

### 3.1 `ApprovedFact`

```text
fact_id
kind
label
raw_value
formatted_value
unit
precision_policy
source_ref
source_field_ref
as_of
valid_until
sensitivity
rendering_constraints
```

Examples of `kind`:

- probability
- odds
- point_spread
- total
- line_movement
- weather
- record
- ranking
- score
- model_metric
- generic_text_fact

The `kind` does not authorize TDLA to interpret sport meaning.

### 3.2 Protected numeric semantics

A fact may provide both `raw_value` and `formatted_value`. The script/render layer should prefer the approved formatted representation. A transformation that changes mathematical meaning is prohibited.

Allowed formatting examples only when declared:

- decimal probability -> percentage;
- standardized decimal precision;
- temperature unit conversion if explicitly enabled by policy;
- odds display style normalization when source semantics are preserved.

### 3.3 `ApprovedClaim`

```text
claim_id
claim_type
text
fact_refs[]
source_ref
allowed_paraphrase: boolean
must_render_verbatim: boolean
valid_until
sensitivity
```

### 3.4 `ApprovedExplanation`

This exists specifically so sport-specific causal or matchup interpretation remains sport-owned.

```text
explanation_id
headline
body
supporting_fact_refs[]
reason_code
priority
allowed_paraphrase
valid_until
```

Example conceptually:

> "The model favors Team A because the certified sport pipeline identifies a pass-rush/protection mismatch."

DLVE may present that explanation only if it arrives through this contract. DLVE may not infer it from raw sack/EPA/pressure fields.

## 4. `ContentCandidate`

A candidate is a generic publication opportunity over one or more publishable packages.

```text
schema_version
candidate_id
fact_package_refs[]
primary_scope_ref
sport
story_family_eligibility[]
content_priority_hint
urgency
expires_at
recommended_duration_band
required_claim_refs[]
optional_claim_refs[]
allowed_cta_profiles[]
required_disclaimer_profile_ref
candidate_digest
```

`content_priority_hint` may be supplied by the authoritative producer. DLVE may combine it with generic publication factors, but it may not compute a new betting thesis.

## 5. `CreativePlan`

```text
schema_version
video_story_id
creative_variant_id
template_ref
render_profile_ref
hook_variant_ref
brand_sting_mode
brand_sting_placement
caption_style_ref
voice_profile_ref
cta_profile_ref
scene_plan[]
asset_policy_ref
music_policy_ref
disclaimer_profile_ref
experiment_refs[]
creative_plan_digest
```

### 5.1 `ScenePlanItem`

```text
scene_id
scene_type
position
claim_refs[]
fact_refs[]
explanation_refs[]
asset_slots[]
duration_policy
transition_in_ref
transition_out_ref
layout_variant
```

A scene cannot reference content that is not available in an approved package.

## 6. `ScriptPackage`

```text
schema_version
script_id
video_story_id
creative_variant_id
segments[]
total_word_count
estimated_duration_ms
language
script_generator_ref
prompt_template_ref
model_ref
created_at
script_digest
```

### 6.1 `ScriptSegment`

```text
segment_id
scene_id
text
segment_type
claim_refs[]
fact_refs[]
explanation_refs[]
protected_tokens[]
allow_paraphrase
```

`segment_type` examples:

- hook
- narration
- transition
- pick_reveal
- CTA
- disclaimer
- brand

A factual segment without fact/claim/explanation traceability is invalid unless it is explicitly classified as non-factual brand/transition/CTA language.

## 7. Protected tokens

A `ProtectedToken` prevents numeric/entity drift during script transformation.

```text
token_id
source_ref
source_value
render_value
normalization_rule_ref
match_policy
```

Examples:

- `61.8%`
- `-2.5`
- `18 mph`
- `+120`
- exact team abbreviation when canonical presentation requires it

The fact integrity gate verifies that protected tokens used in a script match the approved render values.

## 8. `FactIntegrityReport`

```text
schema_version
report_id
script_id
status
checks[]
unsupported_claims[]
missing_required_claims[]
protected_token_mismatches[]
expired_fact_refs[]
validator_release
validated_at
report_digest
```

Allowed terminal status:

- `PASS`
- `FAIL`
- `REVIEW_REQUIRED`

Production auto-publication requires `PASS` unless future A-19 policy explicitly allows a supervised review path.

## 9. `AssetPlan`

```text
schema_version
asset_plan_id
creative_variant_id
slots[]
provider_policy_ref
budget_policy_ref
asset_plan_digest
```

Each slot declares:

```text
slot_id
scene_id
asset_role
allowed_source_classes[]
query_or_prompt_intent
subject_policy
aspect_ratio
resolution_floor
reuse_allowed
fallback_chain[]
```

The prompt intent is not sufficient provenance for a generated asset; the resolved manifest records the exact generation request/provider/model/output hash.

## 10. `AssetManifest`

```text
schema_version
asset_manifest_id
assets[]
created_at
manifest_digest
```

### 10.1 `ResolvedAsset`

```text
asset_id
slot_id
source_class
uri_or_artifact_ref
content_hash
media_type
width
height
duration_ms
origin_provider_ref
origin_record_ref
license_or_rights_ref
allowed_platforms[]
expiry
attribution_requirement
generated_metadata
policy_status
```

For generated assets, `generated_metadata` should retain:

```text
provider_ref
model_ref
prompt_template_ref
resolved_prompt_digest
seed_or_provider_generation_ref if available
generation_timestamp
safety_or_policy_receipt_ref if available
```

No credentials or private tokens enter this manifest.

## 11. `VoicePackage`

```text
schema_version
voice_package_id
script_id
voice_profile_ref
provider_ref
model_ref
audio_asset_ref
content_hash
duration_ms
segment_timing_refs[]
created_at
voice_digest
```

Voice is optional. A no-voice composition is valid when its template/render policy permits it.

## 12. `CaptionPackage`

Canonical caption cue shape:

```text
cue_id
text
start_ms
end_ms
timestamp_ms
confidence
script_segment_ref
style_hint
```

The Remotion adapter may map this to its caption type. The canonical package remains provider/renderer-neutral.

## 13. `VideoRenderSpec`

This is the complete immutable input to the renderer.

```text
schema_version
render_spec_id
video_story_id
creative_variant_id
template_ref
brand_release_ref
component_release_ref
renderer_adapter_ref
renderer_release_ref
render_profile
scene_specs[]
asset_manifest_ref
script_ref
voice_package_ref
caption_package_ref
music_asset_ref
sfx_asset_refs[]
disclaimer_ref
safe_zone_profile_ref
created_at
render_spec_digest
```

### 13.1 `RenderProfile`

```text
profile_id
width
height
fps
pixel_aspect_ratio
container
codec_profile_ref
audio_profile_ref
max_duration_ms
min_duration_ms
safe_zone_profile_ref
platform_intent[]
```

Initial profile:

```text
profile_id: vertical_social_v1
width: 1080
height: 1920
fps: 30
aspect: 9:16
```

Exact encoding settings remain implementation policy and may be tuned without changing sport meaning.

## 14. `RenderManifest`

```text
schema_version
render_manifest_id
render_spec_id
render_attempt_ref
renderer_adapter_ref
renderer_release_ref
artifact_ref
content_hash
container
codec
width
height
fps
duration_ms
file_size_bytes
render_started_at
render_finished_at
probe_summary
manifest_digest
```

`render_attempt_ref` must eventually bind to A-11/A-10 execution identity. The V-series does not create a competing retry model.

## 15. `VideoQcReport`

```text
schema_version
qc_report_id
render_manifest_ref
status
gate_results[]
validated_at
validator_release
report_digest
```

Required gate classes:

- contract
- fact
- asset_rights
- asset_integrity
- layout
- safe_zone
- text_overflow
- captions
- audio
- render_probe
- duration_profile
- disclaimer
- metadata
- publication_package

## 16. `VideoPublicationPackage`

```text
schema_version
publication_package_id
video_story_id
creative_variant_id
render_artifact_ref
render_manifest_ref
qc_report_ref
platform_intents[]
post_copy
thumbnail_ref
metadata
disclaimer_profile_ref
content_valid_until
source_fact_package_refs[]
experiment_refs[]
created_at
package_digest
```

### 16.1 `PlatformIntent`

```text
platform
target_account_ref
publish_mode
scheduled_window
caption_or_description_variant_ref
hashtag_profile_ref
thumbnail_policy_ref
external_side_effect_class
```

This is **intent only**. A-18 owns actual posting, edit/delete behavior, external receipts, and idempotency.

## 17. Performance contracts

### `PlatformMetricSnapshot`

```text
schema_version
snapshot_id
platform
external_post_ref
publication_package_ref
observed_at
source_metrics
normalized_metrics
adapter_ref
adapter_release
snapshot_digest
```

### `NormalizedMetric`

```text
metric_name
value
unit
normalization_version
source_metric_refs[]
semantic_notes
```

Do not assume two platforms' similarly named metrics are identical.

## 18. Example `VideoRenderSpec` shape

Illustrative only:

```json
{
  "schema_version": "video-render-spec.v1",
  "video_story_id": "story_...",
  "creative_variant_id": "creative_...",
  "template_ref": "single_pick_v1@1.0.0",
  "brand_release_ref": "daily-line-brand@1.0.0",
  "render_profile": {
    "profile_id": "vertical_social_v1",
    "width": 1080,
    "height": 1920,
    "fps": 30
  },
  "scene_specs": [
    {"scene_id": "hook", "scene_type": "hook"},
    {"scene_id": "reason-1", "scene_type": "reason"},
    {"scene_id": "model", "scene_type": "model_probability"},
    {"scene_id": "pick", "scene_type": "pick_reveal"},
    {"scene_id": "outro", "scene_type": "outro"}
  ]
}
```

The actual production JSON must include complete references/digests and must never rely on an LLM to fill omitted authoritative fields during render.

## 19. Versioning and compatibility

- breaking semantic changes require a new schema major version;
- additive optional fields may use compatible minor evolution where policy permits;
- unknown required enum values fail closed;
- producers and consumers declare supported versions;
- completed manifests retain the schema versions actually used;
- adapters may translate between compatible versions only through explicit tested transforms.

## 20. Contract validation requirements

Before implementation certification, tests must include:

- valid fixture for every story family;
- invalid/missing fact refs;
- numeric token mutation;
- expired facts;
- missing asset rights metadata;
- invalid render profile;
- unsupported template version;
- duplicate IDs;
- unknown required enum;
- missing disclaimer profile when required;
- platform intent with no passed QC;
- metric snapshot tied to wrong publication package;
- cross-language Python/TypeScript fixture parity.