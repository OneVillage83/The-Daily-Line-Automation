# ADR-0002 — Sport Automation Adapter Is a Transport-Neutral Protocol Boundary

Date: 2026-09-03  
Status: **ACCEPTED**

## Context

The Daily Line will automate multiple sport systems with different internal architectures and maturity levels. Daily-MLB already demonstrates an authenticated asynchronous service/job pattern, while Daily-NFL, Daily-NCAAF, and future sports may eventually run through containers, service APIs, queues, dedicated workers, or other execution mechanisms.

A direct-import design in which The-Daily-Line-Automation (TDLA) imports sport repository packages and calls sport-specific Python functions would create several long-term problems:

- TDLA would become coupled to sport package layouts and dependency graphs;
- sport deployment/release boundaries would blur;
- a Python import would make it easy for sport-domain logic to leak into TDLA;
- changing from a local process to a remote service/container could alter canonical automation behavior;
- dependency conflicts across sports could force unrelated sport releases into one runtime;
- security/service identity and execution isolation would become harder to reason about;
- child job/reconciliation semantics would be inconsistent or hidden.

Conversely, declaring HTTP as the canonical architecture would overfit the first implementation and unnecessarily couple domain contracts to one transport.

## Decision

The Sport Automation Adapter is a **versioned logical protocol boundary**.

TDLA depends on protocol semantics such as:

- adapter description/capability negotiation;
- sport scope discovery/reference;
- plan/plan-fragment resolution;
- readiness evaluation;
- invocation with stable outer idempotency/correlation identity;
- child execution acknowledgement/reconciliation;
- cancellation capability;
- terminal result and artifact-manifest handoff;
- post-event settlement/evaluation invocation.

The physical implementation may use authenticated HTTP, container/CLI wrappers, RPC, queues, or another certified execution backend.

Canonical TDLA logical run/stage/attempt identity and adapter protocol behavior must remain stable if transport changes.

A sport repository may provide a thin adapter/wrapper over an existing certified pipeline/service. TDLA must not copy sport logic into its own repository to avoid writing such a wrapper.

## Required consequence: fail-closed compatibility

Every production adapter exposes a versioned descriptor/capability profile. TDLA binds a plan/run to the negotiated protocol/capability profile and fails closed before dispatch when:

- protocol versions are incompatible;
- required capabilities are absent;
- the requested execution mode is not supported/certified;
- the immutable target/release does not satisfy the plan contract.

No sport-name-based fallback or guessed method/field semantics are allowed.

## Required consequence: child-recovery boundary

For asynchronous production-capable adapters, transport neutrality does not weaken recovery requirements. The adapter must provide enough durable behavior to reconcile an accepted child operation by child reference and, for lost-acknowledgement recovery, by the TDLA logical idempotency identity or an equivalent durable deduplication handle.

Changing transport cannot turn a previously idempotent/reconcilable operation into blind fire-and-forget execution without a new certification decision.

## Alternatives considered

### 1. Import sport Python packages directly into TDLA

Rejected as the canonical architecture.

It may be useful in isolated development tooling, but it couples dependency/runtime boundaries and makes sport-logic leakage too easy. A local adapter may still invoke a sport package behind the protocol wrapper; that is an implementation detail.

### 2. Make REST/HTTP the permanent adapter architecture

Rejected.

HTTP is a strong initial implementation candidate for existing service-style sports, but it is transport, not domain identity.

### 3. Make Prefect tasks/flows the adapter contract

Rejected.

This would violate ADR-0001 by coupling canonical sport integration to the orchestration vendor.

### 4. Let each sport expose an unrelated bespoke integration

Rejected.

This would reproduce the exact multi-sport automation fragmentation TDLA exists to prevent and would make retries, audit, security, reconciliation, and certification inconsistent.

## Consequences and tradeoffs

### Benefits

- sport repositories remain independently releasable;
- TDLA stays free of sport dependency trees and domain implementations;
- local and remote execution can coexist;
- transport can evolve without redefining canonical automation identity;
- contract tests can be reused for every sport adapter;
- async reconciliation/idempotency requirements are visible and enforceable;
- security/isolation boundaries are clearer;
- a future sport can onboard by implementing the protocol instead of changing TDLA generic logic.

### Costs

- each sport needs an adapter/wrapper layer;
- serialization/version compatibility must be maintained explicitly;
- local in-process execution has slightly more ceremony;
- transport adapters require dedicated contract tests;
- cross-repository changes require versioned coordination rather than implicit Python-call compatibility.

These costs are intentional because they buy long-term multi-sport isolation and reproducibility.

## Compatibility / migration impact

Existing sport pipelines are not required to rewrite their internal logic.

They may be wrapped if the wrapper can prove:

- exact mapping to the certified manual pipeline;
- immutable release targeting;
- idempotent/reconcilable invocation;
- stable child/result identity;
- safe shadow/supervised/production behavior;
- artifact/provenance compatibility.

Daily-MLB's existing service job-ID/polling pattern is compatible in principle, but production onboarding must target the eventual certified manual Daily-MLB pipeline rather than treating the current starter collector as automatically production-ready.

## Security / operational impact

- service authentication belongs to the transport/execution layer, while service-principal identity remains auditable;
- raw credentials never become adapter payload/result data;
- remote adapters can use least-privilege identities;
- isolated containers/services can prevent dependency and failure blast-radius coupling across sports;
- execution backend details are finalized under A-10 and security details under A-20.

## Validation required

A candidate adapter must pass A-5 contract/conformance tests including:

- version/capability mismatch fail-closed behavior;
- duplicate invocation/idempotency behavior;
- acknowledgement-loss recovery;
- child reconciliation after TDLA restart;
- shadow-mode side-effect safety;
- malformed-response/schema rejection;
- preservation of nested child/DDC provenance identities.

## Related architecture

- A-0 through A-4 Foundation V1 + V1.1 addendum
- A-5 Sport Automation Adapter Contract V1
- future A-6, A-10, A-11, A-12, A-20
- ADR-0001 Control Plane and Vendor-Neutral Identity

## Supersession

Supersedes: none.  
Superseded by: none.
