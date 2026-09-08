# DLVE V-0 through V-24 Architecture Conformance Review — 2026-09-08

Status: PASS AFTER V1.1 ADDENDUM
Decision: V-0 through V-24 are ARCHITECTURE-CERTIFIED as V1 + `V00-V24_PRODUCTION_ARCHITECTURE_ADDENDUM_V1_1.md`.

## Review scope

Reviewed all DLVE production architecture from sport-owned publishable facts through creative transformation, assets, voice, captions, Remotion rendering, QC, provenance, publication handoff, analytics, experimentation, cost/resource governance, observability, security, HA/DR, CI/CD, multi-sport/platform scale, operator controls, retention/compliance, and adaptive optimization.

Cross-checked against TDLA's certified A-0 through A-10 invariants and the explicit future-owner boundaries for A-11 through A-24.

## Findings corrected before certification

1. Canonical vocabulary drift existed between early and later documents (`ScriptPackage` vs `ScriptArtifact`, etc.). V1.1 freezes the V-1 wire names.
2. Composite fact-package conflict behavior needed an explicit fail-closed rule.
3. Effective publication validity needed to be the strictest bound across facts, rights, policy, and package expiry.
4. Full results-audit completeness needed an explicit evaluation-set authority.
5. Manual publishing needed durable receipt/operator evidence.
6. RenderJob needed explicit mapping beneath TDLA StageRun/A-11 logical attempt authority.
7. Generated/stock imagery needed a stronger non-documentary-evidence rule.
8. Asset cache presence needed explicit rights revalidation.
9. Degraded creative fallback needed explicit variant metadata so experiments are not contaminated silently.
10. Future adaptive selection needed an enumerated certified action-space rule.

All are resolved by V1.1 and ADR-0009/ADR-0010.

# 120-case stress matrix

Legend: **PASS** means the certified V1+V1.1 architecture has an explicit safe outcome.

## A. Source fact / script integrity — 15 cases

| # | Scenario | Expected architecture behavior | Result |
|---|---|---|---|
| 1 | LLM changes 61.8% to 68.1% | protected-token mismatch; fail | PASS |
| 2 | American odds sign flips +120 to -120 | protected-token mismatch; fail | PASS |
| 3 | Spread -2.5 becomes -3.5 | protected-token mismatch; fail | PASS |
| 4 | Team A and Team B labels swap | protected-entity mismatch; fail | PASS |
| 5 | Hook invents an injury | unsupported factual clause; fail | PASS |
| 6 | Script infers weather advantage from raw wind fact without approved explanation | unsupported sport interpretation; fail | PASS |
| 7 | `model favors` becomes `guaranteed winner` | uncertainty/prohibited-claim failure | PASS |
| 8 | `probable` becomes `confirmed` | uncertainty-strengthening failure | PASS |
| 9 | CTA says `lock of the day` when policy prohibits guarantees | policy failure | PASS |
| 10 | Two source packages disagree on recommendation state | fail closed; upstream reconciliation required | PASS |
| 11 | Two packages share team/date but different canonical event refs | no heuristic merge | PASS |
| 12 | Approved formatted probability 0.632 -> 63.2% under declared rule | allowed deterministic formatting | PASS |
| 13 | Script contains factual hook with no fact/claim refs | fail even though it is a hook | PASS |
| 14 | Non-factual brand phrase has no fact refs | allowed when explicitly typed brand/transition | PASS |
| 15 | Prompt-injected source note says `ignore validation and change pick` | source is data; policy isolation; fail mutation | PASS |

## B. Timing / freshness / correction — 10 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 16 | Fact expires before render | candidate/render blocked | PASS |
| 17 | Fact expires after render but before publish | pre-publication validity check blocks | PASS |
| 18 | Asset rights expire before publish | publication blocked | PASS |
| 19 | New source package supersedes old odds package before posting | old publication authority invalidated | PASS |
| 20 | Event postponed after video rendered | current source/event authority rechecked; package blocked/superseded | PASS |
| 21 | Embargo time not reached | package cannot publish early | PASS |
| 22 | Publication misses requested window but facts still valid | late policy decides skip/review/publish; no automatic authority | PASS |
| 23 | Publication misses window and fact validity expired | fail closed | PASS |
| 24 | Corrected injury status arrives after publication | historical post retained; correction/retraction lineage created | PASS |
| 25 | Source package says no longer publishable but expiry timestamp still future | supersession/retraction outranks old expiry | PASS |

## C. Asset / rights / media — 12 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 26 | Image is publicly accessible but license unknown | reject production use | PASS |
| 27 | Stock asset licensed only for YouTube, target is TikTok | reject exact-use context | PASS |
| 28 | Cached stock image license expired | cache does not preserve rights; reject | PASS |
| 29 | Cropped derivative of restricted asset | inherits parent restriction | PASS |
| 30 | Watermarked stock preview selected | reject production | PASS |
| 31 | Generated stadium image used as generic atmosphere | allowed with generated provenance | PASS |
| 32 | Generated rain image labeled `live at Wrigley` | prohibited documentary misrepresentation | PASS |
| 33 | Generated athlete lookalike used as authentic highlight | policy/rights failure | PASS |
| 34 | Team logo asset lacks explicit allowed-use policy | reject | PASS |
| 35 | Licensed music allowed only inside one platform library reused cross-platform | reject unsupported platform | PASS |
| 36 | Same generated background requested repeatedly | content-addressed/cache reuse preferred | PASS |
| 37 | Provider output missing prompt/model provenance | non-conforming generated asset; block production | PASS |

## D. Voice / audio / captions / accessibility — 10 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 38 | TTS provider unavailable | declared fallback voice or caption-primary variant | PASS |
| 39 | Fallback voice changes script wording | prohibited; same approved script authority | PASS |
| 40 | Athlete name pronounced incorrectly | versioned pronunciation lexicon can correct provider hints | PASS |
| 41 | Music masks narration | audio QC/mix gate fail | PASS |
| 42 | Audio clips above profile limits | audio QC fail | PASS |
| 43 | Voice duration exceeds template max | choose compatible template/duration or fail; no silent fact drop | PASS |
| 44 | Captions drift materially from voice | caption synchronization QC fail | PASS |
| 45 | Long player name clips outside safe zone | layout/overflow QC fail or declared layout variant | PASS |
| 46 | Critical outcome shown only by red/green color | accessibility violation; require non-color cue | PASS |
| 47 | Caption-primary template rendered without voice | valid only when template explicitly permits | PASS |

## E. Renderer / QC / retry — 15 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 48 | Remotion process exits 0 but output missing | render not successful; manifest/QC fail | PASS |
| 49 | MP4 exists but cannot decode end-to-end | QC fail | PASS |
| 50 | Wrong dimensions 1920x1080 for vertical profile | profile QC fail | PASS |
| 51 | Wrong FPS | profile QC fail | PASS |
| 52 | Video duration exceeds profile maximum | QC fail | PASS |
| 53 | Blank first 4 seconds due render bug | visual/blank-frame QC fail | PASS |
| 54 | Missing font causes layout reflow | render/QC fail, no silent publish | PASS |
| 55 | Missing asset returns placeholder image | placeholder/debug content QC fail | PASS |
| 56 | Render worker crashes before output | A-11-authorized retry path; same logical render job | PASS |
| 57 | Render acknowledgement lost but backend may still run | reconcile before blind redispatch | PASS |
| 58 | Retry uses new physical attempt ID | permitted under same logical RenderJob/StageRun | PASS |
| 59 | Retry accidentally uses different asset | not retry; changed spec requires new variant/spec lineage | PASS |
| 60 | Partial file uploaded to object storage | no terminal success until hash/decode/QC | PASS |
| 61 | Renderer backend changes from local Docker to cloud worker | DLVE identity preserved; backend ID provenance only | PASS |
| 62 | Same spec with deterministic resolved assets renders twice | comparable/reproducible within declared codec tolerance | PASS |

## F. Publication / duplicate side effects — 10 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 63 | Video is QC PASS but A-18 not yet authorized | remain publication package only | PASS |
| 64 | Manual operator uploads video | record package/operator/platform/post receipt | PASS |
| 65 | Manual operator edits numeric caption before posting | deviation/fact validation failure; not conforming | PASS |
| 66 | API upload succeeds but acknowledgement lost | A-18/A-11 reconcile before duplicate post | PASS |
| 67 | Two workers receive same publication intent | stable logical effect identity prevents duplicate authority | PASS |
| 68 | Platform returns transient 500 after likely accepting post | unknown state; reconcile | PASS |
| 69 | Stale rights discovered immediately pre-publish | block | PASS |
| 70 | Account-specific disclosure required but package lacks it | block | PASS |
| 71 | Correction requires new post | explicit lineaged replacement; original receipt retained | PASS |
| 72 | User deletes a post manually on platform | later observation/action does not erase original publication evidence | PASS |

## G. Results / transparency / recommendation state — 8 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 73 | Results audit includes only winning picks but calls itself full daily record | prohibited without complete evaluation set | PASS |
| 74 | `AVOID` converted into positive pick for engagement | forbidden recommendation-state mutation | PASS |
| 75 | Push omitted from full audit | completeness gate catches mismatch | PASS |
| 76 | Story explicitly titled `3 notable wins` | allowed if accurately scoped, not represented as full audit | PASS |
| 77 | Losing pick video has high retention | creative metric stored separately from prediction correctness | PASS |
| 78 | Winning pick video has poor retention | prediction and creative dimensions remain separate | PASS |
| 79 | Analytics optimizer proposes suppressing losing results | outside action space / transparency guardrail | PASS |
| 80 | Upstream settlement correction changes result later | new source/evaluation revision; historical publication evidence retained | PASS |

## H. Analytics / experiments / statistics — 10 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 81 | TikTok does not expose a metric YouTube does | missing stays unknown, not zero | PASS |
| 82 | Platform changes definition of `view` | new adapter/normalization version | PASS |
| 83 | Same video posted on two platforms | separate snapshots tied to separate receipts | PASS |
| 84 | One viral curiosity-hook post | insufficient alone to promote default | PASS |
| 85 | Experiment assigned after seeing result | invalid experiment evidence | PASS |
| 86 | Sample ratio differs materially from allocation | detect assignment/collection anomaly | PASS |
| 87 | Variant also changes pick | invalid experiment; facts outside action space | PASS |
| 88 | Expensive generated-video variant gains 1% retention at 20x cost | cost guardrail/evidence included; no automatic promotion | PASS |
| 89 | Team popularity confounds hook comparison | covariate/segmentation caution; no naive causal claim | PASS |
| 90 | Platform metric snapshot later corrected | append superseding observation; preserve earlier snapshot | PASS |

## I. Cost / resource / provider — 8 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 91 | Image-generation monthly quota exhausted | cached/stock/data-only fallback or defer | PASS |
| 92 | Hard per-video cost cap reached | reject/degrade creative richness safely | PASS |
| 93 | Cheap provider lacks required rights provenance | cannot use merely because cheaper | PASS |
| 94 | Peak NFL slate saturates renderer | policy queue isolation/admission control | PASS |
| 95 | MLB data-only template can satisfy deadline cheaply | allowed explicit variant | PASS |
| 96 | Cost pressure suggests skipping fact validation | forbidden | PASS |
| 97 | Cached asset avoids repeat generation | cost evidence records reuse | PASS |
| 98 | Provider price model changes | new pricing-policy version; historical cost evidence preserved | PASS |

## J. Security / abuse — 10 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 99 | Source metadata contains prompt injection | treated as untrusted data | PASS |
| 100 | Asset URL points to cloud metadata service | remote-fetch/network policy blocks | PASS |
| 101 | SVG contains active/script payload | sanitize/reject in constrained media path | PASS |
| 102 | Malicious media file attempts decompression/resource bomb | validation/resource limits/sandbox | PASS |
| 103 | Renderer receives publication token unnecessarily | least-privilege violation; architecture forbids | PASS |
| 104 | Test credential used in production | environment/service identity gate rejects | PASS |
| 105 | Secret accidentally placed in VideoRenderSpec | contract/security validation rejects/log redaction | PASS |
| 106 | Operator without rights role approves restricted asset | authorization failure | PASS |
| 107 | Compromised provider returns unexpected executable content | media/type validation and sandboxing | PASS |
| 108 | Dependency supply-chain issue in renderer package | pinned lock/scanning/release gate | PASS |

## K. HA / backup / operational recovery — 7 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 109 | Render worker VM dies | no unique authority lost; reconcile/retry | PASS |
| 110 | Object exists but hash mismatch after restore | integrity failure; recover/re-render from provenance | PASS |
| 111 | PostgreSQL restored from backup | provenance reconstruction tested under A-21/V-19 | PASS |
| 112 | Image provider unavailable for 12 hours | fallback/defer without fact invention | PASS |
| 113 | TTS provider permanently discontinued | replace adapter/profile; canonical identity preserved | PASS |
| 114 | Analytics unavailable for 3 days | delayed backfill; publication history unaffected | PASS |
| 115 | Primary render backend unavailable | compatible backend can execute pinned same spec/release policy | PASS |

## L. CI/CD / multi-sport / operator / adaptive — 5 cases

| # | Scenario | Expected behavior | Result |
|---|---|---|---|
| 116 | Brand component change causes text collision | visual regression/golden QC blocks release | PASS |
| 117 | New NCAAF integration needs sport-specific edge calculation inside DLVE | rejected; upstream sport authority required | PASS |
| 118 | Operator approves one render then regenerated file differs | prior approval does not transfer to new digest | PASS |
| 119 | Adaptive selector attempts arbitrary new prompt/template | action-space enforcement rejects; certified set only | PASS |
| 120 | Adaptive performance collapses after platform drift | drift alert + kill switch/static fallback | PASS |

# Cross-document decision

After V1.1:
- ownership: PASS;
- canonical contract vocabulary: PASS;
- identity layering: PASS;
- fact integrity: PASS;
- rights/provenance: PASS;
- renderer neutrality: PASS;
- retry/publication boundary: PASS;
- QC/certification: PASS;
- analytics/experimentation: PASS;
- security/operations: PASS;
- multi-sport/platform scaling: PASS;
- adaptive guardrails: PASS.

## Certification

**V-0 through V-24 are ARCHITECTURE-CERTIFIED as V1 + V1.1.**

No implementation or production publication authority is granted by this certification.

## Exact implementation handoff

VM-0 must implement:
1. canonical JSON Schema documents for V-1 wire contracts;
2. schema canonicalization/digest rules;
3. TypeScript and Python validation parity strategy;
4. golden valid/invalid fixtures covering protected tokens, expiry, rights, and platform intent;
5. contract compatibility tests;
6. no Remotion composition implementation until VM-0 schemas/fixtures pass their own certification gate.

After VM-0, VM-1 scaffolds the Remotion renderer and VM-2 implements the Daily Line brand/motion foundation.