# Daily Line Repository Registry

This registry defines **ownership**, not implementation status. Live status must be verified from each repository before work.

| Repository | Program role | Authority boundary | Start/resume documents |
|---|---|---|---|
| `OneVillage83/Daily-Data-Core` | Shared data/provider core | Generic odds/weather/provider facts, evidence, shared temporal/data contracts; not sport intelligence | Read root `AGENTS.md`/README and current implementation/status docs discovered at audit time |
| `OneVillage83/Daily-MLB` | MLB sport authority | MLB identity/state/features/models/simulation/fair price/value/gate/settlement/publishable sport truth | `AGENTS.md`, `CODEX_START_HERE.md`, newest exact handoff/status docs |
| `OneVillage83/Daily-NFL` | NFL sport authority | NFL identity/state/play taxonomy/features/models/simulation/fair price/value/gate/settlement/publishable sport truth | `AGENTS.md`, `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`, newest implementation receipt/handoff |
| `OneVillage83/Daily-NCAAF` | NCAAF sport authority | College-football team hierarchy/state/features/models/simulation/gate/settlement/publishable sport truth | README + docs until repo-local agent/resume constitution is established |
| `OneVillage83/Daily-Model-Core` | Shared model lifecycle/core | Reusable contracts, registry, OOS truth/evaluation, reference model families, calibration/ensemble infrastructure; not sport feature meaning | `AGENTS.md`, `CODEX_START_HERE.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/ROADMAP.md` |
| `OneVillage83/The-Daily-Line-website` | Customer product/UI | Product presentation, history/search, report access, account/subscription UX; never sport truth | README + repo-local status/dev docs |
| `OneVillage83/The-Daily-Line-Automation` | Runtime orchestration + DLADS home | Scheduling/workflows/workers/readiness/retry/idempotency/observability/review/distribution; no sport intelligence | root `AGENTS.md`, `docs/implementation/CURRENT_RESUME_POINT.md`, architecture certification log |
| `OneVillage83/Daily-Line-Private-Validation` | Private validation evidence | Supplemental validation/CI evidence only; does not replace private source authority | repo-local README/docs; preserve exact source SHA mapping |
| `OneVillage83/Daily-MLB-Public-CI` | Sanitized public CI mirror | Supplemental validation only; never authoritative MLB source | mirror policy and exact private->public mapping |

## Future sport repositories

`Daily-NBA`, `Daily-NCAAB`, `Daily-WNBA`, `Daily-NCAAWB`, `Daily-NHL`, `Daily-Soccer`, `Daily-Tennis`, `Daily-Golf`, `Daily-MMA`, `Daily-Boxing`, `Daily-Motorsports`, `Daily-Esports`, and future sports follow the same rule: shared infrastructure can be reused, but sport interpretation remains in the sport repo.

## Cross-repo ownership rules

1. Do not copy shared provider/fact infrastructure into sport repos when Daily-Data-Core owns it.
2. Do not move sport-specific feature or causal semantics into Daily-Model-Core.
3. Do not put sport truth into TDLA, the website, or video/content systems.
4. A public mirror or validation repo is evidence, not source authority.
5. The supervisor must inspect the target repo's local constitution before proposing edits.
6. If ownership is ambiguous, the supervisor creates an architecture question/ADR task instead of silently choosing a home.

## Registry update rule

Add a repository only when its program responsibility and source-of-truth boundary are explicit. Changes to ownership are material architecture changes and require a durable decision record.