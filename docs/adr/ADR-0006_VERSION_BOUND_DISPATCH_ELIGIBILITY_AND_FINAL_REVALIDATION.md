# ADR-0006 — Version-Bound Dispatch Eligibility and Final Revalidation

Date: 2026-09-05  
Status: **ACCEPTED**

## Context

A-9 must bridge a distributed-system gap between eligibility evaluation and actual dispatch.

A stage can be fully eligible at one instant and become stale immediately afterward because of:

- sport schedule/scope revision;
- resolved plan supersession;
- readiness expiration or new readiness authority;
- upstream output supersession/retraction;
- deadline/window expiry;
- policy/config/mode authority change.

A mutable `ready=true` flag is unsafe because it loses the exact evidence/authority under which readiness was established.

A simple evaluation record alone is also insufficient unless the dispatcher can prove that the evaluation still refers to current authority.

The architecture needs a durable handoff from A-9 to A-10/A-11 without pretending that distributed state cannot change between check and use.

## Decision

TDLA will use an explicit immutable `DispatchEligibilityGrant` as the handoff from A-9 to A-10/A-11.

The grant:

- references the exact immutable A-9 eligibility evaluation/digest;
- binds the exact resolved-plan/stage-materialization/scope/schedule/dependency/readiness/environment/mode/policy authority used by that evaluation;
- is bounded by the earliest applicable validity/expiry condition;
- is non-transferable across stages, scopes, revisions, replay/reprocess lineages, environments, or modes;
- is **not a bearer capability** and does not by itself authorize execution;
- must be revalidated against current authoritative heads/revisions/digests before dispatch;
- fails closed if any execution-affecting witness changed or validity expired;
- may require immediate inline revalidation when no safe TTL exists.

The canonical sequence is:

```text
A-9 EligibilityEvaluation
        |
        v
DispatchEligibilityGrant
        |
        v
A-10/A-11 verify current authority + validity + idempotency
        |
        +-- stale/changed --> no dispatch; request reevaluation
        |
        +-- current ------> continue dispatch path
```

A grant is audit/reconciliation evidence showing *why dispatch was considered permissible*, not permission that overrides current state.

## Why the grant exists if revalidation is still required

The grant provides a stable handoff identity and immutable proof capsule containing the exact A-9 evidence set.

Without it, A-10/A-11 would need to reconstruct which eligibility result they were consuming from mutable/process-local state.

The grant allows TDLA to answer later:

- which eligibility evaluation led to this dispatch attempt;
- which plan/scope/schedule/dependency/readiness versions were considered current;
- whether the grant was still valid when dispatch occurred;
- what changed when a stale grant was rejected.

## Alternatives considered

### 1. Mutable `ready=true` on StageRun/materialization

Rejected.

It cannot encode which evidence established readiness, does not naturally expire, and is vulnerable to stale-state dispatch after schedule/readiness/dependency changes.

### 2. EligibilityEvaluation only; no explicit handoff identity

Rejected as the canonical contract.

A dispatcher would still need an unambiguous way to identify the exact evaluation it consumes and its validity/current-authority witnesses. A dedicated grant makes the handoff and audit contract explicit.

### 3. Grant as signed bearer token with no current-state recheck

Rejected.

Cryptographic integrity cannot prove the underlying plan/schedule/readiness/dependency authority is still current. A perfectly authentic stale token can still be wrong.

### 4. Global lock spanning evaluation through dispatch

Rejected as the architectural correctness mechanism.

A global distributed lock across sport services, scheduler state, output authority, queueing, and worker dispatch would be brittle, vendor-specific, difficult to recover, and still would not replace A-11 logical idempotency.

Narrow implementation locks/transactions may later optimize races, but correctness relies on immutable witnesses + revalidation.

### 5. Always perform the entire A-9 evaluation inline inside A-10

Rejected as the only model.

Inline reevaluation may be used when appropriate, but forcing it universally would collapse architecture responsibilities and lose a first-class durable eligibility evidence boundary useful for audit, queues, operator visibility, and distributed recovery.

## Consequences

### Benefits

- closes the A-9 to A-10 TOCTOU authority gap;
- prevents stale `READY` evidence from becoming permanent permission;
- preserves exact audit lineage from trigger -> eligibility -> dispatch;
- allows asynchronous queueing without trusting queue age alone;
- remains independent of Prefect/Celery/Redis/queue technology;
- supports explicit stale-grant rejection and reevaluation;
- composes cleanly with A-11 logical execution idempotency.

### Costs

- A-10/A-11 must implement current-authority verification before dispatch;
- A-13 must support durable grant/evaluation references and current-authority lookup efficiently;
- readiness/output/schedule invalidation must be visible to revalidation;
- implementation requires careful canonical digests/test vectors;
- dispatch may occasionally require another readiness refresh when a grant expires while queued.

These costs are accepted because silent stale dispatch is a more serious production defect.

## Compatibility / migration impact

There is no production TDLA implementation to migrate yet.

Future implementations must not introduce a permanent mutable `ready` column or Prefect task-state shortcut as canonical execution authority.

If a runtime maintains cached eligibility for performance, the cache must remain subordinate to the certified evaluation/grant/current-authority contract.

## Security / authorization impact

A grant must not be treated as an authorization credential or secret.

Authentication/authorization of the caller/worker remains A-20. Production certification/approval/side-effect authority remains governed by the resolved plan, certification state, A-19 operator controls where applicable, and later dispatch contracts.

## Validation required

Implementation must prove at minimum:

- schedule revision after READY rejects old grant;
- readiness expires after READY rejects old grant;
- upstream output supersession/retraction rejects old grant;
- plan revision rejects old grant;
- grant cannot be reused across scope/stage/environment/mode;
- two equivalent evaluation attempts do not create duplicate StageRuns;
- queued grant expiration routes to reevaluation rather than blind dispatch;
- A-11 still blocks duplicate logical execution even with multiple valid/equivalent grants.

## Related architecture

- A-5 Sport Automation Adapter readiness contract
- A-6 Pipeline Plan / Stage Contracts
- A-7 Trigger Architecture
- A-8 Event-Relative Scheduling Engine
- A-9 Dependency / Readiness Engine
- future A-10 Worker / Execution Backend
- future A-11 Retry / Timeout / Idempotency
- future A-13 Persistence / Audit / Provenance

## Supersession

Supersedes: none.  
Superseded by: none.