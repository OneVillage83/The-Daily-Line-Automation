# V-2 — The Daily Line Brand and Motion System V1

Status: **ARCHITECTURE BASELINE**  
Date: 2026-09-08

## 1. Purpose

This document defines the reusable visual/audio grammar for The Daily Line social video system. The goal is a recognizable channel identity that can be assembled automatically from reusable components without forcing viewers through a long television-style intro.

The design target is:

> **Sports data terminal + modern short-form motion + cinematic restraint.**

The system should feel analytical, fast, credible, and unmistakably Daily Line without resembling a generic sportsbook commercial or an imitation broadcast package.

## 2. Brand principles

1. Data is the visual hero.
2. Motion should communicate hierarchy, transition, or changing values; decorative motion is secondary.
3. Branding should reinforce the hook, not delay it.
4. The same component system must work across MLB, NFL, NCAAF, and future sports.
5. Sport accents may change; Daily Line core identity does not.
6. Every reusable motion element is versioned.
7. Readability on a phone takes priority over desktop aesthetics.
8. Safe zones and platform UI obstructions are first-class layout constraints.
9. Captions are part of the composition, not an afterthought.
10. Sound design enhances recognition but must never be required for comprehension.

## 3. Core brand assets/components

Implementation should provide these parameterized components:

```text
DailyLineLogo
DailyLineWordmark
DailyLineWatermark
DailyLineBrandSting
DailyLineOutro
DailyLineLowerThird
SportBadge
DataGridBackground
OddsRail
MarketTicker
SectionLabel
StatCard
ComparisonCard
ProbabilityMeter
LineMovementChart
WeatherPanel
PickReveal
ResultBadge
CaptionLayer
CTAChip
DisclaimerLayer
```

No production template should bake copies of these elements directly into one composition when an equivalent shared component exists.

## 4. `DailyLineBrandSting`

This is the reusable title-card animation requested for all Daily Line videos.

### 4.1 Modes

```text
micro
opener
transition
outro
```

The modes share one motion language and component implementation.

### 4.2 Default short-form behavior

The default is **not**:

```text
logo -> tagline -> content
```

The default is:

```text
hook begins immediately
        |
subtle watermark / data motif establishes brand
        |
micro sting integrates into the first transition
        |
body
        |
summary/pick integrated into branded outro
```

### 4.3 Timing baselines at 30 fps

These are initial creative-policy defaults, not permanent performance truths.

| Mode | Baseline duration | Typical frames | Intended use |
|---|---:|---:|---|
| `micro` | 0.6–0.8 sec | 18–24 | after/within hook, quick section break |
| `opener` | ~1.0–1.3 sec | 30–39 | longer recurring shows/special reports |
| `transition` | 0.4–0.7 sec | 12–21 | data-to-data scene bridge |
| `outro` | 1.5–2.5 sec | 45–75 | recommendation/summary/CTA close |

Timing must be stored as creative variant data so retention analysis can test it.

## 5. Sting motion concept

The first visual direction should be implemented with data-native primitives rather than a pre-rendered logo movie.

### Phase A — signal/data activation

- a faint analytical grid or market rail is already moving under the hook;
- one or more numbers/lines slide into a common axis;
- a bright line/sweep establishes the signature Daily Line horizontal motion.

### Phase B — convergence

- odds/data fragments compress or align;
- the horizontal line becomes the visual spine for the wordmark;
- `THE DAILY LINE` resolves rapidly without a long fade.

### Phase C — tagline/continuation

Optional depending on mode:

```text
SEE THE DATA. FIND THE EDGE.
```

The line then continues into the next scene rather than ending on a static title card.

### Outro variant

The same line/grid resolves around a final summary block, for example:

```text
MODEL      63.2%
MARKET     55.1%

PICK       TEAM / MARKET

THE DAILY LINE
SEE THE DATA. FIND THE EDGE.
```

The factual fields are supplied by the approved render spec; the brand component never calculates them.

## 6. Sting props

Conceptual props:

```text
mode
sport_accent_ref
show_tagline
placement_context
headline_optional
summary_fields_optional
cta_optional
disclaimer_profile_ref
duration_policy_ref
sound_sting_ref
experiment_ref
```

The actual Remotion implementation may use Zod props, but canonical creative semantics originate in V-1 contracts.

## 7. Motion implementation rules

The initial Remotion renderer must:

- drive timeline motion from the render frame/time;
- use deterministic interpolation/spring/easing primitives;
- avoid CSS transitions/animations as authoritative timeline behavior;
- keep motion values close to the editable component when practical;
- make scenes and major layers individually previewable;
- use explicit timing rather than setTimeout/browser-clock assumptions;
- honor the render profile fps rather than assuming 30 fps inside components where avoidable.

## 8. Core motion vocabulary

The initial package should use a small repeatable set of transitions:

### `data_sweep`
A horizontal line/rail wipes across and reveals new data.

### `card_rise`
A stat card enters from below with short damped motion.

### `number_lock`
A changing/rolling number settles on the certified value.

### `probability_fill`
A gauge/rail fills to the approved percentage.

### `line_draw`
A market movement line draws through time.

### `grid_focus`
A background grid subtly changes scale/position to move attention.

### `mask_reveal`
Text or card content reveals behind a moving line/mask.

### `hard_data_cut`
Fast cut with a tiny sound/flash cue, used when speed matters more than flourish.

Motion variants are named/versioned so performance analysis can reason about them.

## 9. Typography architecture

Typography is a versioned brand token system.

Token classes:

```text
display
headline
stat_large
stat_label
caption_primary
caption_secondary
body
micro_label
cta
disclaimer
```

Implementation requirements:

- use one primary family and at most a small secondary family set;
- define weights/sizes/line-height centrally;
- support dynamic text fitting with explicit minimum readable sizes;
- prohibit silent overflow/cropping;
- use tabular numerals where appropriate for moving numeric data;
- keep critical text inside platform safe zones.

Actual font selection is a design implementation decision and should be recorded/versioned before production.

## 10. Color/token architecture

Do not scatter raw color values across templates.

Core tokens should include:

```text
background_primary
background_elevated
text_primary
text_secondary
brand_primary
brand_secondary
positive
negative
neutral
warning
data_grid
market_line
```

Sport-specific accent tokens may exist but cannot overwrite the core brand identity.

Team colors/logos are not assumed freely usable. Any official team/league visual assets require the asset-rights policy defined in V-4.

## 11. Background system

Backgrounds are layered, not one giant image:

```text
base field
+ optional image/video layer
+ subtle gradient/light layer
+ data grid / particles / rails
+ foreground cards/text
```

This enables inexpensive motion from still imagery:

- slow camera/pan/scale;
- shallow parallax;
- masked movement;
- animated light/data overlays;
- foreground UI motion.

A cached generated or stock still can therefore support many videos without paying for generative video on every post.

## 12. Generated-image visual policy

The baseline generated imagery should favor:

- generic stadium atmospheres;
- field/court/diamond environments;
- sports equipment;
- abstract analytical/data scenes;
- weather environments;
- tunnels/locker-room-like generic scenes;
- city/stadium atmosphere without false event claims;
- macro sports textures.

By default, prompts should avoid presenting a generated person as a specific real athlete or fabricating an exact news/game photograph. If identifiable people, logos, uniforms, or protected assets are intentionally used, the asset must pass the explicit rights/approval policy.

## 13. Watermark

A subtle Daily Line watermark may begin at frame 0 so the brand is established even when the full sting follows the hook.

Requirements:

- never obstruct key text/data;
- support configurable opacity/position within the safe zone;
- remain consistent within a creative variant;
- not substitute for the full provenance/disclosure system.

## 14. Caption system

Three initial caption styles:

### `tdl_caption_kinetic_v1`
Large central/upper-center short-form captions with selected keyword/value emphasis.

### `tdl_caption_lower_v1`
Lower-third analytical caption style for denser breakdowns.

### `tdl_caption_stat_focus_v1`
Narration text plus a separately animated protected numeric/stat token.

Caption requirements:

- derived from the approved script/caption package;
- timed to speech when voice exists;
- readable without audio;
- protected numeric values cannot be substituted by decorative text generation;
- line wrapping and word count must obey profile-specific limits;
- caption style/position is recorded in the creative variant.

## 15. Audio identity

Audio layers are independently optional:

```text
voiceover
music bed
brand sting
transition SFX
stat/data SFX
```

The visual content must remain understandable if all audio is muted.

### Brand sound

The title sting should have a short reusable sonic signature rather than a long jingle. The sound must have documented ownership/license provenance.

### Music

Music policy must reference licensed/owned/platform-approved assets and permitted surfaces. A track that cannot legally/contractually be used on a target platform is rejected for that platform intent.

## 16. Safe-zone system

Each render profile declares platform-safe regions. Templates consume a named safe-zone profile rather than hard-coding one global rectangle.

The safe-zone system must protect:

- hook text;
- recommendation/pick reveal;
- critical statistics;
- captions;
- CTA;
- disclaimers.

Decorative imagery may extend under platform controls; critical information may not.

## 17. Accessibility/readability

Baseline requirements:

- sufficient text/background contrast under the selected policy;
- no information conveyed only by color;
- captions for narrated short-form where required by policy;
- large enough critical numeric/text sizes for mobile viewing;
- animation must not make factual values unreadable during their required dwell time;
- excessive flashing/strobing is prohibited by brand policy.

## 18. Content pacing primitives

Templates should compose pacing from named timing policies:

```text
hook_fast
hook_standard
card_fast
card_explainer
pick_reveal_fast
pick_reveal_hold
outro_short
outro_standard
```

This lets experiments change pacing as data rather than silently editing component code.

## 19. Short-form default sequence

Initial recommended pattern:

```text
0.00s   hook starts
0.00s   subtle watermark / branded data environment visible
0.6–1.5s micro sting integrated into hook transition
1.2s+   evidence/body
last 2–4s recommendation/summary + branded close
```

Exact times are template-dependent and should be tested rather than permanently assumed.

## 20. Long-form compatibility

The same brand components must support:

- longer YouTube explainers;
- weekly/monthly model reports;
- results/audit shows;
- future horizontal 16:9 video.

Long-form may use the `opener` mode more prominently, but the component remains shared.

## 21. Versioning

Brand releases are immutable references such as:

```text
daily-line-brand@1.0.0
daily-line-brand@1.1.0
```

A production render manifest records the exact brand release. Major visual redesigns create a new release rather than changing historical meaning.

## 22. Initial build order

1. brand tokens;
2. `DailyLineLogo` / `DailyLineWatermark`;
3. `DataGridBackground`;
4. `DailyLineBrandSting` micro mode;
5. sting outro mode;
6. shared `StatCard` / `ProbabilityMeter` / `PickReveal`;
7. caption styles;
8. audio sting integration;
9. visual regression/golden-frame fixtures;
10. expand to opener/transition modes.

## 23. Acceptance criteria

The V-2 implementation is acceptable when:

- the same sting component renders all four modes;
- micro mode can be embedded after/within a hook without a hard title-card interruption;
- title/outro can display supplied certified summary fields without calculating them;
- all shared components use versioned brand tokens;
- critical text passes safe-zone/overflow checks;
- motion is frame-driven and render-stable;
- audio can be removed without losing semantic content;
- templates can change sport accent without forking the brand package;
- creative manifests retain sting mode/placement/timing for performance analysis.