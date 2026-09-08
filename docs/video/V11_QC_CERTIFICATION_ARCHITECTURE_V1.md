# The Daily Line Video Engine — V-11 Quality Control / Certification Architecture V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define mandatory automated and human quality gates between rendered media and publication authority.

## 2. QC layers

1. contract validation;
2. fact/script validation;
3. asset/rights validation;
4. render technical validation;
5. visual layout validation;
6. audio validation;
7. caption/accessibility validation;
8. platform-profile validation;
9. policy/disclosure validation;
10. optional human approval.

## 3. QCEvidenceBundle

Contains immutable results for every applicable gate, tool/version, input digest, timestamps, findings, severity, and final disposition.

## 4. Dispositions

- `PASS`;
- `PASS_WITH_APPROVED_WARNING`;
- `FAIL_RETRYABLE`;
- `FAIL_CONTENT`;
- `FAIL_RIGHTS`;
- `FAIL_POLICY`;
- `REQUIRES_HUMAN_REVIEW`.

A renderer success status is not QC success.

## 5. Technical checks

At minimum:
- file exists and hash captured;
- media decodes end-to-end;
- expected width/height/fps/duration;
- audio track expectations;
- black/blank frame checks;
- frozen/repeated-frame anomaly checks where appropriate;
- corruption/truncation;
- file-size/profile limits.

## 6. Visual checks

- text within safe zones;
- no clipped/overflow text;
- logo/brand presence per template;
- contrast/readability;
- asset aspect/cropping correctness;
- no placeholder/debug content;
- required pick/result/disclosure visible;
- no unintended blank/transparent regions.

## 7. Semantic checks

Compare rendered/on-screen text and captions against approved script/facts. Automated extraction may be used as secondary QC, but canonical expected text comes from the render spec.

## 8. Human review modes

- `SHADOW`: never customer-visible;
- `SUPERVISED`: publication requires explicit approval;
- `AUTO_PRODUCTION`: publication may proceed on certified automated gates.

Graduation to auto-production is per template/platform/sport profile, not a blanket switch.

## 9. Certification

A template/version may receive `PRODUCTION-CERTIFIED` status only after defined golden fixtures, error cases, cross-platform renders, rights checks, and operator review pass. Any material template/brand/runtime change can require recertification.

## 10. Fail closed

Unknown fact provenance, unknown rights, missing mandatory QC evidence, or stale source authority blocks publication.

## 11. Tests

Maintain golden videos/stills and failure fixtures for text overflow, invalid odds, missing logo, missing caption, corrupt audio, blank render, restricted asset, stale source, and platform-spec mismatch.

## 12. Definition of done

V-11 is implementation-ready when every publication candidate has machine-readable QC evidence and certification policy can prove why a video was or was not eligible to publish.