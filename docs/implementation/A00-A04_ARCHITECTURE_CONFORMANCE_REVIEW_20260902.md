# A-0 through A-4 Architecture Conformance Review — 2026-09-02

Repository: `OneVillage83/The-Daily-Line-Automation`  
Review scope: A-0 Mission/Boundary, A-1 Ownership, A-2 Domain Model, A-3 Identity/Lifecycle, A-4 Configuration/Environment  
Reviewed against: current Daily-Data-Core ownership contract, Daily-NFL F-0 through F-4 foundation, current Daily-MLB service/manual collector boundary, and TDLA documentation/governance rules.

## Review objective

Determine whether A-0 through A-4 are sufficiently complete and internally/cross-repository consistent to become the certified foundation governing later A-5 through A-24 architecture and eventual implementation.

The review intentionally looks for contradictions rather than attempting to justify the initial draft.

---

## 1. Daily-Data-Core ownership boundary

### Evidence reviewed

Current DDC ownership documentation establishes that DDC owns shared provider/acquisition transport, immutable raw evidence/provenance, generic sportsbook facts/math, normalized weather, venues/geospatial, and neutral travel/rest primitives, while sport-specific identity, interpretation, model logic, Recommendation Gate behavior, and settlement/report interpretation remain outside DDC.

### TDLA comparison

A-1 assigns TDLA orchestration/scheduling/attempt/publication-coordination responsibilities, not shared fact acquisition or sports meaning.

### Finding

**PASS WITH CLARIFICATION.**

One older Daily-NFL foundation statement included generic `run/job lifecycle` in the Core responsibility list. Without clarification, later implementation could incorrectly treat TDLA and DDC as competing authorities for the same run concept.

### Resolution

Created:

`docs/architecture/A00-A04_FOUNDATION_ADDENDUM_V1_1.md`

The addendum establishes layered/nested lifecycle authority:

```text
TDLA outer automation run/attempt
    -> sport service/job reference
        -> DDC acquisition run(s)
            -> provider request/attempt evidence
```

TDLA owns outer orchestration intent/history. DDC retains internal shared acquisition/provider lifecycle/evidence. Sport repositories may retain internal service/job lifecycle. IDs are linked, not re-keyed.

Result after resolution: **PASS**.

---

## 2. Daily-MLB boundary

### Evidence reviewed

Current Daily-MLB exposes a FastAPI job service and `run_id` for its current collection workflow. It also retains MLB-specific stadium/weather interpretation and later sport intelligence within the MLB repository. The current project direction is to finish/certify the manual MLB production architecture before enabling production automation.

### Stress cases

- TDLA invokes a certified MLB service and receives an MLB job ID.
- MLB internally invokes DDC-backed collectors.
- MLB job retries internal provider acquisition.
- TDLA loses its worker while MLB child job continues.
- MLB final output exists but required TDLA publication stage has not completed.
- lineup/probable-pitcher readiness blocks a final prediction stage.

### Finding

**PASS.**

The foundation does not require TDLA to understand probable-pitcher/lineup meaning. The child-job boundary is now explicitly documented. Manual-first promotion states prevent TDLA from becoming production authority before MLB is certified.

A-5/A-6 must define child execution references, readiness reason contracts, cancellation/timeouts, and artifact-result validation precisely.

---

## 3. Daily-NFL / NCAAF compatibility

### Evidence reviewed

Daily-NFL architecture requires continuous legitimate pregame monitoring until kickoff, with information admissible according to point-in-time availability rather than a blanket game-day exclusion. It owns football-specific injuries/inactives/depth/state/model interpretation.

### Stress cases

- changing kickoff time;
- late inactive report;
- weather refresh at T-90/T-30;
- multiple prediction snapshots before kickoff;
- game-specific vs slate-level work;
- high-concurrency Sunday/Saturday windows;
- provider delay that is optional for one stage but required for another.

### Finding

**PASS.**

A-0 through A-4 support event-relative future scheduling without defining the specific timeline. `scope_reference` remains sport-provided. Supersession preserves prior planned history when event timing changes. Required/optional/degradation semantics remain declared by the sport plan/adapter rather than hard-coded into TDLA.

A-5 through A-9 must complete the adapter, plan, trigger, scheduling, and readiness details before implementation.

---

## 4. Identity / lifecycle stress review

### Cases reviewed

#### Duplicate trigger
Two equivalent schedule/readiness events attempt to create the same logical operation.

Foundation behavior: logical uniqueness/idempotency prevents uncontrolled duplicate logical work; physical retries remain attempts.

**PASS conceptually; exact key algorithm deferred to A-11.**

#### Worker crash before child dispatch
Outer attempt is lost/failed; retry creates a new TDLA attempt under the same logical operation.

**PASS.**

#### Worker crash after child dispatch
The child job may continue. Recovery must reconcile the child reference before blindly creating duplicate work.

**PASS after V1.1 addendum; detailed recovery deferred to A-11/A-12.**

#### Event reschedule
Pending future work may become `SUPERSEDED`; replacement work references the new authoritative event timing while history remains.

**PASS.**

#### Intentional historical repeat
Replay, backfill, and reprocess are separate operations with explicit lineage rather than masquerading as retries.

**PASS.**

#### Market price changes
Price/provider observations do not automatically redefine TDLA logical identity unless the plan explicitly defines a new logical execution boundary.

**PASS as a foundational rule; exact trigger/plan semantics deferred.**

---

## 5. Configuration / environment review

### Cases reviewed

- production vs staging publication destinations;
- secret values changing without leaking into config hashes;
- authorized one-run override;
- config revision after a production run;
- accidental undocumented environment variable;
- configuration effect on future planned work.

### Finding

**PASS.**

A-4 makes environment part of audit/identity context, requires schema validation, hashes normalized non-secret effective configuration, separates secrets, records runtime overrides, and prohibits invisible production behavior.

Future A-20 must define secret backend/service identity details. M0/M1 must establish actual schema/validation implementation.

---

## 6. Vendor independence review

### Case

Replace Prefect with a different runtime after several years of production history.

### Finding

**PASS.**

Canonical TDLA run/attempt/plan identities are TDLA-owned; Prefect IDs are cross-references only. ADR-0001 records the decision and its costs.

Later M3 must prove this in implementation rather than merely claim it.

---

## 7. Documentation / project-memory review

### Requirements checked

- every material change leaves human-readable durable context;
- exact next work step is stored in repository;
- architecture status has one explicit authority;
- ADRs do not silently override architecture;
- long-running checkpoint logs cannot silently replace certification authority;
- change history is preserved instead of rewritten.

### Finding

**PASS.**

`AGENTS.md`, `CHANGE_JOURNAL.md`, `CURRENT_RESUME_POINT.md`, `ARCHITECTURE_CERTIFICATION_LOG.md`, and ADR policy establish the required hierarchy.

One operational improvement is required going forward: journal timestamps should use actual ISO-8601 timestamps rather than placeholder time-of-day values. This review records that requirement and future entries must comply.

---

## 8. Review findings summary

| Area | Initial result | Resolution | Final result |
|---|---|---|---|
| DDC ownership | ambiguity around `run/job lifecycle` terminology | V1.1 nested-lifecycle addendum | PASS |
| MLB ownership/manual-first | clean | none | PASS |
| NFL/NCAAF compatibility | clean at foundation level | detailed scheduling deferred | PASS |
| logical run / attempt identity | clean | exact idempotency deferred | PASS |
| replay/backfill/reprocess | clean | none | PASS |
| config/environment | clean | implementation deferred | PASS |
| Prefect independence | clean | ADR-0001 | PASS |
| documentation memory | clean | require actual timestamps going forward | PASS |

No unresolved contradiction remains that should block A-0 through A-4 from governing A-5 design.

---

# Certification decision

**A-0 through A-4: ARCHITECTURE-CERTIFIED V1 + V1.1 addendum.**

Certification means these contracts now govern future architecture/implementation. It does **not** mean runtime implementation exists.

Any later contradiction requires an explicit architecture revision/addendum or superseding version, corresponding ADR when appropriate, compatibility analysis, change-journal entry, and certification-log update.

---

# Exact next architecture step

Proceed to **A-5 — Sport Automation Adapter Contract**.

A-5 must specifically resolve the downstream requirements surfaced here:

1. sport adapter identity/version/capability handshake;
2. sport-provided scope/event references without TDLA canonicalizing sport ontology;
3. plan/readiness/result interfaces;
4. child/external execution references;
5. outer idempotency-reference propagation;
6. child timeout/cancellation/reconciliation semantics;
7. required vs optional capability declaration;
8. sport-defined degradation/failure reason codes;
9. artifact/result manifest contract;
10. manual/shadow/supervised/production mode capability;
11. compatibility/version negotiation;
12. explicit rule preventing adapter implementation from moving sport logic into TDLA.
