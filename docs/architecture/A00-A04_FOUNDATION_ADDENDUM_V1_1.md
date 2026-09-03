# A-0 through A-4 Foundation Addendum V1.1 — Nested Lifecycle / Cross-Repository Boundary Clarification

Date: 2026-09-02 (America/Los_Angeles)  
Status: **GOVERNING ADDENDUM — paired with A00-A04_AUTOMATION_FOUNDATION_V1.md**

## Why this addendum exists

The A-0 through A-4 certification review compared TDLA's proposed ownership with current Daily-Data-Core ownership documentation and the earlier Daily-NFL F-0 through F-4 architecture.

A terminology ambiguity was identified:

- Daily-Data-Core's current ownership contract clearly owns shared provider/acquisition infrastructure and immutable evidence.
- an earlier Daily-NFL architecture document also lists a generic `run/job lifecycle` among Core responsibilities;
- Daily-MLB's current manual collector exposes its own service `run_id` / job lifecycle for a concrete collection operation;
- TDLA A-1 says TDLA owns workflow/stage orchestration lifecycle.

These are compatible only if the lifecycle layers are explicitly distinguished. TDLA must not replace or redefine the internal acquisition/job lifecycle of DDC or a certified sport pipeline.

## Governing clarification

### 1. TDLA owns the outer automation lifecycle

TDLA owns **orchestration intent and execution history across systems**, including:

- automation plan;
- workflow run;
- stage run;
- physical orchestration attempt;
- scheduling/trigger/dependency state;
- operator action;
- outer retry/idempotency policy;
- publication orchestration;
- automation certification state.

A TDLA run answers: **"Why was this production operation expected to happen, under which plan/release/configuration, what did TDLA dispatch, and what happened next?"**

### 2. DDC may own internal shared acquisition/provider lifecycles

DDC may define and persist job/request/run identity necessary to its shared acquisition/provider responsibilities, such as:

- provider HTTP attempts;
- shared collection/acquisition runs;
- raw-evidence capture sessions;
- provider retry/diagnostic records;
- other DDC-owned internal execution state.

A DDC acquisition run answers: **"How was this shared provider/fact acquisition performed and evidenced?"**

TDLA does not recreate this evidence or take ownership of the internal DDC lifecycle.

### 3. Sport repositories may own internal pipeline/job lifecycles

A certified sport executable/service may expose internal job/run identity necessary to execute sport logic. For example, a Daily-MLB service can accept a request and return a sport-service job ID that later resolves to an artifact.

TDLA may invoke and monitor that interface, but the sport's internal job ID remains a **child/external execution reference**, not the canonical TDLA run ID.

### 4. Nested lifecycle rule

One production operation may therefore contain nested identities:

```text
TDLA WorkflowRun
    └── TDLA StageRun
        └── TDLA RunAttempt
            └── Sport service/job reference
                └── DDC acquisition run(s)
                    └── provider request/attempt evidence
```

Each layer keeps the authority appropriate to its domain.

TDLA's execution envelope may reference child IDs/artifact hashes/provenance IDs supplied by lower layers, but it must not silently re-key or overwrite them.

### 5. Retry ownership must be composable

Nested systems may each retry operations at their own layer. Therefore:

- TDLA retries the outer logical stage according to TDLA policy;
- a sport service may retry internal sport operations according to its certified contract;
- DDC/provider transport may retry transient acquisition calls according to DDC policy.

The fact that an inner layer retried does not automatically mean TDLA creates a new attempt.

A new TDLA attempt occurs only when TDLA re-dispatches the outer execution after the prior TDLA attempt fails/is lost/times out according to the outer contract.

### 6. Idempotency must span the boundary intentionally

The Sport Automation Adapter contract in A-5/A-6 must define how TDLA passes a stable outer idempotency/execution reference when the sport interface supports it.

Sport/DDC internal operations may have their own identities. No layer may assume another layer's retry mechanism is sufficient to prevent duplicate user-visible side effects.

### 7. Success authority remains layered

A child sport/DDC job reporting success is evidence, not automatically sufficient for TDLA stage success.

TDLA stage success requires its declared output contract to validate, while sport semantic success remains sport-owned and acquisition evidence remains DDC-owned.

### 8. Cross-layer failure classification

TDLA may store normalized outer classifications such as `CHILD_EXECUTION_FAILED`, `DEPENDENCY_UNAVAILABLE`, or `OUTPUT_CONTRACT_INVALID`, plus the referenced child diagnostic.

It must not rewrite a DDC/provider or sport-specific failure into a different domain claim without the owning adapter/contract providing that classification.

## Authority effect

This addendum refines A-1 and A-3 terminology. It does not move shared acquisition/provider ownership out of DDC and does not move sport intelligence out of Daily-* repositories.

Where `A00-A04_AUTOMATION_FOUNDATION_V1.md` says TDLA owns lifecycle/state, interpret that as **TDLA outer automation lifecycle/state** under this addendum.

## Required downstream consequences

A-5 and A-6 must include:

- child/external execution-reference fields;
- adapter idempotency/reference propagation rules;
- separation of outer attempt state from inner job state;
- result/artifact validation boundaries;
- explicit timeout/cancellation semantics for child jobs.

A-11 must later define how nested retry and idempotency policies compose.

A-13 must preserve cross-layer provenance references without copying ownership.

## Supersession

This V1.1 addendum remains authoritative unless a later version explicitly supersedes it. The original V1 foundation remains historical/governing for all unaffected language.
