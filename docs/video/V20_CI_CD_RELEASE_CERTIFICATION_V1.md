# The Daily Line Video Engine — V-20 CI/CD / Release / Certification V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define how video-engine code, templates, brand assets, schemas, and render runtime become immutable production releases.

## 2. Release units

Track independently but compatibly:
- contract/schema package;
- video-renderer application;
- template library;
- brand-system assets/tokens;
- prompt/policy bundle;
- platform output profiles;
- pronunciation/caption policies;
- optional provider adapters.

A production `RendererReleaseManifest` binds exact compatible versions/digests.

## 3. CI gates

At minimum:
- TypeScript typecheck;
- lint/format policy;
- unit tests;
- schema/contract compatibility tests;
- deterministic canonicalization tests;
- component tests;
- render smoke tests;
- golden still/video checks;
- caption/overflow/accessibility checks;
- media decode/QC tests;
- security/dependency scan;
- rights metadata completeness for bundled assets.

## 4. Golden fixtures

Maintain representative synthetic fixtures for MLB/NFL/NCAAF-style content, long names, extreme odds, no-voice, weather, line movement, results, multi-stat explanations, and failure cases. Fixtures must not require live provider access for core CI.

## 5. Visual regression

Use deterministic still frames/key checkpoints or approved perceptual comparison. Expected changes require explicit baseline update and change note; visual drift cannot silently pass.

## 6. Compatibility

Schema/template/brand/runtime compatibility is declared. Breaking changes require versioning/migration plan; old published artifacts retain original release provenance.

## 7. Promotion

Suggested environments:
`dev -> test -> shadow -> supervised -> production`.
Production promotion requires successful certification evidence for affected templates/platform profiles.

## 8. Rollback

Rollback selects a prior immutable release; it does not rewrite history. In-flight jobs either finish under their pinned release or are explicitly superseded/reprocessed according to policy.

## 9. Tests

- old fixture with new schema compatibility;
- visual regression detection;
- missing bundled asset;
- dependency mismatch;
- release-manifest digest;
- rollback to prior renderer;
- mixed-version rejection.

## 10. Definition of done

V-20 is implementation-ready when every production render identifies an immutable, CI-certified release manifest reproducible from source and locked dependencies.