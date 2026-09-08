# DLVE V-0 through V-24 Production Architecture Addendum V1.1

Status: ARCHITECTURE-CERTIFIED WITH V1 BASELINE
Date: 2026-09-08

This addendum resolves cross-document terminology and production edge cases found during the final V-0 through V-24 conformance review. It is authoritative together with the V1 documents. Where this addendum is more specific, it controls for DLVE V1.x.

## 1. Parent-authority precedence

DLVE specializes TDLA but never overrides it. Current and future certified A-sections control shared orchestration concerns including retry/idempotency, persistence, publication side effects, operator authority, security, deployment, and adaptive automation. DLVE contracts must conform through explicit versioned updates if a later A-section is stricter.

This dependency does not make DLVE architecture incomplete: DLVE defines its exact subsystem boundary and handoff while intentionally leaving shared platform mechanics to their owner.

## 2. Canonical contract vocabulary

The V-1 external/wire names are canonical for V1:

- `ScriptPackage` — canonical scripted-language artifact. Later prose term `ScriptArtifact` means the same conceptual artifact and must not become a second schema.
- `VoicePackage` — canonical narration artifact. `VoiceArtifact` is descriptive prose only.
- `CaptionPackage` — canonical caption artifact. `CaptionArtifact` is descriptive prose only.
- `VideoQcReport` — canonical QC evidence contract. `QCEvidenceBundle` is descriptive/grouping prose only unless a future major schema explicitly replaces it.
- `PlatformMetricSnapshot` — canonical platform performance observation. `PerformanceObservation` is descriptive prose only.
- `RenderManifest` — canonical completed-render manifest.
- `RenderArtifactId` — content-addressed media artifact identity referenced by the render manifest.
- `VideoPublicationPackage` — canonical DLVE-to-A-18 handoff.

Implementation MUST NOT create duplicate persistence models for the descriptive aliases.

## 3. Logical render job vs TDLA execution identity

`RenderJob` is a DLVE logical operation over one exact `VideoRenderSpec` + output profile + renderer release authority. It does not replace TDLA `StageRun` or A-11 logical operation identity.

Required mapping:

```text
TDLA StageRun / logical operation
        -> one DLVE RenderJob semantic ref
        -> one or more A-11-authorized RunAttempts
        -> A-10 execution envelopes / backend submissions
        -> RenderManifest / RenderArtifact
```

A retry with unchanged semantic inputs remains the same RenderJob and same TDLA logical operation but a new physical RunAttempt when A-11 authorizes it. Changed creative/render semantics create a new render-spec/variant lineage rather than masquerading as retry.

## 4. Composite fact packages and conflicts

A `VideoStoryId` may reference multiple publishable packages only when their authorities and compatibility are explicit.

DLVE MUST NOT reconcile conflicting sport truth. If two source packages disagree about a protected value, recommendation state, event identity, or required explanation and no upstream authority declares precedence/supersession, candidate assembly fails closed.

Merging facts by matching team name, date, market label, or provider ID is prohibited.

## 5. Effective validity / freshness closure

The publication candidate's effective validity boundary is the strictest applicable bound across:
- publishable package expiry;
- referenced fact/claim/explanation validity;
- embargo/release policy;
- event/cutoff policy when declared;
- asset/license expiry;
- compliance/disclaimer policy validity;
- publication-package expiry.

The effective `content_valid_until` cannot be later than the minimum controlling bound.

A successful earlier render does not preserve publication authority after this boundary.

## 6. Corrections / supersession

If a source package is corrected or superseded before publication, the old package cannot remain current publication authority merely because its original expiry has not passed. Current-authority/retraction evidence invalidates affected pending packages.

After publication, historical evidence is immutable. A correction/retraction creates explicit lineaged action and, when appropriate, a replacement publication package.

## 7. Candidate-ranking boundary

DLVE generic candidate ranking may use declared metadata such as:
- upstream content-priority hint;
- urgency/expiry;
- platform/account cadence policy;
- topic/category diversity;
- already-measured creative performance for equivalent presentation choices;
- operator/editorial priority;
- cost/resource availability.

DLVE may not inspect raw sport metrics and infer which team/player/market is a better bet or more important because of sport-specific meaning.

## 8. Results-audit completeness

A story represented as a complete Daily Line results/audit report requires an upstream `evaluation_set_ref` or equivalent completeness authority identifying the expected recommendation/outcome population.

DLVE cannot remove losses, pushes, avoids, or unfavorable outcomes from a complete-audit story to improve performance metrics. A separate editorial story such as `three notable wins` may exist only when accurately labeled and not presented as the complete record.

## 9. Script factual-clause closure

Every factual clause in hook, body, pick reveal, CTA, post copy, thumbnail text, or generated metadata must trace to source authority. Non-factual brand/transition language is explicitly typed.

A statement becomes factual based on meaning, not where it appears. A hook is not exempt from the fact-integrity gate.

## 10. Protected entity tokens

Protected-token validation applies to:
- probabilities;
- odds;
- spreads/totals;
- scores/records;
- weather quantities;
- dates/times;
- team/player/event labels when source presentation requires exact mapping;
- directional movement (`-2.5 -> -3.5`, rising/falling, home/away);
- units and sign.

Formatting policies are explicit and versioned.

## 11. Asset rights revalidation

Asset cache presence does not imply current publishing rights. Rights status is revalidated for the exact platform/account/territory/use class at package assembly and again at the A-18 pre-publication boundary when policy requires.

Derived/cropped/transcoded assets inherit parent restrictions unless rights evidence explicitly permits otherwise.

## 12. Documentary-evidence rule for generated visuals

AI-generated/generic stock media may illustrate a concept but cannot be described or visually labeled as authentic footage/photo evidence of a specific event unless it is authentic licensed source media.

Generated media must not fabricate injuries, weather at a venue, scoreboard outcomes, quotes, player actions, or other documentary evidence.

## 13. Team/league marks and identifiable people

Logo, uniform, league/team mark, athlete/public-figure likeness, and voice usage are rights/policy-sensitive asset classes. Availability on the internet or ability to generate a likeness is not use authority.

Default reusable backgrounds should remain generic/first-party unless explicit rights policy permits identifiable marks/people.

## 14. Voice timing and content fitting

Measured narration duration may expand/contract scene timing within declared template bounds. Mandatory facts/disclosures cannot be silently removed or sped beyond intelligibility to hit a duration target.

If content cannot fit safely, choose another certified duration/template variant or fail candidate generation.

## 15. Caption/QC authority

The approved script is expected-text authority for generated narration. Speech transcription/OCR may be secondary QC evidence, not the source of truth that can rewrite the script.

Text overflow/collision resolution uses declared layout variants. Silent clipping or omission is prohibited.

## 16. Platform profile versioning

Codec, duration, safe-zone, cover, metadata, analytics mapping, and disclosure settings are versioned platform profiles/adapters because platform requirements change. A profile update does not mutate historical render/publication evidence.

## 17. Manual publication receipts

Before API automation is certified, a manual publication package may be used. Manual posting must record where practical:
- operator identity;
- publication-package digest;
- platform/account;
- external post URL/ID or verifiable receipt;
- posted timestamp;
- deviations from requested copy/timing;
- correction/delete evidence if later applicable.

Manual action is not permission to bypass stale-fact, rights, QC, or compliance gates.

## 18. Analytics semantics

Missing platform metrics are `unknown/not exposed`, not zero. Normalized metrics preserve source definition and adapter version. A platform schema/definition change creates a new mapping version.

Prediction performance and creative performance remain separate dimensions.

## 19. Experiment assignment and promotion

Experiment assignment is immutable before publication. Facts/recommendations/disclosures/rights/QC requirements are outside the creative action space.

Experiment results generate evidence/recommendations. Before A-24 certification, default-policy changes require explicit reviewed configuration/release change.

## 20. Adaptive action-space closure

Any future automatic selector receives an enumerated set of already-certified actions. It cannot construct arbitrary template code, prompts, claims, disclosures, or asset-rights overrides during production selection.

A static certified fallback and kill switch are mandatory.

## 21. Degraded-mode labeling

Fallback from generated imagery/voice/music to data-only/caption-led rendering is an explicit creative variant attribute. It is not a hidden mutation of an already-assigned experiment variant.

Where an experiment requires comparable treatment, fallback may invalidate/exclude the observation according to predeclared analysis policy.

## 22. Cost does not outrank safety

Hard resource pressure may skip/defer or choose an allowed cheaper variant, but cannot bypass fact integrity, rights, compliance, accessibility requirements, or mandatory QC.

## 23. Security closure

Source text, stock metadata, prompts, URLs, SVG/HTML/media metadata, filenames, and provider responses are untrusted data. They cannot alter authority policy. Remote-media/network access and render execution are sandboxed/validated under V-18/A-20.

## 24. Retention / deletion closure

Deleting a large media object for policy/cost reasons does not erase the immutable identity/provenance record required to explain a historical publication, subject to applicable privacy/legal requirements. Tombstone/deletion evidence is explicit.

## 25. Architecture certification decision

After application of this addendum and the 120-case stress review recorded in `docs/implementation/DLVE_V00-V24_ARCHITECTURE_CONFORMANCE_REVIEW_20260908.md`, V-0 through V-24 are **ARCHITECTURE-CERTIFIED as V1 + V1.1**.

This grants architecture authority only. No DLVE implementation or auto-publication authority is granted.

The first implementation milestone is VM-0: canonical JSON Schemas, cross-language contract parity, canonical digests, and golden fixtures.