# The Daily Line Automation — Current Resume Point

Last updated: 2026-09-08 (America/Los_Angeles)  
Authority: This file is the single exact continuation point for unfinished TDLA work. It does not override architecture/certification authority; it tells the next session where to resume.

## Current core TDLA state

- Repository constitution/documentation-memory policy is authoritative in `AGENTS.md`.
- A-0 through A-4 Foundation V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-5 Sport Automation Adapter V1 + V1.1 is **ARCHITECTURE-CERTIFIED**.
- A-6 Pipeline Plan / Stage Contracts V1 + V1.1 is **ARCHITECTURE-CERTIFIED**.
- A-7 Trigger Architecture V1 + V1.1 is **ARCHITECTURE-CERTIFIED**.
- A-8 Event-Relative Scheduling Engine V1 + V1.1 is **ARCHITECTURE-CERTIFIED**.
- A-9 Dependency / Readiness Engine V1 + V1.1 is **ARCHITECTURE-CERTIFIED**.
- A-10 Worker / Execution Backend V1 + V1.1 is **ARCHITECTURE-CERTIFIED**.
- ADR-0001 through ADR-0007 govern the certified core architecture through A-10.
- No production implementation milestone is certified.
- No TDLA automation is production-authoritative.
- Daily-MLB remains manual-first; later automation must prove equivalence after its final manual production pipeline is certified.

Full A-0 through A-10 rules and evidence remain in the governing architecture files, certification log, and conformance reviews. This resume point intentionally does not duplicate every previously certified invariant.

---

# Supplemental architecture completed 2026-09-08 — Daily Line Video Engine (DLVE)

A complete V1 supplemental architecture baseline for automated social video now exists inside this repository.

## Governing video documents

- `docs/video/README.md` — video architecture index and A-series boundary map.
- `docs/video/V00_SOCIAL_VIDEO_ENGINE_ARCHITECTURE_V1.md` — system topology, ownership, identity, provenance, renderer boundary.
- `docs/video/V01_VIDEO_JOB_AND_FACT_CONTRACTS_V1.md` — canonical `PublishableFactPackage` through `VideoPublicationPackage` contracts.
- `docs/video/V02_BRAND_MOTION_SYSTEM_V1.md` — Daily Line visual/motion/audio system and reusable `DailyLineBrandSting`.
- `docs/video/V03_TEMPLATE_LIBRARY_V1.md` — `single_pick`, `top_three`, `model_explainer`, `line_movement`, `weather_edge`, `results_audit`, `data_story` templates.
- `docs/video/V04_RENDER_ASSET_QC_HANDOFF_V1.md` — Remotion adapter, asset provenance, generated-still policy, render/QC, A-18 handoff.
- `docs/video/V05_PERFORMANCE_EXPERIMENTATION_V1.md` — creative metrics, experimentation, cost-aware evaluation, A-24 boundary.
- `docs/implementation/VIDEO_ENGINE_IMPLEMENTATION_ROADMAP_V1.md` — VM-0 through VM-15 implementation/certification sequence.
- `docs/implementation/VIDEO_ENGINE_ARCHITECTURE_CONFORMANCE_REVIEW_20260908.md` — 48-case architecture stress review; PASS for the supplemental baseline.
- `docs/adr/ADR-0008_PARAMETERIZED_VIDEO_RENDERER_AND_FACT_AUTHORITY.md` — accepted decision to use a parameterized renderer with sport-owned fact authority and Remotion as the replaceable V1 render runtime.
- `docs/implementation/VIDEO_ENGINE_CHANGE_RECORD_20260908.md` — durable change record for this architecture pass.

## Locked DLVE rules that must not be forgotten

1. **DLVE presentation is not sport intelligence.** Sport repositories remain authoritative for facts, predictions, Recommendation Gate state, causal interpretation, and sport-specific explanation claims.
2. Sport/content authorities emit a versioned `PublishableFactPackage`; DLVE may reorder/shorten/paraphrase approved material but may not create new sport truth.
3. Every factual script segment maps to approved claim/fact/explanation IDs; numeric/entity values may be protected tokens. Unsupported claims fail closed.
4. Remotion + React + TypeScript is the initial renderer, but Remotion composition/process/backend IDs are provenance only.
5. Canonical cross-language video contracts are versioned JSON/JSON Schema; Python and TypeScript meanings must remain mechanically aligned.
6. The reusable `DailyLineBrandSting` supports `micro`, `opener`, `transition`, and `outro` modes. Default short-form policy is hook-first with the micro sting after/within the hook rather than a blocking multi-second logo intro.
7. Initial master profile is `vertical_social_v1` at 1080x1920 / 9:16 / 30 fps; additional layouts are explicit render profiles, not blind crops.
8. Most videos should use reusable data graphics + cached owned/generated/stock stills + motion/captions/voice rather than expensive generative video.
9. Generated/stock/licensed/owned assets require immutable provenance, content hash, rights/policy metadata, and platform compatibility.
10. Authoritative rendering consumes a fully resolved immutable `VideoRenderSpec`; it may not fetch fresh sport facts during render.
11. Render success does not authorize publication. V-series output ends at a passed `VideoPublicationPackage`; future A-18 owns social-platform side effects.
12. Video retries/attempts must bind to future A-11; V-series architecture does not invent a separate retry/idempotency formula.
13. Exact persistence/DDL remains A-13; resource/provider budgets remain A-15; secrets/service identity remain A-20.
14. Performance metrics bind to exact creative variants and preserve platform-native semantics. Cross-platform `view` metrics are not assumed identical.
15. Creative experiments may alter approved presentation variables only. They cannot alter facts, recommendations, model thresholds, or hide unfavorable results from a full results audit.
16. Before A-24, performance analysis may recommend a creative-policy change but may not autonomously apply it to production.

## Safe video implementation sequence when intentionally resumed

Do **not** start with social API posting.

Start here:

> **VM-0 — implement canonical JSON Schemas + valid/invalid fixtures + Python/TypeScript parity tests.**

Then:

```text
VM-1  Remotion renderer scaffold
  -> VM-2  Daily Line brand foundation + reusable title sting
  -> VM-3  shared data/caption components
  -> VM-4  synthetic single_pick_v1 reference video
  -> VM-5  fact-bound LLM script transformer
  -> VM-6  asset broker / generated-still caching
  -> VM-7  voice/captions/audio
  -> VM-8  render worker + QC
  -> VM-9  real MLB shadow input only after source handoff is certified
```

External publication remains blocked until A-18 is certified.

---

# Exact next core TDLA step — A-11 Retry / Timeout / Idempotency Architecture

The video architecture is complete for this checkpoint and does **not** supersede the canonical A-series sequence.

Resume core TDLA architecture at:

> **A-11 Retry / Timeout / Idempotency Architecture.**

Central rule to preserve:

> A retry is a new physical `RunAttempt` of the same logical StageRun/operation, carrying the same stable logical idempotency identity. Timeout, lease loss, heartbeat loss, missing acknowledgement, or unknown state is not proof the prior attempt/child/side effect disappeared. Reconciliation and current-authority revalidation come before any retry that could duplicate work.

A-11 must freeze logical operation identity, StageRun uniqueness, stable logical idempotency hierarchy, RunAttempt sequencing, timeout/reconciliation behavior, and side-effect deduplication boundaries while leaving generalized failure/degradation to A-12 and PostgreSQL uniqueness/outbox mechanics to A-13.

## If the next user request is specifically to start building the video system

Do not redo architecture discovery. Read the V-series documents above and begin **VM-0** directly.

## If the next user request is to continue the main automation architecture

Begin **A-11** directly.