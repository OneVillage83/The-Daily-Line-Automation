# The Daily Line Video Engine — V-18 Security / Secrets / Service Identity V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define least-privilege security for AI/media providers, render workers, object storage, publication handoff, and analytics connectors.

## 2. Secret rule

Secrets are referenced by logical names and resolved at runtime. Secret values never enter Git, VideoJob/RenderSpec digests, normal logs, captions, prompts unless absolutely required by provider transport, or publication artifacts.

## 3. Service identities

Separate identities should exist by function/environment where practical:
- script/media generation;
- render worker;
- object storage writer/reader;
- analytics collector;
- publication service (A-18);
- operator dashboard.

Production and non-production credentials are isolated.

## 4. Least privilege

Render workers need read access only to required inputs and write access only to assigned output namespace. Script/image workers do not receive social-platform publishing credentials.

## 5. Network controls

Remote asset fetch is allowlisted/proxied or otherwise validated. Internal/cloud metadata/private-network addresses are denied to rendering/content fetch paths unless explicitly required and isolated.

## 6. Untrusted content

Prompt injection, malicious filenames, crafted media, metadata, SVG/HTML, and external URLs are untrusted inputs. Media processing runs in constrained workers with validation and resource limits.

## 7. Supply chain

Production builds pin dependencies, verify locks, scan dependencies/images, and retain release provenance. Fonts/assets/packages from unknown origins are not introduced ad hoc.

## 8. Access/audit

Operator approvals, production-mode changes, kill-switch actions, provider config, rights overrides, and publication-authority changes require authenticated auditable identity.

## 9. Credential incidents

Suspected exposure requires immediate disable/rotation plus documented incident and impact analysis. Historical manifests retain logical secret references, never exposed values.

## 10. Tests

- secret redaction;
- environment isolation;
- least-privilege storage access;
- SSRF/private-IP blocking;
- malicious media handling;
- prompt injection;
- unauthorized production approval;
- dependency/image scanning.

## 11. Definition of done

V-18 is implementation-ready when every external capability has explicit authentication, least privilege, environment isolation, audit, and incident response.