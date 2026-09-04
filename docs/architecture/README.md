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
| A-9 | Dependency / readiness engine | TBD | **NEXT** |
| A-10 | Worker / execution backends | TBD | Planned |
| A-11 | Retry / timeout / idempotency | TBD | Planned |
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

The review identified and resolved one lifecycle-boundary ambiguity. TDLA owns the **outer automation lifecycle**; sport services and DDC may retain their own nested child job/acquisition lifecycle identities. These IDs are linked through provenance rather than collapsed into a single authority.

## Certification evidence for A-5

- `A05_SPORT_AUTOMATION_ADAPTER_V1.md`
- `A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md`
- `docs/implementation/A05_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md`
- `docs/adr/ADR-0002_TRANSPORT_NEUTRAL_SPORT_ADAPTER_PROTOCOL.md`

A-5 establishes a versioned sport-neutral protocol boundary with capability negotiation, opaque sport-owned scope references, readiness declarations, immutable invocation targeting, async child reconciliation, semantic result/artifact handoff, execution-mode/side-effect safety, and post-event hooks.

Important A-5 certified clarifications:

- physical retry `attempt_id` is correlation/audit metadata and cannot be used as child deduplication identity;
- the stable logical idempotency identity remains constant across retries;
- `MANUAL_CERTIFIED` is not unattended automation authority;
- technical support for production mode is not production authorization;
- asynchronous production integration must recover the lost-acknowledgement case by logical idempotency identity/equivalent durable deduplication handle;
- the adapter is a transport-neutral protocol, not a Python-import/HTTP/Prefect-specific contract.

## Certification evidence for A-6

- `A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`
- `A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md`
- `docs/implementation/A06_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md`
- `docs/adr/ADR-0003_IMMUTABLE_PLAN_FRAGMENTS_AND_EXPLICIT_COMPOSITION.md`

A-6 establishes a declarative DAG-based plan model with immutable sport/platform fragments, explicit typed composition, deterministic stage materialization, sport-owned dynamic scope membership, fan-out/fan-in barriers, typed timing/readiness/input/output declarations, immutable target/policy binding, side-effect classification, and deterministic semantic plan digests.

Important A-6 certified clarifications:

- sport child membership is represented through a neutral `ScopeSetBinding` over exact sport-owned `SportScopeRef` values; TDLA does not invent membership;
- semantic plan digests exclude schema-declared presentation-only/audit metadata but include all execution-affecting fields;
- repeated snapshots use stable logical `ScheduleSlotRef` identity rather than wall-clock timestamp identity;
- production resolved plans pin immutable execution-affecting policy versions/digests rather than mutable policy aliases;
- cross-fragment composition has no silent precedence; conflicts and incompatible port bindings fail closed;
- the `ResolvedAutomationPlan`, not a Prefect flow definition, is the executable plan authority.

## Certification evidence for A-7

- `A07_TRIGGER_ARCHITECTURE_V1.md`
- `A07_TRIGGER_ARCHITECTURE_ADDENDUM_V1_1.md`
- `docs/implementation/A07_ARCHITECTURE_CONFORMANCE_REVIEW_20260904.md`
- `docs/adr/ADR-0004_DURABLE_TRIGGER_EVIDENCE_AND_REEVALUATION_ONLY_AUTHORITY.md`

A-7 establishes a durable event architecture where physical trigger deliveries, immutable semantic source-event revisions, plan-bound trigger bindings, trigger evaluations, and logical eligibility-reevaluation requests are separate identities.

Important A-7 certified rules:

- a trigger requests eligibility reevaluation only; it never grants execution or side-effect authority;
- accepted trigger evidence and causal reevaluation intent are durable before downstream irreversible action;
- physical delivery identity is separate from semantic source occurrence/revision identity;
- corrections/retractions are immutable revisions/lineage, not mutation of prior evidence;
- same occurrence+revision with conflicting semantic payload fails closed as an identity conflict;
- logical eligibility reevaluation identity is separate from physical processing attempts;
- trigger deduplication and A-11 stage idempotency are separate defenses;
- stale/out-of-order events and timer occurrences cannot roll authority backward or revive superseded work;
- sport-change signals remain opaque hints; A-5 readiness remains authoritative when required;
- raw burst evidence is retained even when reevaluation causes are coalesced;
- coalescing cannot silently cross incompatible plan/stage/scope/binding/environment revisions;
- untrusted deliveries cannot create authoritative `TriggerEvent` objects;
- replay/test ingress is explicitly labeled and restricted;
- source silence/outage is not evidence that domain state did not change;
- there is no direct webhook/timer/operator-trigger-to-publication/destructive-action path.

## Certification evidence for A-8

- `A08_EVENT_RELATIVE_SCHEDULING_ENGINE_V1.md`
- `A08_EVENT_RELATIVE_SCHEDULING_ENGINE_ADDENDUM_V1_1.md`
- `docs/implementation/A08_ARCHITECTURE_CONFORMANCE_REVIEW_20260904.md`
- `docs/adr/ADR-0005_STABLE_SCHEDULE_SLOTS_AND_RESOLVED_TIME_AUTHORITY.md`

A-8 establishes stable logical schedule slots, immutable schedule resolutions, logical due occurrences, explicit missed-window policy, reschedule/TBD/cancellation supersession, restart/HA recovery semantics, UTC/DST rules, recurring calendar identity, and a one-way handoff into A-7 `TIME_DUE` reevaluation evidence.

Important A-8 certified rules:

- a wall-clock timestamp is a resolution of stable schedule intent, not the stage/snapshot identity;
- every production event-relative resolution binds exact plan/stage/scope/schedule/anchor/timing-policy authority;
- event-time changes create new immutable `ScheduleResolution` authority and supersede pending old authority rather than mutating history;
- same UTC instant under a new sport schedule revision remains new authority/provenance, though runtime timer wakeups may be reused safely;
- one logical `ScheduleOccurrence` maps to at most one canonical semantic A-7 `TIME_DUE` event;
- physical timer callbacks/scans/leases are not canonical schedule occurrence identity;
- earlier reschedules that make slots overdue are classified independently using immutable missed-window policies;
- missed-window policy can request reevaluation, skip, supersede, or require review, but the scheduler itself never executes sport work;
- stale already-emitted old timer authority must be revalidated after later supersession before dispatch;
- unresolved/TBD anchors never receive invented placeholder due clocks;
- event-relative elapsed offsets use resolved UTC duration arithmetic;
- local calendar recurrences explicitly retain DST ambiguity/nonexistent-time resolution authority;
- restart/downtime/multiple scheduler replicas converge on the same logical occurrence/evidence;
- customer-visible/destructive late work has no generic catch-up permission;
- Prefect/APScheduler/CronJob/queue IDs remain runtime cross-references only;
- there is no direct scheduler-to-executor path.

## Certified foundation + adapter + plan + trigger + scheduling invariants

- TDLA is a control plane, not a sports model repository.
- DDC remains authority for certified shared sport-agnostic acquisition/facts.
- sport repositories remain authority for sport-specific intelligence and readiness meaning.
- website/app state remains owned by the product surface and receives explicit publication contracts.
- production automation authority follows manual pipeline certification and equivalence proof.
- logical run identity differs from physical execution attempts.
- nested sport/DDC child execution identities remain separate from TDLA outer identity.
- retries, replay, backfill, reprocess, and supersession remain explicitly distinct.
- completed operational history is immutable/auditable.
- Prefect 3 is the intended initial runtime but cannot become TDLA permanent identity authority.
- the sport adapter protocol is transport-neutral and capability-negotiated.
- sport scope identity is opaque/sport-owned; TDLA stores references and neutral scheduling metadata.
- unknown child state is not permission to duplicate dispatch.
- shadow/supervised/production side-effect authority is explicit and fail-closed.
- V1 executable plans are declarative DAGs assembled from immutable fragments with explicit typed bindings.
- stage definition, stage materialization, logical StageRun, and physical RunAttempt remain distinct identities.
- dynamic fan-out membership is revision/digest bound and sport-owned.
- optional/conditional/no-op/degraded outcomes satisfy only explicitly compatible dependency/output contracts.
- production resolved plans use immutable execution targets and immutable execution-affecting policy bindings.
- semantic plan identity uses deterministic canonical normalization + SHA-256.
- trigger delivery, semantic source event, reevaluation request, StageRun, and RunAttempt remain separate identities.
- trigger evidence is durable and append-only; corrections/retractions preserve lineage.
- trigger-source duplicates/out-of-order events do not become direct execution authority.
- schedule slot identity is stable across clock-time changes; resolutions/occurrences retain exact authority and supersession lineage.
- time-due evidence is reevaluation-only and cannot bypass current schedule/dependency/readiness/idempotency/side-effect gates.
- scheduler correctness does not rely on a singleton process or vendor-native timer identity.
- PostgreSQL is intended as TDLA authoritative persistence.
- non-secret effective configuration is schema-validated and hashable.
- every material change must produce detailed durable documentation and an exact resume point.

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
