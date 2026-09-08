# The Daily Line Video Engine — V-10 Render Runtime / Deployment Architecture V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define the replaceable rendering plane, with Remotion as the initial implementation, while keeping DLVE canonical identity independent of renderer/runtime vendor IDs.

## 2. Initial runtime

Remotion is the V1 rendering implementation because it supports parameterized React compositions, deterministic frame-driven animation, reusable components, server/local rendering, media layers, and programmatic video generation.

## 3. Renderer abstraction

`RendererAdapter` exposes:
- capability descriptor;
- validate render spec;
- estimate resources;
- render still/probe;
- render video;
- reconcile render job;
- cancel when supported;
- collect output metadata.

Remotion composition IDs, Chromium process IDs, Lambda IDs, container IDs, worker IDs, and cloud-job IDs are provenance only.

## 4. RenderJob identity

One logical `RenderJob` binds exact:
- `VideoRenderSpec` digest;
- template version;
- brand-system version;
- asset manifest digest;
- audio/caption artifacts;
- platform output profile;
- renderer release/image digest.

Retries are physical attempts under the same logical job when inputs are unchanged.

## 5. Execution environments

Support progression:
1. local development/Studio;
2. local/Docker CI render;
3. dedicated render worker;
4. scalable cloud/container/Lambda-compatible backend;
5. optional GPU/heavy-media worker classes.

## 6. Immutable build

Production rendering uses a pinned renderer release/container digest and dependency lock. No production render runs from an unpinned moving branch.

## 7. Resource classes

Profiles include CPU, memory, disk/temp space, concurrency, timeout, font/assets cache, and optional hardware acceleration. Scheduling remains generic TDLA resource policy; rendering estimates are DLVE evidence.

## 8. Determinism

Given identical render spec, assets, fonts, renderer release, and deterministic inputs, visual output should be reproducible within documented codec/runtime tolerance. Non-deterministic generated media is resolved before render and pinned by asset hash.

## 9. Output profiles

Each platform/output profile defines:
- width/height/aspect;
- fps;
- duration limits;
- codec/container;
- bitrate/quality policy;
- audio codec/rate;
- color/pixel-format settings;
- safe-zone profile;
- maximum file constraints.

## 10. Failure / reconciliation

Unknown render state is reconciled before blind redispatch when the backend may still be running. Partial files are never terminal success. Output hash and decode/QC evidence are required.

## 11. Security

Renderer workers receive least-privilege access to required assets/output paths. Remote URLs are constrained/validated to prevent SSRF-style access. Secrets do not enter render specs or manifests.

## 12. Tests

- composition schema validation;
- pinned-release reproducibility;
- worker crash/retry;
- lost render acknowledgement;
- partial output rejection;
- corrupt codec output rejection;
- missing font/asset fail-closed;
- high-concurrency resource limits;
- backend replacement identity preservation.

## 13. Definition of done

V-10 is implementation-ready when renderer adapter, immutable release binding, job identity, worker profiles, reconciliation, and output contracts are executable and tested.