# EdgeStack Implementation Handoff — Relocation Notice

**Status:** SUPERSEDED IN TDLA  
**Relocation date:** 2026-09-17

Do not implement EdgeStack inside The-Daily-Line-Automation.

The canonical implementation plan now lives in:

`OneVillage83/Daily-Line-Core`

Primary files:

- `CODEX_START_HERE.md`
- `docs/IMPLEMENTATION_ROADMAP.md`
- `docs/CURRENT_RESUME_POINT.md`
- `docs/EDGESTACK_PARLAY_OPTIMIZER_V1.md`

The former `Daily-Data-Core/docs/daily_line_core/` staging copy is historical only.

## Why this moved

EdgeStack and the All Bets Prediction Scanner are cross-sport product decision capabilities. They consume sealed sport decision packages plus point-in-time market evidence and create the final cross-sport recommendation/product package. TDLA is downstream and should receive sealed information after DLC has made and sealed those decisions.

## TDLA responsibility after relocation

TDLA may consume sealed DLC outputs for:

- video/social content;
- marketing automation;
- distribution/publication workflows;
- operational orchestration permitted by TDLA's own certified contracts.

TDLA does not own the EdgeStack optimizer, Recommendation Gate semantics, sport probabilities, or cross-sport recommendation ranking.

## Bridge note

The GrokBot-OpenAI-Bridge is being proven against TDLA first because TDLA is near completion and provides a bounded proving ground. That testing location does not confer ownership of DLC/EdgeStack logic on TDLA.

Once the Bridge proving-ground test is accepted and the authorized repository catalog is deliberately expanded, `OneVillage83/Daily-Line-Core` should be registered as its own repository/workstream.

The current DLC next step is **DLC-0 architecture/ownership conformance review**. The current TDLA core resume point remains its own A-series continuation unless the owner explicitly chooses a different TDLA task.
