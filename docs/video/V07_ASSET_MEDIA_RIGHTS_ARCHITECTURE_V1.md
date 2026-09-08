# The Daily Line Video Engine — V-7 Asset / Media / Rights Architecture V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define how DLVE discovers, generates, caches, licenses, validates, and reuses visual/audio assets while preserving provenance and publication rights.

## 2. Asset classes

- first-party brand assets;
- first-party generated graphics;
- AI-generated still images;
- licensed stock still images;
- licensed stock motion/video;
- licensed music beds;
- licensed sound effects;
- team/league/public assets explicitly authorized for use;
- data-generated charts/graphics;
- operator-supplied assets.

## 3. Canonical AssetRecord

Each asset has:
- `asset_id`;
- content hash;
- media type;
- dimensions/duration/codec where applicable;
- source/provider;
- source locator/reference;
- acquisition/generation timestamp;
- license/usage class;
- license evidence reference;
- expiration/restriction fields;
- generated prompt/model/version where applicable;
- person/team/brand sensitivity tags;
- allowed platforms/territories/use modes if restricted;
- derivative/parent lineage;
- QC status;
- retention policy.

## 4. Rights-first publication rule

No production publication may reference an asset lacking an allowed-use determination for the exact use context. `downloaded` or `publicly accessible` does not mean `publishable`.

## 5. Generated-media rule

Generated media is preferred for generic cinematic context when it reduces licensing complexity, but generated imagery must not be used to fabricate real events, statistics, injuries, quotes, or exact documentary evidence.

Generated depictions of real athletes/public figures require explicit policy approval and provenance. Default production strategy is generic sport imagery, first-party graphics, or properly licensed authentic media.

## 6. Stock selection

Stock assets are selected using semantic tags and versioned ranking rules. Asset selection cannot imply a factual event that did not occur. Example: generic rain footage may illustrate weather context, but cannot be represented as live footage from a stadium unless it actually is.

## 7. Asset cache

Reusable assets are content-addressed. Cache lookup occurs before new generation/acquisition. Cache keys include semantic class, aspect suitability, rights status, and content hash; not merely filename.

## 8. Derivatives

Crop, color treatment, blur, parallax layers, masks, thumbnails, and transcodes are derivative assets with parent lineage and their own hashes. Derivatives inherit restrictions unless a license says otherwise.

## 9. AI prompt provenance

For generated assets retain:
- prompt template/version;
- resolved prompt hash;
- model/provider/version;
- seed when available;
- generation settings;
- moderation/safety result;
- generated file hash;
- parent/reference assets when used.

## 10. Watermarks / unsafe stock

Watermarked preview assets are non-production. Unknown-license internet imagery is non-production by default.

## 11. Failure modes

If preferred assets are unavailable:
1. reusable first-party/data graphic;
2. cached licensed/generated alternative;
3. new approved generated still;
4. licensed stock fallback;
5. data-only visual template.

The system must not bypass rights validation to meet a posting deadline.

## 12. Retention

License evidence and asset provenance must outlive the public publication according to legal/operational retention policy. Source assets may have separate retention rules from manifests/provenance.

## 13. Tests

- expired license rejection;
- unsupported platform restriction rejection;
- unknown-license rejection;
- derivative lineage preservation;
- duplicate content-addressed cache reuse;
- generated-prompt provenance;
- misleading-live-footage labeling prevention;
- watermarked preview rejection.

## 14. Definition of done

V-7 is implementation-ready when the asset registry, rights policy, lineage contract, fallback order, and publication gate are implemented and validated.