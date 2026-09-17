# EdgeStack Implementation Handoff — Relocation Notice

**Status:** SUPERSEDED IN TDLA  
**Relocation date:** 2026-09-17

Do not implement EdgeStack inside The-Daily-Line-Automation.

The canonical implementation plan is now staged for **Daily-Line-Core (DLC)** at:

- `OneVillage83/Daily-Data-Core/docs/daily_line_core/DLC_IMPLEMENTATION_HANDOFF_V1.md`
- `OneVillage83/Daily-Data-Core/docs/daily_line_core/DLC_REPOSITORY_BOOTSTRAP.md`

The final physical home will be `OneVillage83/Daily-Line-Core` after repository creation.

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

Once the bridge proving-ground test is accepted and the authorized repository catalog is expanded, DLC should be registered as its own repository/workstream and implemented beginning with **DLC-0** in the canonical DLC handoff.

The current TDLA core resume point remains **A-11 Retry / Timeout / Idempotency Architecture** unless the owner explicitly chooses a different TDLA task.
