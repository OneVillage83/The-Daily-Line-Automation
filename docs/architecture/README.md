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
| A-6 | Pipeline plan / stage contracts | TBD | **NEXT** |
| A-7 | Trigger architecture | TBD | Planned |
| A-8 | Event-relative scheduling | TBD | Planned |
| A-9 | Dependency / readiness engine | TBD | Planned |
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

## Certified foundation + adapter invariants

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
- PostgreSQL is intended as TDLA authoritative persistence.
- production workloads must use immutable release identities/digests.
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
