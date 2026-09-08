# The Daily Line Video Engine — V-12 Persistence / Provenance Ledger V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define the durable identity and provenance records required to reconstruct any Daily Line video from sport facts through publication and later analytics.

## 2. Persistence authority

TDLA PostgreSQL is the planned authoritative operational store. Large media objects belong in object storage behind immutable/content-addressed references. Exact DDL must be implemented consistently with A-13 persistence architecture.

## 3. Required durable entities

- VideoStoryCandidate;
- PublishableFactPackageRef;
- VideoJob;
- CreativeVariant;
- ScriptArtifact;
- AssetRecord/AssetManifest;
- VoiceArtifact;
- CaptionArtifact;
- VideoRenderSpec;
- RenderJob / RenderAttempt;
- RenderArtifact;
- QCEvidenceBundle;
- VideoPublicationPackage;
- publication receipt references;
- PerformanceObservation;
- ExperimentAssignment;
- approval/operator evidence;
- supersession/retraction records.

## 4. Immutable history

Completed artifacts/evidence are append-only. Corrections create new revisions with lineage. A changed script, asset, render, or source fact package never mutates historical evidence in place.

## 5. Digests

Semantic records use schema-versioned canonical serialization and cryptographic digests. Raw media uses content hashes. Presentation-only database fields do not silently change semantic identity.

## 6. Provenance chain

A published post must resolve:

```text
platform publication receipt
-> VideoPublicationPackage
-> QCEvidenceBundle
-> RenderArtifact/RenderSpec
-> Script/Caption/Voice/Asset manifests
-> PublishableFactPackage
-> sport pipeline run/artifact provenance
```

## 7. Retractions/corrections

If source facts are corrected after publication, the original publication remains historical evidence. A correction/retraction workflow creates new state and, if needed, a replacement publication package.

## 8. Deletion/privacy

Operational deletion requests must preserve legally/operationally required audit metadata while removing media or personal data when policy requires. Exact retention/privacy mechanics belong to security/legal policy.

## 9. Re-render semantics

- same creative semantics + runtime retry: same logical render job, new attempt;
- same content + different platform encode: distinct output profile artifact under related job/variant;
- changed hook/script/asset: new creative/render variant;
- corrected source facts: new fact-package revision and new lineage;
- historical reproduction: replay;
- changed creative/runtime for comparison: reprocess/experiment lineage as declared.

## 10. Tests

- lineage reconstruction;
- immutable historical record;
- digest canonicalization;
- correction/retraction lineage;
- same-vs-new render identity;
- object missing/hash mismatch;
- publication-to-source trace.

## 11. Definition of done

V-12 is implementation-ready when a published video can be traced deterministically to every material source and transformation without relying on chat history, filenames, or provider dashboards.