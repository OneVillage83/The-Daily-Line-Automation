# The Daily Line Video Engine — V-13 Publication / Distribution Contract V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define the handoff from certified video artifacts to TDLA A-18 publication/distribution without making DLVE own platform-side-effect identity.

## 2. Boundary

DLVE produces an immutable `VideoPublicationPackage`. A-18 owns authenticated platform submission, scheduling, retries, reconciliation, receipts, edits/deletes where supported, and duplicate-side-effect prevention.

## 3. VideoPublicationPackage

Includes:
- package id/version/digest;
- render artifact ref/hash;
- thumbnail/cover refs where applicable;
- caption/post-copy artifact;
- hashtags/tags metadata;
- platform target profile(s);
- requested publish window;
- source fact provenance;
- script/asset/QC refs;
- disclosure/compliance metadata;
- experiment assignment if any;
- allowed publication modes;
- expiration/staleness boundary.

## 4. Platform adapters

Platform-native post IDs and upload session IDs remain A-18 provenance. DLVE never assumes TikTok/Instagram/YouTube APIs or upload semantics are identical.

## 5. Staleness before publish

Immediately before irreversible publish, current source-fact/rights/policy validity must be rechecked according to package rules. A video rendered earlier can become ineligible to publish.

## 6. Scheduling

Requested posting time is intent, not unconditional side-effect authority. Late/missed-window policy can skip, reschedule, require review, or publish if still valid; it cannot bypass freshness/rights/QC gates.

## 7. Caption/post copy

Social copy is a separate approved artifact linked to the same facts. Platform-specific truncation/hashtags/links are deterministic transformations or independently validated creative variants.

## 8. Duplicate protection

Publication must use stable logical effect identity under A-11/A-18. Lost acknowledgement is reconciled before creating another post.

## 9. Retraction/correction

A correction may produce a new package and explicit replace/retract workflow. Historical receipts remain auditable.

## 10. Manual export

Until platform APIs are certified, DLVE may produce a manual publication bundle containing video, cover, caption, provenance/QC summary, and exact posting instructions. Manual posting still records operator/receipt evidence when possible.

## 11. Tests

- stale-before-publish block;
- duplicate acknowledgement loss;
- platform-specific metadata;
- expired asset rights;
- manual package completeness;
- correction/retraction lineage;
- cross-platform package separation.

## 12. Definition of done

V-13 is implementation-ready when DLVE can hand A-18 a self-contained, immutable, validated package without embedding platform side-effect logic into the renderer.