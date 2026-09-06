# The Daily Line Automation — Architecture Index

This directory contains the governing architecture contracts for The-Daily-Line-Automation (TDLA).

Architecture is intentionally defined before production implementation so TDLA can become a durable multi-sport control plane without accumulating sport-specific or vendor-specific coupling.

## Architecture authority

- Architecture contracts define intended behavior and ownership.
- `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md` is the authoritative status record for whether an architecture section is merely drafted/documented, frozen/certified, superseded, or under revision.
- ADRs record durable decisions/tradeoffs but do not silently override an architecture contract. When an ADR changes architecture, the affected architecture document and certification log must also be updated.
- Running checkpoint/progress logs never override a newer certification decision.

## Sections

| Section | Topic | Document | Status |
|---|---|---|---|
| A-0 | Mission, principles, system boundary | `A00-A04_AUTOMATION_FOUNDATION_V1.md` + V1.1 addendum | **ARCHITECTURE-CERTIFIED** |
| A-1 | Ownership / cross-repository authority | foundation V1 + `A00-A04_FOUNDATION_ADDENDUM_V1_1.md` | **ARCHITECTURE-CERTIFIED** |
| A-2 | Canonical automation domain model | foundation V1 + V1.1 addendum | **ARCHITECTURE-CERTIFIED** |
| A-3 | Run identity / execution lifecycle | foundation V1 + V1.1 addendum | **ARCHITECTURE-CERTIFIED** |
| A-4 | Configuration / environment model | `A00-A04_AUTOMATION_FOUNDATION_V1.md` | **ARCHITECTURE-CERTIFIED** |
| A-5 | Sport Automation Adapter contract | `A05_SPORT_AUTOMATION_ADAPTER_V1.md` + `A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md` | **ARCHITECTURE-CERTIFIED** |
| A-6 | Pipeline plan / stage contracts | `A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md` + `A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md` | **ARCHITECTURE-CERTIFIED** |
| A-7 | Trigger architecture | `A07_TRIGGER_ARCHITECTURE_V1.md` + `A07_TRIGGER_ARCHITECTURE_ADDENDUM_V1_1.md` | **ARCHITECTURE-CERTIFIED** |
| A-8 | Event-relative scheduling | `A08_EVENT_RELATIVE_SCHEDULING_ENGINE_V1.md` + `A08_EVENT_RELATIVE_SCHEDULING_ENGINE_ADDENDUM_V1_1.md` | **ARCHITECTURE-CERTIFIED** |
| A-9 | Dependency / readiness engine | `A09_DEPENDENCY_READINESS_ENGINE_V1.md` + `A09_DEPENDENCY_READINESS_ENGINE_ADDENDUM_V1_1.md` | **ARCHITECTURE-CERTIFIED** |
| A-10 | Worker / execution backends | `A10_WORKER_EXECUTION_BACKEND_V1.md` + `A10_WORKER_EXECUTION_BACKEND_ADDENDUM_V1_1.md` | **ARCHITECTURE-CERTIFIED** |
| A-11 | Retry / timeout / idempotency | TBD | **NEXT** |
| A-12 | Failure / degradation / recovery | TBD | Planned |
| A-13 | Persistence / immutable audit / provenance | TBD | Planned |
| A-14 | Artifact / replay / backfill / reprocess | TBD | Planned |
| A-15 | Resource / concurrency / provider budgeting | TBD | Planned |
| A-16 | Observability / tracing / metrics | TBD | Planned |
| A-17 | Alerts / incidents | TBD | Planned |
| A-18 | Publication / distribution | TBD | Planned |
| A-19 | Human approval / operator controls | TBD | Planned |
| A-20 | Security / secrets / service identity | TBD | Planned |
| A-21 | Deployment / HA / backup / DR | TBD | Planned |
| A-22 | CI/CD / immutable release execution | TBD | Planned |
| A-23 | Multi-sport scaling / isolation | TBD | Planned |
| A-24 | Future adaptive/intelligent automation | TBD | Planned |

## Certification evidence for A-0 through A-4

- `docs/implementation/A00-A04_ARCHITECTURE_CONFORMANCE_REVIEW_20260902.md`
- `A00-A04_FOUNDATION_ADDENDUM_V1_1.md`
- `docs/adr/ADR-0001_CONTROL_PLANE_AND_VENDOR_NEUTRAL_IDENTITY.md`

TDLA owns the outer automation lifecycle while sport services and DDC may retain nested child job/acquisition/provider lifecycle identities linked through provenance.

## Certification evidence for A-5

- `A05_SPORT_AUTOMATION_ADAPTER_V1.md`
- `A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md`
- `docs/implementation/A05_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md`
- `docs/adr/ADR-0002_TRANSPORT_NEUTRAL_SPORT_ADAPTER_PROTOCOL.md`

A-5 establishes a transport-neutral versioned sport adapter with opaque sport scope refs, readiness contracts, immutable invocation targets, semantic results/artifacts, and safe async child reconciliation. Physical retry `attempt_id` is not child dedup identity; lost child acknowledgement must be recoverable by stable logical idempotency/equivalent durable lookup.

## Certification evidence for A-6

- `A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`
- `A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md`
- `docs/implementation/A06_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md`
- `docs/adr/ADR-0003_IMMUTABLE_PLAN_FRAGMENTS_AND_EXPLICIT_COMPOSITION.md`

A-6 establishes immutable DAG-based resolved plans, separately owned sport/platform fragments, explicit typed composition, exact sport-owned fan-out/fan-in membership, stable `ScheduleSlotRef` identities, immutable execution targets/policies, and deterministic semantic plan digests.

## Certification evidence for A-7

- `A07_TRIGGER_ARCHITECTURE_V1.md`
- `A07_TRIGGER_ARCHITECTURE_ADDENDUM_V1_1.md`
- `docs/implementation/A07_ARCHITECTURE_CONFORMANCE_REVIEW_20260904.md`
- `docs/adr/ADR-0004_DURABLE_TRIGGER_EVIDENCE_AND_REEVALUATION_ONLY_AUTHORITY.md`

A-7 separates physical trigger deliveries, immutable semantic event revisions, bindings/evaluations, and logical eligibility-reevaluation requests. Triggers are durable reevaluation evidence only and never direct execution authority.

## Certification evidence for A-8

- `A08_EVENT_RELATIVE_SCHEDULING_ENGINE_V1.md`
- `A08_EVENT_RELATIVE_SCHEDULING_ENGINE_ADDENDUM_V1_1.md`
- `docs/implementation/A08_ARCHITECTURE_CONFORMANCE_REVIEW_20260904.md`
- `docs/adr/ADR-0005_STABLE_SCHEDULE_SLOTS_AND_RESOLVED_TIME_AUTHORITY.md`

A-8 separates stable logical schedule slots from immutable resolved clock authority, handles reschedules/TBD/missed windows/recovery/DST, and produces one canonical reevaluation-only A-7 `TIME_DUE` event per logical occurrence.

## Certification evidence for A-9

- `A09_DEPENDENCY_READINESS_ENGINE_V1.md`
- `A09_DEPENDENCY_READINESS_ENGINE_ADDENDUM_V1_1.md`
- `docs/implementation/A09_ARCHITECTURE_CONFORMANCE_REVIEW_20260905.md`
- `docs/adr/ADR-0006_VERSION_BOUND_DISPATCH_ELIGIBILITY_AND_FINAL_REVALIDATION.md`

A-9 derives immutable eligibility from current plan/materialization/scope/schedule/dependency/output/readiness/policy authority. Sport `READY` is not a permanent mutable flag. A version-bound non-bearer `DispatchEligibilityGrant` carries exact evidence to A-10/A-11 and must be revalidated before dispatch.

## Certification evidence for A-10

- `A10_WORKER_EXECUTION_BACKEND_V1.md`
- `A10_WORKER_EXECUTION_BACKEND_ADDENDUM_V1_1.md`
- `docs/implementation/A10_ARCHITECTURE_CONFORMANCE_REVIEW_20260905.md`
- `docs/adr/ADR-0007_IMMUTABLE_EXECUTION_ENVELOPE_AND_RECONCILABLE_BACKEND_DISPATCH.md`

A-10 establishes the replaceable physical execution plane.

Important certified rules:

- canonical TDLA WorkflowRun/StageRun/RunAttempt identities remain separate from Prefect/Docker/Kubernetes/queue/process/backend IDs;
- an immutable schema-versioned `ExecutionEnvelope` captures exact attempt, eligibility, plan/stage/scope/schedule, immutable target, adapter/config/input/output, environment/mode, and A-11 logical-idempotency authority;
- A-9 current-authority witnesses are checked preflight and again immediately before irreversible submission;
- durable TDLA `DispatchRecord`/intent exists before backend submission;
- one RunAttempt uses a stable `BackendSubmissionKey` for ambiguous acknowledgement recovery/idempotent retransmission where supported;
- backend submission reconciliation and A-5 nested sport-child reconciliation are separate mandatory ambiguity defenses;
- worker claim/lease/heartbeat/cancellation evidence never proves the sport child stopped;
- worker/backend capability and environment/mode authorization are revalidated at actual assignment/start;
- backend callbacks are observations and cannot roll canonical state backward by receipt order;
- process exit 0, Prefect Completed, Kubernetes Job Complete, or queue acknowledgement never replace A-5/A-6 semantic result/output validation;
- final result/manifests correlate to the exact attempt/envelope/child authority; partial or unrelated artifacts cannot masquerade as success;
- backend execution-handle and sport-child-ref roles remain logically distinct even when a direct service integration reuses one external ID;
- stale queued work fails current-authority validation before start;
- backend migration does not change TDLA business/audit identity.

## Certified invariants through A-10

- TDLA is a control plane, not a sports model repository.
- DDC retains shared sport-agnostic acquisition/fact authority; sport repos retain sport intelligence/readiness/settlement meaning.
- production automation follows certified manual pipelines and equivalence proof.
- completed operational evidence is immutable and explicitly lineaged.
- Prefect is an initial replaceable runtime, never permanent TDLA identity authority.
- transport, scheduler, worker, and backend native IDs are runtime cross-references only.
- `ResolvedAutomationPlan` is executable plan authority; stage definition/materialization/StageRun/RunAttempt remain distinct.
- dynamic sport scope/fan-out membership stays sport-owned and revision/digest bound.
- trigger delivery and schedule due occurrences request reevaluation only.
- stable schedule slots survive event-time changes through immutable superseding resolutions.
- eligibility is immutable derived evidence over exact current authority, not `ready=true`.
- readiness/dependency/output evidence can become stale and must be revalidated before dispatch.
- `DispatchEligibilityGrant` is a version-bound proof capsule, not a bearer execution token.
- A-10 execution uses an immutable `ExecutionEnvelope` and durable dispatch intent before external action.
- backend submission ambiguity and sport-child ambiguity are reconciled independently before duplicate action.
- process/backend completion never substitutes for semantic result/output validation.
- A-11 remains final logical retry/timeout/idempotency authority and is next.
- PostgreSQL is intended as authoritative TDLA persistence; A-13 will freeze DDL/transaction mechanics.
- every material change leaves durable journal/status/resume documentation.

## Change process

When changing architecture:

1. identify affected sections and ownership boundaries;
2. create/update an ADR for meaningful tradeoffs or authority changes;
3. version/update the architecture contract;
4. document compatibility/migration implications;
5. update `CHANGE_JOURNAL.md`;
6. update `CURRENT_RESUME_POINT.md`;
7. update the certification log.

Do not simply edit architecture prose after implementation and present the new behavior as if it had always been intended.
