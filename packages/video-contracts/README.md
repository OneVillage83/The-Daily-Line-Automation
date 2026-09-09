# @daily-line/video-contracts — VM-0

This package is the canonical machine-readable contract foundation for the Daily Line Video Engine (DLVE).

Architecture authority:

- `docs/video/V01_VIDEO_JOB_AND_FACT_CONTRACTS_V1.md`
- `docs/video/V00-V24_PRODUCTION_ARCHITECTURE_ADDENDUM_V1_1.md`
- `docs/adr/ADR-0008_PARAMETERIZED_VIDEO_RENDERER_AND_FACT_AUTHORITY.md`
- `docs/adr/ADR-0009_RIGHTS_FIRST_MEDIA_PROVENANCE_AND_NON_DOCUMENTARY_GENERATIVE_VISUALS.md`

## Authority model

The JSON Schemas in `schemas/` are the V1 wire-contract authority. Python and TypeScript must validate the same serialized contract against the same schema. Neither Pydantic nor TypeScript interfaces are permitted to acquire independent semantic meaning.

Remotion props are a renderer projection of `VideoRenderSpec`; they are not a replacement contract.

## Canonical V1 contract catalog

`schema-catalog.json` maps each supported `schema_version` to exactly one schema and one semantic digest field.

VM-0 implements:

- `PublishableFactPackage`
- `ContentCandidate`
- `CreativePlan`
- `ScriptPackage`
- `FactIntegrityReport`
- `AssetPlan`
- `AssetManifest`
- `VoicePackage`
- `CaptionPackage`
- `VideoRenderSpec`
- `RenderManifest`
- `VideoQcReport`
- `VideoPublicationPackage`
- `PlatformMetricSnapshot`

Descriptive aliases from later architecture prose (`ScriptArtifact`, `VoiceArtifact`, `CaptionArtifact`, `QCEvidenceBundle`, `PerformanceObservation`) MUST NOT become duplicate schemas or persistence models in V1.

## Validation layers

Validation is deliberately layered:

1. **JSON Schema** — shape, required fields, closed objects, enums, primitive types, timestamp formats, digest syntax.
2. **Canonical digest** — deterministic semantic identity and provenance binding.
3. **Single-document semantic rules** — unique IDs, reference closure, time-window ordering, protected-token preservation, generated-media rules, QC consistency, schedule validity.
4. **Cross-document scenario rules** — expiration at an explicit `as_of`, unresolved source conflicts, rights/platform compatibility, strict content-validity closure, QC-before-publication.
5. Later VM milestones add content/media/render-specific validators without weakening VM-0.

Schema validation alone does not grant publication authority.

## Python

The Python implementation uses JSON Schema Draft 2020-12 and the same canonicalization rules as Node.

Local validation:

```bash
PYTHONPATH=packages/video-contracts/python \
python packages/video-contracts/scripts/validate_fixtures.py
```

The package intentionally validates dictionaries against canonical schemas rather than maintaining hand-authored duplicate Pydantic semantics in VM-0. Future generated Pydantic/dataclass helpers must remain projections of the schemas.

## TypeScript

Runtime validation uses Ajv 2020 with the same schema files. Type declarations are generated from the schemas using `json-schema-to-typescript`.

```bash
cd packages/video-contracts
npm install
npm run check:digests
npm run generate:types
npm run typecheck
npm run check:schemas:ts
```

Generated declarations are build artifacts; the schemas remain authority.

## Compatibility/versioning

### Patch-level implementation changes

May fix validators, diagnostics, comments, or code without changing accepted/rejected wire semantics or canonical digests.

### Backward-compatible schema evolution

A new optional field is not added silently to an already-certified file. Create a new schema release/version, explicit compatibility transform if needed, new fixtures, and update the catalog. Consumers declare supported versions.

### Breaking changes

Any change that can alter required fields, interpretation, canonical ordering, digest behavior, enum meaning, numeric representation, protected-token semantics, rights/QC/publication authority, or source-binding meaning requires a new contract major schema version or an explicitly certified superseding version.

### Unknown fields

V1 production contracts are closed (`additionalProperties: false`) at authority-bearing object boundaries. Unknown fields fail closed rather than being silently ignored.

### Unknown enum/schema versions

Unknown required enum values and unknown `schema_version` values fail closed. Version translation requires an explicit tested transform; consumers may not guess.

## Golden fixtures

`fixtures/valid/end-to-end/` is a coherent synthetic single-pick contract chain. It contains no live sport claim and exists only to prove contracts.

`fixtures/invalid/` contains schema/domain negatives.

`fixtures/scenarios/` contains semantic/cross-artifact cases with exact expected error-code sets:

- protected numeric mutation;
- expired package/fact;
- unresolved composite-source conflict;
- asset/platform rights mismatch;
- publication with failed QC;
- `content_valid_until` later than strict source/rights validity;
- one fully valid end-to-end scenario.

These fixtures are permanent compatibility evidence. Fixing code to make a negative fixture pass without a contract-version decision is a regression.

## Canonicalization

See `CANONICALIZATION.md`. Fractional business values use decimal strings. Canonical JSON numbers are safe integers only. SHA-256 digests exclude only the document's own digest field and retain referenced upstream digests.

## CI gate

`.github/workflows/video-contracts-vm0.yml` is the VM-0 contract gate. It runs Python fixture validation and Node/TypeScript digest/schema/type-generation checks. VM-1 must not weaken or bypass this gate.

## Ownership boundary

This package is presentation-contract infrastructure. It does not infer sport truth. `PublishableFactPackage` is the sport-authorized input boundary; DLVE validators preserve and constrain that authority rather than re-deriving it.
