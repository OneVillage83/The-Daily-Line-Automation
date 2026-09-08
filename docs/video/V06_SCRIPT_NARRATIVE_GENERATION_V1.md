# The Daily Line Video Engine — V-6 Script / Narrative Generation V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define the production-safe creative-language layer that transforms sport-owned publishable facts into concise social-video narration without creating new sport intelligence.

## 2. Authority boundary

The script system MAY:
- reorder already-approved facts for clarity;
- compress or expand approved explanations;
- choose tone, hook form, sentence length, cadence, and rhetorical structure;
- produce multiple creative variants from identical fact authority;
- generate captions/voiceover text that preserve semantic meaning.

The script system MUST NOT:
- invent or alter numeric facts;
- infer a new betting recommendation;
- infer causal sport claims not supplied by the source package;
- convert uncertainty into certainty;
- omit required risk/disclosure/result context when the source marks it mandatory;
- claim guarantees, locks, certainties, or risk-free outcomes.

## 3. Canonical inputs

`ScriptGenerationRequest` binds:
- `video_job_id`;
- exact `PublishableFactPackage` identity/digest;
- template/version;
- platform target;
- target duration band;
- tone profile/version;
- hook strategy/version;
- disclosure policy/version;
- prohibited-claim policy/version;
- model/provider identity when AI is used;
- deterministic generation settings when supported.

## 4. Canonical outputs

`ScriptArtifact` includes:
- immutable `script_artifact_id`;
- source fact-package digest;
- ordered narration segments;
- on-screen text segments;
- fact references for every factual clause;
- approved non-factual connective language;
- estimated spoken duration;
- generation metadata;
- validation status;
- semantic digest.

Every factual clause must resolve to one or more `FactRef` values.

## 5. Narrative graph

V1 supports:

```text
Hook
  -> Context
  -> Evidence
  -> Interpretation (source-authorized only)
  -> Recommendation/Takeaway (source-authorized only)
  -> CTA/Brand Close
```

Templates may omit nodes, but may not reorder required disclosure or evidence constraints in a way that creates misleading meaning.

## 6. Hook taxonomy

Allowed initial families:
- curiosity;
- contradiction;
- direct value proposition;
- line movement;
- data surprise;
- matchup question;
- weather/context alert;
- recap/result;
- educational explanation.

Hook wording remains creative metadata and is experimentable. Hook facts remain source-bound.

## 7. Numeric preservation

Numeric values are treated as typed tokens, not free prose. Production validation compares emitted numbers, percentages, odds, lines, dates, times, units, player/team identifiers, and directional changes against the bound fact package.

A mismatch fails closed unless the source contract explicitly permits a deterministic formatting transformation, for example:
- `0.632` -> `63.2%`;
- American odds formatting normalization;
- unit rounding under a versioned display policy.

## 8. Uncertainty language

Source confidence/uncertainty markers must propagate. Examples:
- `estimated` cannot become `confirmed`;
- `probable` cannot become `will`;
- `model favors` cannot become `guaranteed winner`;
- `lean` cannot become `best bet` unless source authority explicitly labels it so.

## 9. Multi-variant generation

Multiple scripts from one fact package are separate `CreativeVariantId`s but share the same source fact authority. Variants may differ in hook, pacing, order, CTA, voice cadence, and visual emphasis. They may not differ in the underlying factual/recommendation meaning unless the source package itself differs.

## 10. Deterministic fallbacks

If AI generation is unavailable or fails validation, the system can render a deterministic template script from typed fields. A provider outage must not force invention or publication without validation.

## 11. Human review

Supervised mode may require operator approval of script text. Production mode may later permit auto-approval only after script-validation certification thresholds are met. Approval is immutable evidence tied to exact script digest.

## 12. Security / prompt injection

Source text is data, not instructions. Sport-provided notes, external headlines, comments, metadata, or scraped text cannot alter system policy. Prompt construction must isolate authority policy from untrusted content.

## 13. Tests required before production

At minimum:
- number mutation rejection;
- odds-sign mutation rejection;
- team/player identity swap rejection;
- unsupported causal inference rejection;
- prohibited guarantee language rejection;
- uncertainty-strengthening rejection;
- fact omission policy tests;
- deterministic fallback tests;
- prompt-injection tests;
- identical-source multi-variant provenance tests.

## 14. Definition of done

V-6 is implementation-ready when typed contracts, validation rules, prompt boundaries, fallback behavior, and test vectors are implemented and conformance-reviewed.