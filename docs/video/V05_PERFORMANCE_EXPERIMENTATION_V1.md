# V-5 — Performance Measurement and Experimentation Architecture V1

Status: **ARCHITECTURE BASELINE**  
Date: 2026-09-08

## 1. Purpose

V-5 defines how The Daily Line learns which creative treatments perform well without allowing social-platform feedback to rewrite sport truth or silently change production policy.

The performance loop operates on **presentation decisions**, not prediction/model authority.

## 2. Goals

The system should eventually answer questions such as:

- Which hook families retain viewers best by sport/story type?
- Does the Daily Line micro sting perform better inside the hook, after the hook, or only at the close?
- Which caption style improves completion and saves/shares?
- Which video durations work best for single-pick vs explainer content?
- Does voiceover outperform caption-led content for a given platform?
- Which asset/background styles improve retention without increasing cost disproportionately?
- Which CTAs generate followers/site actions without reducing completion?
- How does performance differ by platform, sport, time window, and story family?

## 3. Non-goals

The V-5 loop may not:

- change model probabilities;
- change recommendation thresholds;
- decide a sport fact is true because a video performed well;
- reinterpret an injury/weather/matchup;
- suppress losses from a results audit to improve engagement;
- publish unapproved claims;
- self-modify production policy before the A-24 adaptive-automation contract authorizes it.

## 4. Provenance requirement

Every platform post/metric snapshot must be traceable to:

```text
external_post_ref
  -> VideoPublicationPackageId
  -> RenderArtifactId
  -> VideoRenderSpecId
  -> CreativeVariantId
  -> VideoStoryId
  -> source PublishableFactPackage(s)
```

Without that linkage, metrics may be stored for observation but cannot be used as trusted creative experiment evidence.

## 5. Creative feature manifest

Every `CreativeVariant` records a normalized feature vector.

Initial fields:

```text
platform_intent
sport
story_family
template_id
template_version
render_profile
video_duration_ms
hook_family
hook_length_ms
hook_text_density
brand_sting_mode
brand_sting_placement
brand_sting_start_ms
brand_sting_duration_ms
caption_style
voice_present
voice_profile
music_profile
asset_style
asset_source_class_mix
scene_count
scene_order_signature
cta_profile
disclaimer_profile
post_copy_variant
thumbnail_variant
experiment_refs[]
```

These fields are presentation metadata only.

## 6. Raw metric ingestion

Platform adapters should preserve the provider-native response and names where permitted, alongside normalized metrics.

Potential raw metrics include:

- impressions;
- views;
- qualified/engaged views;
- watch time;
- average view duration;
- average percentage viewed;
- completion;
- replay/loop indicators;
- likes;
- comments;
- shares;
- saves;
- follows/subscribers;
- profile/channel visits;
- link clicks/site actions;
- negative feedback where available.

Not every platform exposes every metric, and similarly named metrics may use different definitions.

## 7. Normalization rule

Never assume:

```text
TikTok view == Instagram view == YouTube Shorts view
```

A normalized metric records:

- canonical metric name;
- value/unit;
- source metric(s);
- adapter/version;
- semantic note;
- transformation formula/version where applicable;
- observation window.

Cross-platform comparisons must account for metric-definition differences.

## 8. Metric observation windows

Performance changes over time. Metric snapshots should be captured at explicit windows where platform capability permits, for example:

```text
~1 hour
~6 hours
~24 hours
~72 hours
~7 days
final/settled observation
```

These are scheduling policy examples; exact cadence belongs to the implementation/A-series orchestration policy.

A late metric update does not rewrite earlier snapshots.

## 9. Initial derived creative outcomes

Where source semantics support them, the analysis layer may derive:

```text
view_rate
completion_rate
average_percent_viewed
watch_time_per_impression
share_rate
save_rate
comment_rate
follow_conversion_rate
profile_action_rate
site_action_rate
```

Every derived metric must record its formula/version and required source fields.

## 10. Primary metric by story type

Do not optimize every video to one global metric.

Illustrative policy:

### alerts / line movement
Primary: rapid view/retention and timeliness.

### single pick
Primary: average percentage viewed / completion, with follow/site action as secondary.

### educational data story
Primary: watch time, completion, shares/saves.

### results audit
Primary: completion/trust-oriented engagement; cannot hide negative results to optimize metrics.

Actual primary metrics are versioned experiment policy rather than hard-coded architecture.

## 11. Experiment object

A formal experiment requires:

```text
experiment_id
schema_version
hypothesis
owner
status
eligible_population
exclusions
variant_definitions[]
allocation_method
allocation_seed_or_policy_ref
primary_metrics[]
guardrail_metrics[]
minimum_sample_policy
minimum_runtime_policy
analysis_method_ref
start_at
end_or_stop_policy
result
rollout_recommendation
created_at
closed_at
```

## 12. Variant allocation

The default architecture should support deterministic assignment based on a stable candidate/story identity plus experiment seed, so duplicate orchestration does not randomly change creative assignment.

The exact idempotency/uniqueness mechanism must bind to A-11/A-13 when those sections are certified.

## 13. Experiment examples

### EXP-HOOK-001

Hypothesis: curiosity hook outperforms generic matchup intro for `single_pick_v1`.

Variants:

- A: curiosity
- B: evidence-first

Guardrails:

- no change to facts/pick;
- same template body where practical;
- same duration band;
- no compliance difference.

### EXP-STING-001

Hypothesis: micro branding after the initial hook retains better than a blocking frame-0 sting.

Variants:

- A: watermark frame 0 + micro sting after hook
- B: micro sting immediately at frame 0
- C: watermark only, full brand at outro

### EXP-CAPTION-001

Kinetic captions vs lower-third analytical captions.

### EXP-VOICE-001

Voiceover vs caption-led no-voice creative where template permits.

## 14. Confounding and causal caution

Social-platform distribution is not a clean laboratory environment.

Potential confounders include:

- topic popularity;
- matchup/team popularity;
- posting time;
- platform distribution changes;
- audience growth;
- account history;
- competing news;
- sport season phase;
- content urgency;
- source candidate quality;
- small sample sizes.

The analysis layer must not label ordinary observational correlations as causal experiment wins unless the allocation/design supports that conclusion.

## 15. Segment analysis

Performance may be segmented by:

- platform;
- sport;
- story family;
- template;
- duration band;
- audience/account;
- weekday/time window;
- season phase;
- voice/no voice;
- caption style;
- brand-sting placement;
- asset style;
- CTA;
- paid/organic mode if such a distinction is later used.

Segmentation rules and minimum evidence thresholds must prevent tiny slices from automatically driving policy.

## 16. Cost-aware creative metrics

DLVE should measure not only performance, but performance per resource cost.

Potential derived analysis:

```text
watch_time_per_render_dollar
qualified_views_per_asset_cost
followers_per_generation_cost
incremental_retention_vs_extra_generation_cost
```

This helps determine whether expensive generative video actually beats a Remotion + still-image composition enough to justify its cost.

A-15 will eventually govern resource/budget authority.

## 17. Template leaderboard

The system may maintain evidence such as:

```text
sport: NFL
story_family: single_pick
platform: YouTube Shorts

hook_family             avg_pct_viewed   completion   n
curiosity               ...              ...          ...
evidence_first          ...              ...          ...
question                 ...              ...          ...
```

The leaderboard is descriptive evidence. It is not itself production policy authority.

## 18. Creative policy recommendation

V-5 may output a versioned `CreativePolicyRecommendation`:

```text
recommendation_id
scope
current_policy_ref
proposed_policy_change
supporting_experiment_refs[]
supporting_metric_snapshots[]
analysis_method_ref
confidence_or_evidence_grade
expected_effect
known_risks
created_at
status
```

Allowed statuses:

- `PROPOSED`
- `REVIEWED`
- `ACCEPTED_FOR_CONFIG_CHANGE`
- `REJECTED`
- `EXPIRED`

Before A-24, a human/config release process must apply any accepted change.

## 19. Adaptive automation boundary

Future A-24 may authorize controlled adaptive selection such as:

- multi-armed bandit allocation across approved hooks;
- sport/platform-specific template selection;
- time-window selection;
- asset-style selection;
- duration-band selection.

Even then, adaptation must operate only inside pre-approved creative bounds. It can never mutate sport facts, recommendations, or compliance requirements.

## 20. Drift monitoring

The analysis layer should detect:

- sudden performance collapse after template/brand release;
- platform metric schema change;
- hook performance drift;
- account-level distribution changes;
- unusual negative-feedback changes;
- differences between platforms that make a global policy unsafe.

A-16/A-17 will own production observability/alerting semantics.

## 21. Data retention/provenance

Metric and experiment evidence must retain:

- adapter/release version;
- source observation timestamp;
- exact post/publication package identity;
- exact creative variant;
- raw metric semantics;
- normalization method/version;
- experiment allocation evidence;
- later corrections/revisions without erasing prior snapshots.

A-13 will freeze persistence mechanics.

## 22. Privacy/platform policy boundary

The performance system should use account/content aggregate metrics by default. Any future user-level/audience data use requires explicit privacy/security architecture and platform-permission review. The V1 architecture does not require personal audience profiling.

## 23. Initial implementation phases

1. creative feature manifest emission;
2. publication-package linkage;
3. one platform raw metric adapter;
4. immutable metric snapshots;
5. normalized metric layer;
6. manual dashboards/reports;
7. explicit A/B experiment objects;
8. cost-aware analysis;
9. creative-policy recommendation reports;
10. adaptive selection only after A-24.

## 24. Acceptance criteria

V-5 implementation is acceptable when:

- every metric maps to an exact creative/publication package;
- raw platform semantics are preserved;
- cross-platform metrics are not falsely treated as identical;
- experiment allocation is reproducible;
- experiments cannot alter facts/recommendations;
- results/audit content cannot selectively hide unfavorable outcomes to optimize engagement;
- recommendations are advisory before A-24;
- cost can be included in creative evaluation;
- historical metric snapshots are not overwritten by later observations.