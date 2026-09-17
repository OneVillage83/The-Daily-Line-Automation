# EdgeStack Parlay Optimizer — Relocation Notice

**Status:** SUPERSEDED IN THIS REPOSITORY — CANONICAL OWNER MOVED TO DAILY-LINE-CORE  
**Relocation date:** 2026-09-17

EdgeStack is **not** owned by The-Daily-Line-Automation.

The canonical logical owner is now **Daily-Line-Core (DLC)**, the cross-sport decision aggregation and product-assembly layer that sits downstream of sealed sport decision packages and Daily-Data-Core market evidence, and upstream of the report, infographic, website, and automation consumers.

Until the dedicated `OneVillage83/Daily-Line-Core` repository is physically created, the canonical planning documents are staged at:

- `OneVillage83/Daily-Data-Core/docs/daily_line_core/README.md`
- `OneVillage83/Daily-Data-Core/docs/daily_line_core/DLC_ARCHITECTURE_V1.md`
- `OneVillage83/Daily-Data-Core/docs/daily_line_core/EDGESTACK_PARLAY_OPTIMIZER_V1.md`
- `OneVillage83/Daily-Data-Core/docs/daily_line_core/DLC_IMPLEMENTATION_HANDOFF_V1.md`
- `OneVillage83/Daily-Data-Core/docs/daily_line_core/DLC_REPOSITORY_BOOTSTRAP.md`

Physical repository creation/extraction is tracked in `OneVillage83/Daily-Data-Core#5`.

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
