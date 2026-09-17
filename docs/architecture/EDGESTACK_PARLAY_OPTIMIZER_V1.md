# EdgeStack Parlay Optimizer — Relocation Notice

**Status:** SUPERSEDED IN THIS REPOSITORY — CANONICAL OWNER IS DAILY-LINE-CORE  
**Relocation date:** 2026-09-17

EdgeStack is **not** owned by The-Daily-Line-Automation.

The canonical owner is now:

`OneVillage83/Daily-Line-Core`

Canonical documents include:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/OWNERSHIP_BOUNDARIES.md`
- `docs/INTEGRATION_CONTRACTS.md`
- `docs/EDGESTACK_PARLAY_OPTIMIZER_V1.md`
- `docs/IMPLEMENTATION_ROADMAP.md`
- `docs/CURRENT_RESUME_POINT.md`

The former `Daily-Data-Core/docs/daily_line_core/` staging directory is historical only.

## TDLA boundary

TDLA may consume a sealed `DailyLinePublicationPackage` or approved derivative `PublishableFactPackage` produced by DLC and use those facts for downstream workflows such as:

- social video;
- social posts;
- marketing content;
- publication/distribution automation;
- other operational automation.

TDLA must **not**:

- calculate sport fair probabilities;
- own Recommendation Gate semantics;
- assemble the All Bets product scanner;
- generate/rank EdgeStacks;
- reinterpret sport-native model output;
- silently recompute DLC product decisions.

Downstream automation may transform presentation only within the authority granted by the sealed DLC package.

The product identity remains:

> **The Daily Line EdgeStack Parlay Optimizer**  
> **Stack the Edge. Not the Odds.**
