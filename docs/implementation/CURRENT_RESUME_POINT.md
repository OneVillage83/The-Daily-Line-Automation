# The Daily Line Automation — Current Resume Point

Last updated: 2026-09-02  
Authority: This file is the single exact continuation point for unfinished TDLA work. It does not override architecture/certification authority; it tells the next session where to resume.

## Current project state

- Repository exists and is no longer empty.
- Repository constitution/documentation-memory policy is established in `AGENTS.md`.
- A-0 through A-4 architecture is documented in `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md`.
- A-0 through A-4 are **DOCUMENTED — REVIEW PENDING**, not yet architecture-certified.
- No production implementation milestone is certified.
- No TDLA automation is production-authoritative.
- Daily-MLB remains manual-first; later automation must prove equivalence after its manual production architecture is certified.

## Exact next step

### Step 1 — Review A-0 through A-4 before certification

Perform a conformance/consistency review focused on:

1. **DDC boundary:** confirm TDLA does not duplicate provider acquisition, raw-evidence, generic market/weather/venue/travel functions that belong to Daily-Data-Core.
2. **Daily-MLB boundary:** confirm TDLA does not absorb MLB-specific readiness, lineup/pitcher semantics, model logic, recommendation logic, or settlement/report interpretation.
3. **Daily-NFL / NCAAF boundary:** confirm the generic contracts can support event-relative football workflows without introducing football-specific branches into TDLA.
4. **Identity review:** stress-test logical run vs attempt vs replay vs reprocess vs backfill vs supersession semantics for duplicate triggers, schedule changes, process loss, and intentional reruns.
5. **Configuration review:** verify environment/config precedence, non-secret digest rules, runtime override audit, and secret-reference treatment are sufficient.
6. **Vendor independence:** verify no canonical TDLA identity depends on Prefect-specific IDs/state.
7. **Documentation memory:** verify the mandated change-journal + resume-point + certification-log process is sufficient to prevent future rediscovery/rework.

### Step 2 — Resolve findings

If review finds defects:
- update A-0 through A-4;
- add/update ADR(s) when the fix reflects a durable decision/tradeoff;
- append `CHANGE_JOURNAL.md`;
- keep status as review pending until clean.

### Step 3 — Certify A-0 through A-4 if clean

Create an architecture-conformance review record and update:
- `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`;
- `docs/architecture/README.md`;
- `CHANGE_JOURNAL.md`;
- this resume point.

### Step 4 — Begin A-5 Sport Automation Adapter Contract

A-5 must define the precise sport-neutral boundary by which Daily-* repositories expose automation capabilities. At minimum test the design against:

- MLB probable-pitcher/lineup timing;
- postponements/reschedules/doubleheaders;
- NFL/NCAAF injury/inactive/weather timing;
- one-event and whole-slate workflows;
- optional vs required data/stages;
- no-games days;
- settlement/evaluation workflows;
- shadow/supervised/production modes;
- partial provider degradation;
- deadline-driven final prediction/publication stages.

## Do not do yet

Until A-0 through A-4 review is complete and A-5/A-6 contracts are defined:

- do not build sport-specific adapters;
- do not add MLB/NFL conditional branches to generic code;
- do not create production Prefect flows and treat them as authority;
- do not design database DDL prematurely around Prefect objects;
- do not enable production publishing;
- do not automate around unfinished Daily-MLB manual architecture.

## Required reading for next session

1. `README.md`
2. `AGENTS.md`
3. this file
4. `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`
5. `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md`
6. relevant DDC / Daily-MLB / Daily-NFL governing architecture before certifying cross-repository boundaries.
