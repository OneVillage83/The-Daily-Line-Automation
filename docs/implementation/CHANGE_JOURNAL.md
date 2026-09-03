# The Daily Line Automation — Change Journal

Purpose: durable chronological human-readable memory for every material repository change.

This file is not a substitute for Git history; it records the context Git history alone does not preserve reliably: why a change occurred, what contract/authority it affected, what validation was performed, known risks, and the exact continuation point.

## Required entry template

Copy this template for future material changes.

```markdown
## YYYY-MM-DDTHH:MM:SSZ — <short title>

- **Change ID:** <commit / PR / milestone / ADR / local checkpoint>
- **Area:** <architecture | code | schema | config | dependency | CI | deployment | test | incident | docs | etc.>
- **Summary:** <precise description>
- **Reason:** <why this was necessary>
- **Files/components affected:** <paths/services/contracts>
- **Authority/contract impact:** <none or exact impact>
- **Data/migration impact:** <none or details>
- **Operational impact:** <none or details>
- **Validation/evidence:** <tests/commands/audits/results>
- **Risks/open questions:** <known limitations>
- **Rollback/recovery:** <when relevant>
- **Next exact step:** <specific continuation point>
```

If one work unit contains several logically distinct material changes, record them separately or make the subdivisions explicit enough that future maintainers can reconstruct each decision.

---

## 2026-09-02T00:00:00Z — Repository architecture/documentation foundation created

> Historical note: this first journal entry used a placeholder midnight timestamp during repository seeding. It preserves the original entry as written. The actual foundation/review work occurred on 2026-09-02 America/Los_Angeles; the later correction/certification entry below records an actual ISO-8601 timestamp. Future entries must use actual timestamps.

- **Change ID:** Initial architecture seed; commits created during 2026-09-02 repository pass.
- **Area:** architecture / documentation / governance.
- **Summary:** Established the first governing documentation for The-Daily-Line-Automation: repository mission, ownership boundaries, A-0 through A-4 architecture, implementation roadmap, architecture certification authority, change-documentation rules, and resume-point discipline.
- **Reason:** The repository was empty. The project intentionally starts architecture-first so the eventual multi-sport automation platform does not become a collection of sport-specific cron scripts or acquire undocumented implementation debt.
- **Files/components affected:** `README.md`; `AGENTS.md`; `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md`; `docs/architecture/README.md`; `docs/implementation/IMPLEMENTATION_ROADMAP_V1.md`; `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`; this journal; `CURRENT_RESUME_POINT.md`; ADR documentation created in the same foundation pass.
- **Authority/contract impact:** Establishes initial TDLA authority boundaries: DDC owns certified shared sport-agnostic acquisition/facts; sport repositories own sport intelligence; TDLA owns orchestration/operations; website/app owns product state. Establishes logical-run/attempt separation, manual-first automation authority, immutable history, versioned configuration/release identity, and replaceable orchestration infrastructure.
- **Data/migration impact:** None. No runtime schema exists yet.
- **Operational impact:** None in production. No automation is production-authoritative. Daily-MLB remains manual-first.
- **Validation/evidence:** Repository documents were created directly in the GitHub repository. Architecture status was intentionally `DOCUMENTED — REVIEW PENDING`, not self-certified. A dedicated architecture review was required.
- **Risks/open questions:** A-5 through A-24 remained undefined. The exact Sport Automation Adapter shape, plan/stage schema, trigger semantics, scheduling identity, persistence DDL, and orchestration implementation details were not yet frozen.
- **Rollback/recovery:** Documentation-only foundation; future revisions must preserve history and document supersession rather than erase prior reasoning.
- **Next exact step:** Perform an A-0 through A-4 architecture review against Daily-Data-Core, Daily-MLB, and Daily-NFL boundaries. Correct any contradictions. If clean, mark A-0 through A-4 `ARCHITECTURE-CERTIFIED`, then design A-5 Sport Automation Adapter Contract.

---

## 2026-09-03T05:53:00Z — A-0 through A-4 reviewed, lifecycle ambiguity resolved, foundation certified

- **Change ID:** A00-A04 certification pass; key commits include `6d93a656`, `f65f75d4`, `3d7dca95`, `41ea5ab4`, `ac9b41cb`, `708f6f0b`, `8495b2b7`.
- **Area:** architecture / governance / documentation.
- **Summary:** Performed the required cross-repository review of A-0 through A-4, identified a terminology ambiguity around `run/job lifecycle`, documented a nested lifecycle model, certified A-0 through A-4, synchronized the repository status/index/resume point, and finalized ADR-0001.
- **Reason:** The foundation was deliberately not self-certified. A review was required to prove TDLA would not duplicate DDC acquisition responsibilities, absorb sport logic, or couple canonical identity to Prefect.
- **Files/components affected:** `docs/architecture/A00-A04_FOUNDATION_ADDENDUM_V1_1.md`; `docs/implementation/A00-A04_ARCHITECTURE_CONFORMANCE_REVIEW_20260902.md`; `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`; `docs/architecture/README.md`; `README.md`; `docs/implementation/CURRENT_RESUME_POINT.md`; `docs/adr/ADR-0001_CONTROL_PLANE_AND_VENDOR_NEUTRAL_IDENTITY.md`; this journal.
- **Authority/contract impact:** A-0 through A-4 changed from `DOCUMENTED — REVIEW PENDING` to **`ARCHITECTURE-CERTIFIED`**. The V1.1 addendum clarifies that TDLA owns the **outer automation lifecycle**, while a sport service and DDC may retain nested child job/acquisition lifecycle identities. Cross-layer IDs are linked through provenance and never silently replaced.
- **Data/migration impact:** None. No runtime database/schema exists yet.
- **Operational impact:** No production authority granted. TDLA remains architecture-only. Daily-MLB remains manual-first. Future TDLA retries/recovery must reconcile child job references rather than blindly redispatch when outer state is lost.
- **Validation/evidence:** Reviewed current DDC ownership documentation, Daily-NFL F-0 through F-4 architecture, and the current Daily-MLB service/job boundary. Stress-tested duplicate triggers, worker failure before/after child dispatch, event reschedule, replay/backfill/reprocess, price changes, staging/production configuration separation, secret hashing boundaries, and Prefect replacement. Full evidence is recorded in `docs/implementation/A00-A04_ARCHITECTURE_CONFORMANCE_REVIEW_20260902.md`.
- **Risks/open questions:** Exact Sport Automation Adapter method/schema design remains undefined; nested idempotency propagation, child cancellation/reconciliation, exact logical key construction, trigger semantics, and persistence DDL are intentionally deferred to A-5/A-6/A-11/A-13. No implementation should guess them early.
- **Rollback/recovery:** Certification history is append-only. If a future contradiction is found, create a versioned addendum/superseding architecture and record migration impact rather than deleting this decision.
- **Next exact step:** Design `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_V1.md` using the detailed checklist and stress cases now stored in `docs/implementation/CURRENT_RESUME_POINT.md`.

---

## Journal rules

1. Entries are append-oriented history. Do not delete an old entry because the architecture later changes.
2. Corrections should be recorded as a new entry explaining what earlier assumption changed.
3. Large checkpoints may use a dedicated progress log, but major decisions/results must still be summarized here.
4. Every completed work session updates `docs/implementation/CURRENT_RESUME_POINT.md`.
5. Certification authority changes must also update `ARCHITECTURE_CERTIFICATION_LOG.md`.
6. Use an actual ISO-8601 timestamp for new entries; do not use placeholder time-of-day values.
