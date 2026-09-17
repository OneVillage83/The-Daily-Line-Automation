# EdgeStack Architecture Change Record — 2026-09-17

- **Timestamp:** 2026-09-17T19:24:00Z
- **Change ID:** EdgeStack V1 documentation checkpoint; commits beginning with `b1476ede`, `1de769e6`, `b03301b7`, `a88ea79f`.
- **Area:** product architecture / cross-repository prediction pipeline / documentation.
- **Summary:** Formalized The Daily Line **EdgeStack Parlay Optimizer** and **All Bets Prediction Scanner** as a future cross-repository capability. EdgeStack evaluates every supported/modelable bet, filters legs through calibrated probabilities and Recommendation Gates, searches 2-5 leg combinations, adjusts joint probabilities for correlation, compares them with real Kalshi/provider combo quotes, and publishes Core/Value/Upside combinations. Added a bounded ES-0 through ES-10 implementation handoff for GrokBot-OpenAI-Bridge / Codex.
- **Reason:** The product needs a durable implementation-ready specification for short probability/value-optimized combinations rather than ad hoc high-multiplier parlays. The same pipeline should expose model analysis for the entire supported betting universe, making the parlay optimizer a first-class product differentiator.
- **Files/components affected:** `docs/architecture/EDGESTACK_PARLAY_OPTIMIZER_V1.md`; `docs/implementation/EDGESTACK_IMPLEMENTATION_HANDOFF_V1.md`; `docs/architecture/README.md`; `docs/implementation/CURRENT_RESUME_POINT.md`; this change record.
- **Authority/contract impact:** No existing A-series certification changed. TDLA remains orchestration-only and must not own sport fair-probability, Recommendation Gate, or EdgeStack value logic. The physical runtime owner for EdgeStack must be frozen by ADR at ES-0 before implementation. The current core TDLA resume point remains A-11.
- **Data/migration impact:** None. Documentation only; no schemas, databases, migrations, production services, or provider integrations were created.
- **Operational impact:** None. No production recommendations, automation authority, publication side effects, or betting/order placement were enabled.
- **Validation/evidence:** Documentation was written against the current TDLA ownership constitution and explicitly preserves DDC/sport-repo/website/TDLA boundaries. The implementation plan requires point-in-time validation, calibrated joint probabilities, quote provenance, and same-game correlation handling before production authority.
- **Risks/open questions:** Final physical repo/package ownership for the EdgeStack Engine is intentionally unresolved until ES-0 ADR. Exact shared market-key contracts, provider RFQ interfaces, calibration promotion thresholds, and website publication schema must be finalized during the ES-series. Provider APIs may not expose every UI market/quote programmatically.
- **Rollback/recovery:** Documentation-only. If product direction changes, supersede/version the EdgeStack architecture and retain this record for history rather than deleting it.
- **Next exact step:** Core TDLA continues at **A-11 Retry / Timeout / Idempotency Architecture**. When the owner explicitly requests EdgeStack implementation, begin **ES-0: ownership ADR + canonical contracts/fixtures**, one authorized repository per Bridge/Codex turn.

## Explicitly deferred from EdgeStack V1

Per owner direction, the following are intentionally left for a later architecture phase:

- bankroll manager;
- stake sizing / Kelly sizing;
- stop-loss or daily loss limits;
- chase-prevention logic;
- personalized wagering amounts;
- automatic bet placement.

These must not be silently added during ES-0 through ES-10 implementation.
