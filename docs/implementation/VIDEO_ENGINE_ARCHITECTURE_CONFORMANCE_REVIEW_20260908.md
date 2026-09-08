# Daily Line Video Engine — Architecture Conformance Review

Date: 2026-09-08  
Reviewed scope: V-0 through V-5 + ADR-0008

## 1. Review purpose

This review tests the social-video architecture against TDLA's existing ownership, identity, execution, provenance, and architecture-first rules before implementation begins.

The review is architecture-only. It grants no external social-publication authority and no production implementation certification.

## 2. Governing constraints checked

The review checked compatibility with these already-established TDLA rules:

- TDLA may coordinate publication/distribution but may not absorb sport intelligence.
- Sport-specific facts, recommendations, explanations, and interpretation remain sport-owned.
- Runtime/backend/vendor IDs do not become canonical TDLA identity.
- immutable versioned input/output artifacts and provenance are required.
- trigger/render/backend success does not automatically authorize a user-visible side effect.
- A-11 will own logical retry/idempotency semantics.
- A-13 will own authoritative persistence/audit DDL.
- A-18 will own external publication/distribution side effects.
- A-24 will own future adaptive/intelligent automation authority.

## 3. Review result

**PASS — V1 architecture baseline is internally coherent and compatible with the certified A-0 through A-10 control-plane architecture, subject to the explicit deferred-authority boundaries recorded below.**

The V-series is a supplemental subsystem architecture. It does not move the canonical A-series continuation point away from A-11.

## 4. Major findings

### Finding 1 — Video engine belongs in TDLA with a strict fact boundary

Result: **PASS**

The system can live in `The-Daily-Line-Automation` because it centralizes generic rendering, brand, asset, QC, publication-package, and performance infrastructure. The critical safeguard is `PublishableFactPackage`: DLVE never receives permission to infer sport meaning from raw model/data state.

### Finding 2 — LLM scripting does not violate sport ownership if fact-bound

Result: **PASS WITH REQUIRED GATE**

The script generator is architecture-compliant only when every factual segment maps to approved claim/fact/explanation IDs and protected values are verified after generation. Unmapped sport claims fail closed.

### Finding 3 — Remotion does not become identity authority

Result: **PASS**

Remotion is behind a renderer adapter and consumes canonical `VideoRenderSpec`. Composition IDs, Node process IDs, Chromium IDs, and renderer-native job IDs are provenance only.

### Finding 4 — Rendering remains separate from publication

Result: **PASS**

V-4 ends at `VideoPublicationPackage`. External social posting remains reserved for A-18, preventing a render worker from gaining accidental social-account side-effect authority.

### Finding 5 — Retry semantics are not duplicated

Result: **PASS**

V-series identity deliberately does not freeze retry/idempotency formulas. Render attempts must bind to future A-11 rather than inventing an independent `video_retry_key` system.

### Finding 6 — Generated media is auditable

Result: **PASS**

Generated images/voice are immutable assets with hashes/provider/model/prompt provenance. Replays reuse stored assets instead of silently calling a provider again and changing historical output.

### Finding 7 — Performance optimization cannot rewrite truth

Result: **PASS**

V-5 records creative variables and metrics only. It cannot alter model predictions/recommendations or self-change production policy before A-24.

## 5. Stress matrix

### Authority / fact integrity

| # | Scenario | Expected result | Review |
|---:|---|---|---|
| 1 | LLM changes `61.8%` to `68.1%` | protected-token mismatch; fail | PASS |
| 2 | LLM invents an injury as a reason | unsupported claim; fail | PASS |
| 3 | LLM infers wind favors under from raw weather only | prohibited without approved explanation | PASS |
| 4 | sport package supplies explicit weather relevance explanation | may paraphrase if allowed | PASS |
| 5 | candidate has only one approved reason | use one reason; do not invent more | PASS |
| 6 | recommendation is `AVOID` but hook asks for "best bet" | policy/fact mismatch; fail | PASS |
| 7 | package expires before render | ineligible; re-resolve | PASS |
| 8 | package expires after render but before publication | publication package becomes ineligible | PASS |
| 9 | sport fact package corrected before publication | old package cannot publish | PASS |
| 10 | result audit contains losses | template cannot hide them when claiming full-period audit | PASS |

### Identity / provenance

| # | Scenario | Expected result | Review |
|---:|---|---|---|
| 11 | same story rendered with two hooks | same story, distinct creative variants | PASS |
| 12 | same creative rendered twice after transient failure | same render spec; attempts under A-11 | PASS |
| 13 | template version changes | new creative/render identity | PASS |
| 14 | platform post ID changes/duplicates | external provenance only | PASS |
| 15 | renderer changes from Remotion later | canonical story/fact identity preserved | PASS |
| 16 | generated asset provider returns new image on retry | authoritative retry reuses stored resolved asset | PASS |
| 17 | asset hash differs from manifest | QC fail | PASS |
| 18 | script model/provider changes | new script/creative provenance | PASS |
| 19 | same MP4 used for two platforms | distinct platform intents/publication packages may reference same artifact | PASS |
| 20 | platform modifies/re-encodes upload | external processing does not replace source render artifact identity | PASS |

### Renderer / fallback

| # | Scenario | Expected result | Review |
|---:|---|---|---|
| 21 | generated image API unavailable | cached/stock/data fallback if permitted | PASS |
| 22 | TTS unavailable | explicit no-voice variant if template permits | PASS |
| 23 | music missing | no-music variant/policy if permitted | PASS |
| 24 | critical image required but unavailable | fail candidate/render prep | PASS |
| 25 | long team label overflows | layout QC fail or valid fit variant | PASS |
| 26 | caption extends under platform controls | safe-zone QC fail | PASS |
| 27 | render file is zero bytes | render probe fail | PASS |
| 28 | process exits 0 but video cannot decode | QC fail | PASS |
| 29 | renderer fetches fresh sports API data | architecture violation | PASS |
| 30 | CSS timeline animation renders differently | implementation violates frame-driven rule | PASS |

### Brand / retention architecture

| # | Scenario | Expected result | Review |
|---:|---|---|---|
| 31 | all shorts begin with 3s static logo | not default policy; requires explicit experiment/design exception | PASS |
| 32 | hook begins immediately, micro sting at ~1s | supported default | PASS |
| 33 | full opener for long-form weekly show | supported `opener` mode | PASS |
| 34 | outro contains pick/summary | supported; avoids dead branding | PASS |
| 35 | sport needs different accent | token/prop variation, not brand fork | PASS |

### Publication / external effects

| # | Scenario | Expected result | Review |
|---:|---|---|---|
| 36 | MP4 QC passes | still no social-post authority | PASS |
| 37 | platform upload ACK lost | deferred to A-18/A-11 reconciliation | PASS |
| 38 | duplicate scheduler callback requests post | future A-18/A-11 must dedupe | PASS |
| 39 | account token leaked in manifest | prohibited | PASS |
| 40 | asset license excludes one platform | platform intent fails rights QC | PASS |

### Performance / experimentation

| # | Scenario | Expected result | Review |
|---:|---|---|---|
| 41 | one hook performs well in tiny sample | no automatic rollout | PASS |
| 42 | TikTok/YouTube `view` semantics differ | preserve raw semantics; version normalization | PASS |
| 43 | model pick accuracy correlates with views | creative system cannot change model policy | PASS |
| 44 | generative video costs 10x but lifts retention slightly | cost-aware analysis allowed | PASS |
| 45 | results audit losses reduce engagement | cannot suppress truthful losses | PASS |
| 46 | experiment changes protected fact value | invalid experiment | PASS |
| 47 | adaptive selector wants new unapproved hook type | blocked outside approved variant set | PASS |
| 48 | A-24 not certified | recommendations only; no autonomous production policy mutation | PASS |

## 6. Deferred-authority checks

### A-11

No logical idempotency-key formula or physical-attempt semantics are frozen by the video docs. PASS.

### A-13

No authoritative PostgreSQL DDL is frozen. Logical object-storage namespaces are illustrative only. PASS.

### A-15

Cost/resource telemetry is anticipated but no budget-enforcement authority is preempted. PASS.

### A-18

External publication is explicitly out of V-series scope. `VideoPublicationPackage` is a handoff contract only. PASS.

### A-20

Provider/platform credentials remain logical secret references only. PASS.

### A-24

Performance system is advisory until adaptive authority is explicitly certified. PASS.

## 7. Compatibility with MLB/NFL/NCAAF direction

### MLB

Compatible as long as the final certified MLB pipeline produces explicit publishable facts/explanations rather than asking DLVE to inspect raw MLB state and invent a story.

### NFL/NCAAF

Compatible with multiple pregame snapshots/event-relative updates because content packages include validity/expiry and source run/scope provenance. DLVE does not need football-specific readiness semantics.

### Multi-sport

The same rendering contracts apply because sport-specific meaning is supplied as approved content, while the renderer handles generic cards, probabilities, lines, weather displays, explanations, results, and branding.

## 8. Architecture status decision

The following V1 documents are accepted as the **DLVE V1 architecture baseline**:

- `docs/video/V00_SOCIAL_VIDEO_ENGINE_ARCHITECTURE_V1.md`
- `docs/video/V01_VIDEO_JOB_AND_FACT_CONTRACTS_V1.md`
- `docs/video/V02_BRAND_MOTION_SYSTEM_V1.md`
- `docs/video/V03_TEMPLATE_LIBRARY_V1.md`
- `docs/video/V04_RENDER_ASSET_QC_HANDOFF_V1.md`
- `docs/video/V05_PERFORMANCE_EXPERIMENTATION_V1.md`
- `docs/adr/ADR-0008_PARAMETERIZED_VIDEO_RENDERER_AND_FACT_AUTHORITY.md`

This acceptance is **architecture authority for the supplemental video subsystem only**. It grants no production implementation or platform-publication authority.

## 9. Exact safe implementation continuation

When video implementation is intentionally started, begin with:

> **VM-0 — canonical JSON Schema contracts + cross-language fixtures.**

Then:

> VM-1 Remotion scaffold -> VM-2 brand foundation -> VM-3 components -> VM-4 synthetic `single_pick_v1`.

Do not begin real social posting before A-18. Do not invent retry/persistence/security mechanics before their A-series authority is certified.

## 10. Core TDLA continuation remains unchanged

The canonical A-series exact next architecture step remains:

> **A-11 Retry / Timeout / Idempotency Architecture.**

The video architecture does not supersede that continuation point.