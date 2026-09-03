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

- **Change ID:** Initial architecture seed; commits created during 2026-09-02 repository pass.
- **Area:** architecture / documentation / governance.
- **Summary:** Established the first governing documentation for The-Daily-Line-Automation: repository mission, ownership boundaries, A-0 through A-4 architecture, implementation roadmap, architecture certification authority, change-documentation rules, and resume-point discipline.
- **Reason:** The repository was empty. The project intentionally starts architecture-first so the eventual multi-sport automation platform does not become a collection of sport-specific cron scripts or acquire undocumented implementation debt.
- **Files/components affected:** `README.md`; `AGENTS.md`; `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md`; `docs/architecture/README.md`; `docs/implementation/IMPLEMENTATION_ROADMAP_V1.md`; `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`; this journal; `CURRENT_RESUME_POINT.md`; ADR documentation created in the same foundation pass.
- **Authority/contract impact:** Establishes initial TDLA authority boundaries: DDC owns certified shared sport-agnostic acquisition/facts; sport repositories own sport intelligence; TDLA owns orchestration/operations; website/app owns product state. Establishes logical-run/attempt separation, manual-first automation authority, immutable history, versioned configuration/release identity, and replaceable orchestration infrastructure.
- **Data/migration impact:** None. No runtime schema exists yet.
- **Operational impact:** None in production. No automation is production-authoritative. Daily-MLB remains manual-first.
- **Validation/evidence:** Repository documents were created directly in the GitHub repository. Architecture status is intentionally `DOCUMENTED — REVIEW PENDING`, not self-certified. A dedicated architecture review is still required.
- **Risks/open questions:** A-5 through A-24 remain undefined. The exact Sport Automation Adapter shape, plan/stage schema, trigger semantics, scheduling identity, persistence DDL, and orchestration implementation details are not yet frozen.
- **Rollback/recovery:** Documentation-only foundation; future revisions must preserve history and document supersession rather than erase prior reasoning.
- **Next exact step:** Perform an A-0 through A-4 architecture review against Daily-Data-Core, Daily-MLB, and Daily-NFL boundaries. Correct any contradictions. If clean, mark A-0 through A-4 `ARCHITECTURE-CERTIFIED`, then design A-5 Sport Automation Adapter Contract.

---

## Journal rules

1. Entries are append-oriented history. Do not delete an old entry because the architecture later changes.
2. Corrections should be recorded as a new entry explaining what earlier assumption changed.
3. Large checkpoints may use a dedicated progress log, but major decisions/results must still be summarized here.
4. Every completed work session updates `docs/implementation/CURRENT_RESUME_POINT.md`.
5. Certification authority changes must also update `ARCHITECTURE_CERTIFICATION_LOG.md`.
