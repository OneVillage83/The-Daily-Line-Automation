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
| A-0 | Mission, principles, system boundary | `A00-A04_AUTOMATION_FOUNDATION_V1.md` | Documented; review pending |
| A-1 | Ownership / cross-repository authority | `A00-A04_AUTOMATION_FOUNDATION_V1.md` | Documented; review pending |
| A-2 | Canonical automation domain model | `A00-A04_AUTOMATION_FOUNDATION_V1.md` | Documented; review pending |
| A-3 | Run identity / execution lifecycle | `A00-A04_AUTOMATION_FOUNDATION_V1.md` | Documented; review pending |
| A-4 | Configuration / environment model | `A00-A04_AUTOMATION_FOUNDATION_V1.md` | Documented; review pending |
| A-5 | Sport Automation Adapter contract | TBD | **NEXT** |
| A-6 | Pipeline plan / stage contracts | TBD | Planned |
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

## Locked directional decisions already established

The foundation currently establishes these intended invariants, subject to certification review:

- TDLA is a control plane, not a sports model repository.
- DDC remains authority for certified shared sport-agnostic acquisition/facts.
- sport repositories remain authority for sport-specific intelligence and readiness meaning.
- website/app state remains owned by the product surface and receives explicit publication contracts.
- production automation authority follows manual pipeline certification and equivalence proof.
- logical run identity differs from physical execution attempts.
- retries, replay, backfill, reprocess, and supersession remain explicitly distinct.
- completed operational history is immutable/auditable.
- Prefect 3 is the intended initial runtime but cannot become TDLA permanent identity authority.
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
