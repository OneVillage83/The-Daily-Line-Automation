# DLVE Canonical JSON and Digest Rules — VM-0 V1

Status: implementation authority for `packages/video-contracts` V1 contracts.

## Purpose

DLVE contract identities must be identical when the same semantic document is produced or consumed by Python, TypeScript/JavaScript, a future database exporter, or another compatible runtime. Native object ordering, whitespace, floating-point formatting, or serializer defaults must never create different business identities.

## Digest algorithm

For every cataloged V1 contract:

1. validate the document against the exact `schema_version` JSON Schema;
2. remove only that contract's own digest field from a deep copy;
3. retain all referenced upstream IDs and digests;
4. normalize schema-declared semantic-set arrays;
5. sort object keys by the lexicographic order of their UTF-8 byte sequences;
6. serialize as UTF-8 JSON with no BOM and no insignificant whitespace;
7. hash the serialized bytes with SHA-256;
8. encode the result as `sha256:<64 lowercase hex characters>`.

The digest is a semantic contract digest, not a file hash. Pretty-printing a JSON file does not change it.

## Numeric domain

Canonical V1 contract JSON permits only:

- strings;
- booleans;
- null;
- integers in JavaScript's exact safe range `[-9007199254740991, 9007199254740991]`;
- arrays/objects composed of those values.

Fractional/decimal business values MUST be strings using an explicit schema format, for example:

- `"0.618"`
- `"61.8"`
- `"9800.5"`

This rule deliberately avoids cross-runtime floating-point stringification ambiguity. Display values such as `"61.8%"`, `"-2.5"`, and `"+120"` remain protected strings.

## Semantic-set normalization

Arrays that represent ordering are left in their declared order. Examples: scene plans, script segments, caption cues.

Arrays that represent sets are normalized before hashing. V1 examples include reference sets, allowed platform sets, claim/fact reference sets, experiment refs, allowed source classes, rights territories, use classes, and SFX refs.

Object collections whose order is not semantic use stable identity sort keys. V1 includes:

- approved facts by `fact_id`;
- approved claims by `claim_id`;
- approved explanations by `explanation_id`;
- package bindings by `(ref,digest)`;
- assets by `asset_id`;
- platform intents by `(platform,target_account_ref,publish_mode)`;
- QC gates by `(gate_class,code)`;
- normalized metrics by `(metric_name,normalization_version)`.

The normalization registry exists in both `python/dlve_contracts/canonical.py` and `typescript/src/canonical.ts`. Any change to this registry changes semantic identity behavior and therefore requires a versioned contract decision and new golden vectors.

## Strings

Strings are Unicode, encoded as UTF-8. Unpaired UTF-16 surrogate code points are forbidden. JSON escaping is limited to serializer-required escaping; non-ASCII text is preserved as Unicode rather than converted to ASCII escape sequences.

## Digest field map

The authoritative mapping is implemented in code and mirrored by `schema-catalog.json`. A contract's own digest field is excluded from its digest; nested/upstream digest fields are included so provenance bindings participate in downstream identity.

## Golden vectors

`fixtures/valid/end-to-end/` contains one valid V1 instance of every canonical contract. `fixtures/valid/digest-stability.json` proves that reordering semantic-set collections does not change the digest.

Python and Node independently recompute every golden digest. A release cannot change the expected digest vectors without an intentional schema/canonicalization version change.
