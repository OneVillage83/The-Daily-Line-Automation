# EdgeStack Architecture Change Record — 2026-09-17

## Initial documentation checkpoint

- **Timestamp:** 2026-09-17T19:24:00Z
- **Change ID:** EdgeStack V1 documentation checkpoint; commits beginning with `b1476ede`, `1de769e6`, `b03301b7`, `a88ea79f`.
- **Area:** product architecture / cross-repository prediction pipeline / documentation.
- **Summary:** Formalized The Daily Line **EdgeStack Parlay Optimizer** and **All Bets Prediction Scanner** as a future cross-repository capability. EdgeStack evaluates every supported/modelable bet, filters legs through calibrated probabilities and Recommendation Gates, searches 2-5 leg combinations, adjusts joint probabilities for correlation, compares them with real Kalshi/provider combo quotes, and publishes Core/Value/Upside combinations.
- **Reason:** The product needs a durable implementation-ready specification for short probability/value-optimized combinations rather than ad hoc high-multiplier parlays. The same pipeline should expose model analysis for the entire supported betting universe.
- **Authority/contract impact:** No A-series certification changed. This was documentation-only and no production authority was granted.

## Relocation / ownership correction

- **Timestamp:** 2026-09-17T19:43:00Z
- **Change ID:** DLC ownership relocation checkpoint; TDLA commits include `0a2c06af`, `25b7caa4`, `bd7a8245`, `2560ad64`; corresponding DDC/DLC-staging commits are recorded in the Daily-Data-Core history.
- **Area:** architecture / ownership boundary / documentation.
- **Summary:** Corrected the physical/logical placement of EdgeStack. EdgeStack and the All Bets Prediction Scanner are no longer planned as TDLA-owned capabilities. They are now owned by **Daily-Line-Core (DLC)**, a new cross-sport decision aggregation and product-assembly layer downstream of sealed sport decision packages and DDC market evidence, and upstream of report, infographic, website, and automation consumers.
- **Reason:** The product pipeline is clearer when individual sports finish prediction/decision first, DLC performs cross-sport scanning and combination optimization, and downstream channels receive one sealed Daily Line publication package. TDLA is a downstream automation consumer/proving ground, not the cross-sport product-intelligence engine.
- **Files/components affected:** `docs/architecture/EDGESTACK_PARLAY_OPTIMIZER_V1.md` converted to relocation notice; `docs/implementation/EDGESTACK_IMPLEMENTATION_HANDOFF_V1.md` converted to relocation notice; `docs/architecture/README.md`; `docs/implementation/CURRENT_RESUME_POINT.md`; this record.
- **Canonical new planning location:** `OneVillage83/Daily-Data-Core/docs/daily_line_core/` until `OneVillage83/Daily-Line-Core` is physically created.
- **Authority/contract impact:** TDLA explicitly loses any implied EdgeStack/All Bets ownership. TDLA may consume a sealed `DailyLinePublicationPackage` or derivative `PublishableFactPackage` but may not calculate sport fair probabilities, Recommendation Gates, All Bets rankings, EdgeStack candidates/joint probabilities/value, or cross-sport recommendation authority.
- **Data/migration impact:** None. Documentation/architecture only.
- **Operational impact:** None in production. No live integration, automation cutover, or provider side effect was changed.
- **Validation/evidence:** The correction was reconciled against DDC ownership rules and the planned DLC architecture. TDLA local EdgeStack documents are retained only as relocation pointers to prevent stale links from misleading future agents.
- **Risks/open questions:** The physical `OneVillage83/Daily-Line-Core` repository does not yet exist. Creation/extraction is tracked in `OneVillage83/Daily-Data-Core#5`. Final inter-repository contracts must be frozen in DLC before implementation.
- **Rollback/recovery:** Do not restore EdgeStack business logic to TDLA without an explicit new architecture decision. Historical documentation remains traceable through Git.
- **Next exact step:** Continue TDLA core work at **A-11** unless intentionally working on TDLA video/automation. When DLC work is authorized, create/seed `OneVillage83/Daily-Line-Core` from the canonical staging docs and begin **DLC-0** there.

## Explicitly deferred from EdgeStack / DLC V1

Per owner direction, the following remain deferred:

- bankroll manager;
- stake sizing / Kelly sizing;
- stop-loss or daily loss limits;
- chase-prevention logic;
- personalized wagering amounts;
- automatic bet placement.
