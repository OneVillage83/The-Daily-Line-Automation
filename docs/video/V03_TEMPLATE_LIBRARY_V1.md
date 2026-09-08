# V-3 — Reusable Video Template Library V1

Status: **ARCHITECTURE BASELINE**  
Date: 2026-09-08

## 1. Purpose

The Daily Line does not use one universal video template. It uses a small, reusable library of story families composed from shared brand/data components.

Each template:

- is parameterized;
- consumes only V-1 approved content;
- has explicit scene/claim requirements;
- declares duration bands and render-profile compatibility;
- records versioned creative choices for performance analysis;
- must fail closed when required facts/scenes cannot be populated.

## 2. Shared template rules

1. The hook appears before any blocking brand card in short-form unless an experiment explicitly changes that policy.
2. The template cannot calculate or infer sport recommendations.
3. The template cannot silently omit a required disclaimer or expiry restriction.
4. Numeric/stat values are rendered from protected source facts.
5. Every scene has a maximum text density and safe-zone policy.
6. Outro content should summarize value already delivered rather than becoming dead branding time.
7. Templates may omit voice/music when their fallback contract permits it.
8. Template logic is presentation logic only.

## 3. Shared scene primitives

Templates may compose these scene families:

```text
HookScene
MatchupScene
StatScene
ComparisonScene
ReasonScene
WeatherScene
LineMovementScene
ModelProbabilityScene
PickRevealScene
RankingScene
ResultScene
AuditSummaryScene
DataStoryScene
BrandTransitionScene
OutroScene
DisclaimerScene
```

## 4. Template TDL-01 — `single_pick_v1`

### Goal

Fast, evidence-led explanation of one approved Daily Line recommendation.

### Target duration

15–25 seconds baseline.

### Required inputs

- event/matchup identity presentation fields;
- recommendation state and approved display value;
- at least one approved supporting claim/explanation;
- at least one approved model/market/stat fact suitable for display;
- content expiry;
- disclaimer profile.

### Default scene grammar

```text
HOOK
  -> micro brand transition
  -> MATCHUP
  -> REASON / STAT
  -> MODEL OR COMPARISON
  -> PICK REVEAL
  -> BRANDED SUMMARY / CTA
```

### Hook families

- curiosity: "One line stands out on tonight's slate."
- contrast: "The model and the market disagree here."
- evidence-first: approved stat/value opens immediately.
- question: "Why does the model like this side?"

Hooks that state sport-specific reasons must map to approved explanation claims.

### Fallbacks

- no generated hero image -> use branded data background;
- no voice -> caption-led version;
- one approved reason only -> compress to reason + pick rather than fabricate a second reason.

## 5. Template TDL-02 — `top_three_v1`

### Goal

Rank multiple approved candidates for a slate/day.

### Target duration

20–35 seconds baseline.

### Required inputs

- 2–3 publishable candidates;
- authoritative ordering or generic ranking policy that does not invent sport meaning;
- one compact approved fact/reason per item;
- recommendation display state per item.

### Default scene grammar

```text
HOOK: "Three spots from today's slate"
  -> #3 card
  -> #2 card
  -> #1 card
  -> summary / CTA
```

If the sport authority does not provide a meaningful rank, DLVE may label the items as "three spots" rather than implying #1 is analytically superior.

## 6. Template TDL-03 — `model_explainer_v1`

### Goal

Explain an approved model conclusion using sport-owned reason claims.

### Target duration

25–50 seconds baseline.

### Required inputs

- approved conclusion;
- 2–4 approved explanations/reasons;
- supporting facts;
- optional market/model comparison.

### Default scene grammar

```text
HOOK / QUESTION
  -> matchup/context
  -> reason 1
  -> reason 2
  -> optional reason 3
  -> model/market summary
  -> approved recommendation or neutral conclusion
  -> outro
```

This template is prohibited from deriving its own explanation from raw feature values.

## 7. Template TDL-04 — `line_movement_v1`

### Goal

Turn an approved meaningful line/price movement into a timely short.

### Target duration

10–25 seconds baseline.

### Required inputs

- market identifier;
- old value;
- new value;
- timestamps/source;
- approved context/explanation if the video claims why the move happened;
- expiry/freshness policy.

### Default scene grammar

```text
HOOK: "This line just moved"
  -> animated old -> new value
  -> optional approved reason/context
  -> current model/market relation if approved
  -> CTA / branded close
```

If no approved causal explanation exists, the video may say that the line moved but may not speculate about the cause.

## 8. Template TDL-05 — `weather_edge_v1`

### Goal

Present weather conditions that a certified sport pipeline has explicitly deemed relevant.

### Target duration

15–35 seconds baseline.

### Required inputs

- approved weather facts;
- event/stadium/location presentation data;
- sport-owned relevance explanation;
- approved recommendation/context if included.

### Default scene grammar

```text
HOOK: weather value/condition
  -> weather card
  -> sport-owned relevance explanation
  -> model/market implication if approved
  -> summary
```

DLVE is explicitly prohibited from inferring that wind/rain/temperature favors a side/total based only on raw weather data.

## 9. Template TDL-06 — `results_audit_v1`

### Goal

Publish transparent post-event performance/results.

### Target duration

15–45 seconds baseline.

### Required inputs

- certified settled/evaluated result package;
- exact evaluation window/date;
- win/loss/push/no-action semantics supplied by sport/evaluation authority;
- unit/ROI/CLV metrics only if officially produced;
- sample size.

### Default scene grammar

```text
DATE / AUDIT HOOK
  -> aggregate result summary
  -> compact result cards
  -> optional calibration/CLV/model metric
  -> losses/failures remain visible per policy
  -> branded close
```

This template must not cherry-pick only winners when it is labeled as a daily/weekly audit of the full eligible set.

## 10. Template TDL-07 — `data_story_v1`

### Goal

Educational/growth content built from approved research/statistical claims rather than necessarily a betting recommendation.

### Target duration

25–60 seconds baseline, with longer variants supported.

### Required inputs

- approved thesis/claim;
- supporting facts and explanations;
- source/provenance;
- no requirement for a recommendation.

### Example story shapes

- myth vs evidence;
- why one metric matters;
- stadium/weather explanation;
- model concept;
- market concept;
- historical data pattern with stated limitations.

### Default scene grammar

```text
HOOK
  -> claim
  -> evidence 1
  -> evidence 2
  -> interpretation supplied by authority
  -> takeaway
  -> brand/CTA
```

## 11. Future templates

The architecture should support later additions without changing V-1 contracts:

- injury/status alert;
- upset/watchlist;
- game-day slate opener;
- morning report;
- closing-line recap;
- weekly model audit;
- head-to-head matchup deep dive;
- player prop story;
- market education;
- long-form YouTube analysis;
- breaking-news context only when authoritative content exists.

## 12. Template manifest

Every template release declares:

```text
template_id
template_version
supported_story_family
supported_render_profiles
required_fact_kinds[]
required_claim_types[]
optional_scene_types[]
required_scene_types[]
min_duration_ms
max_duration_ms
voice_policy
caption_policy
asset_slot_contracts[]
disclaimer_slot
fallback_policy_ref
brand_release_compatibility
```

## 13. Component composition contract

Templates should use shared components rather than duplicate visuals.

Example:

```text
single_pick_v1
├── HookScene
│   ├── DataGridBackground
│   ├── HookText
│   └── DailyLineWatermark
├── BrandTransitionScene
│   └── DailyLineBrandSting(mode=micro)
├── ReasonScene
│   ├── StatCard
│   └── SectionLabel
├── ModelProbabilityScene
│   ├── ProbabilityMeter
│   └── ComparisonCard
├── PickRevealScene
│   └── PickReveal
└── OutroScene
    └── DailyLineBrandSting(mode=outro)
```

## 14. Dynamic duration

A template may calculate duration from the resolved scene/script/caption timing before render, but once `VideoRenderSpec` is created, authoritative duration is fixed for that render spec.

A renderer must not arbitrarily stretch or truncate factual scenes after the render spec is immutable.

## 15. Image strategy per template

Visual priority order:

1. Daily Line data UI and motion;
2. approved reusable owned/generated/stock background;
3. new generated still only when the story materially benefits;
4. approved stock motion;
5. generative video only when explicitly selected and budget/policy allows.

Most Daily Line shorts should be able to render without generative video.

## 16. Hook experimentation

Each template exposes a controlled set of hook slots rather than asking an LLM to freely reinvent the first seconds every time.

Hook dimensions may include:

- statement vs question;
- curiosity vs evidence-first;
- value-first vs matchup-first;
- one-line vs two-line;
- hook duration;
- brand-sting timing.

All hook variants are recorded in `CreativeVariantId`/manifest data.

## 17. Outro experimentation

Outro variants may test:

- follow CTA;
- website CTA;
- no CTA;
- next-video teaser;
- recommendation summary;
- results transparency message.

The outro must remain compatible with platform policy and the applicable disclaimer profile.

## 18. Render-profile compatibility

Initial template support:

| Template | Vertical social | Horizontal long-form | Square |
|---|---|---|---|
| single_pick_v1 | required | future | future |
| top_three_v1 | required | future | future |
| model_explainer_v1 | required | future | future |
| line_movement_v1 | required | optional future | future |
| weather_edge_v1 | required | future | future |
| results_audit_v1 | required | future | future |
| data_story_v1 | required | planned | future |

Horizontal versions should be explicit layout variants, not naive crops of vertical compositions.

## 19. Template testing

Every template implementation requires:

- minimum-content fixture;
- maximum-density fixture;
- long team/name/value fixture;
- no-image fallback fixture;
- no-voice fallback fixture if supported;
- required disclaimer fixture;
- invalid missing-fact fixture;
- expired content fixture;
- visual golden-frame samples at important timeline points;
- short render smoke test;
- cross-template shared-component version test.

## 20. Initial implementation priority

Build in this order:

1. `single_pick_v1`
2. `top_three_v1`
3. `results_audit_v1`
4. `line_movement_v1`
5. `weather_edge_v1`
6. `model_explainer_v1`
7. `data_story_v1`

`single_pick_v1` is the reference template used to prove the complete architecture before expanding the library.