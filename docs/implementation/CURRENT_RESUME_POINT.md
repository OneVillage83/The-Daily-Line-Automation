# The Daily Line Automation — Current Resume Point

Last updated: 2026-09-02 (America/Los_Angeles)  
Authority: This file is the single exact continuation point for unfinished TDLA work. It does not override architecture/certification authority; it tells the next session where to resume.

## Current project state

- Repository exists and the architecture/documentation foundation is established.
- Repository constitution/documentation-memory policy is authoritative in `AGENTS.md`.
- A-0 through A-4 base architecture is in `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md`.
- Nested lifecycle/cross-repository clarification is in `docs/architecture/A00-A04_FOUNDATION_ADDENDUM_V1_1.md`.
- A-0 through A-4 are **ARCHITECTURE-CERTIFIED**.
- Certification evidence: `docs/implementation/A00-A04_ARCHITECTURE_CONFORMANCE_REVIEW_20260902.md`.
- ADR-0001 establishes TDLA canonical automation identity and a replaceable orchestration runtime.
- No production implementation milestone is certified.
- No TDLA automation is production-authoritative.
- Daily-MLB remains manual-first; later automation must prove equivalence after its manual production architecture is certified.

## Resolved finding from A-0 through A-4 review

The review identified one important terminology ambiguity: DDC/sport repositories may already have internal acquisition/job lifecycles, while TDLA owns orchestration lifecycle.

Certified resolution:

```text
TDLA WorkflowRun
    -> TDLA StageRun / RunAttempt
        -> sport child job/service reference
            -> DDC acquisition run(s)
                -> provider request/attempt evidence
```

TDLA does not collapse or replace child identities. It links them through provenance.

## Exact next step — A-5 Sport Automation Adapter Contract

Design and document the precise sport-neutral interface by which Daily-MLB, Daily-NFL, Daily-NCAAF, and future Daily-* repositories expose automation capabilities to TDLA without moving sport logic into TDLA.

### A-5 must define at minimum

1. **Adapter identity/version**
   - adapter contract version;
   - sport implementation version;
   - capability negotiation/compatibility;
   - fail-closed behavior for incompatible versions.

2. **Sport scope references**
   - event/game reference;
   - slate/day/batch reference;
   - schedule revision/reference fields;
   - TDLA stores sport-owned references without becoming permanent sport identity authority.

3. **Planning interface**
   - obtain/validate an automation plan or plan fragment;
   - event-relative timing declarations;
   - required/optional stages;
   - deadlines/cutoffs;
   - dependencies;
   - execution mode (`MANUAL_*`, `AUTOMATION_SHADOW`, `AUTOMATION_SUPERVISED`, `AUTOMATION_PRODUCTION`).

4. **Readiness interface**
   - `READY`, `WAITING`, `BLOCKED`, or equivalent contract result;
   - sport-defined reason codes;
   - next-check hints where valid;
   - evidence/freshness references;
   - no TDLA interpretation of MLB/NFL-specific meaning.

5. **Execution interface**
   - immutable release/executable reference;
   - structured invocation request;
   - stable outer idempotency/execution reference propagation;
   - child/external execution reference returned by sport service where applicable;
   - synchronous vs asynchronous execution capability.

6. **Child reconciliation**
   - inspect a previously-dispatched child job after TDLA restart/loss;
   - determine running/succeeded/failed/cancelled/unknown;
   - avoid blind duplicate redispatch;
   - retain child diagnostics without redefining sport meaning.

7. **Cancellation / timeout contract**
   - whether cancellation is supported;
   - cancellation acknowledgement semantics;
   - what TDLA timeout means vs child-service timeout;
   - orphaned-child behavior.

8. **Result contract**
   - sport semantic success/degradation/failure result;
   - required output/artifact manifest identity;
   - sport-provided model/config/version metadata;
   - structured failure/degradation reason codes;
   - TDLA independently validates generic outer output requirements.

9. **Artifact contract**
   - manifest schema/version;
   - content hashes;
   - artifact locations/handles;
   - required vs optional artifacts;
   - immutable evidence references;
   - ownership of retention/storage metadata.

10. **Settlement/evaluation hooks**
    - generic orchestration invocation only;
    - sport owns settlement interpretation and evaluation semantics;
    - same adapter framework should support postgame workflows without TDLA sports logic.

11. **Security boundary**
    - service identity/auth capability declaration;
    - no raw sport/provider secrets returned in adapter results;
    - safe diagnostics.

12. **Observability/provenance handoff**
    - trace/correlation ID propagation;
    - child execution references;
    - output/input provenance handles;
    - TDLA vs sport/DDC authority clearly separable.

### A-5 stress cases that must be used before certification

- MLB probable-pitcher or lineup not ready at one check and ready later;
- MLB postponement/reschedule/doubleheader;
- NFL/NCAAF late inactive/injury/weather update before kickoff;
- no-games day;
- slate-level execution plus game-level child work;
- partial optional-provider degradation;
- child job continues after TDLA worker dies;
- duplicate readiness/trigger events;
- shadow mode must produce no production publication side effect;
- supervised mode pauses for operator approval;
- production mode can auto-continue only under explicit policy;
- settlement/evaluation runs after event completion;
- incompatible adapter/TDLA contract versions fail closed.

## Immediate documentation outputs for A-5

Create:

- `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_V1.md`
- architecture review/certification evidence for A-5 after stress testing;
- ADR only if A-5 introduces a durable new tradeoff not already covered;
- detailed `CHANGE_JOURNAL.md` entry;
- updated `ARCHITECTURE_CERTIFICATION_LOG.md`;
- updated architecture index;
- updated resume point.

## Do not do yet

Until A-5 and A-6 are certified:

- do not build real MLB/NFL/NCAAF adapters;
- do not add sport-specific conditionals to generic TDLA code;
- do not create production Prefect flows and treat runtime IDs as canonical authority;
- do not design final PostgreSQL DDL around unreviewed adapter/run contracts;
- do not enable production publishing;
- do not automate around unfinished Daily-MLB manual architecture.

## Required reading for next session

1. `README.md`
2. `AGENTS.md`
3. this file
4. `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`
5. `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md`
6. `docs/architecture/A00-A04_FOUNDATION_ADDENDUM_V1_1.md`
7. `docs/implementation/A00-A04_ARCHITECTURE_CONFORMANCE_REVIEW_20260902.md`
8. `docs/adr/ADR-0001_CONTROL_PLANE_AND_VENDOR_NEUTRAL_IDENTITY.md`
9. relevant current DDC / Daily-MLB / Daily-NFL governing contracts while designing A-5.
