# Daily WNBA Build Boundary V1

**Status:** EXISTING EMPTY REPOSITORY — ARCHITECTURE / IMPLEMENTATION NOT AUTHORIZED BY THIS FILE  
**Repository:** `OneVillage83/Daily-WNBA`

Read `SHARED_SPORT_BUILD_CONSTITUTION_V1.md` first.

## Authorization / separation from NBA

WNBA may reuse generic basketball components, but it requires its own roster/schedule/data-quality/calibration and promotion evidence. NBA model weights/calibrators are never copied into WNBA production authority by default.

## Mission

Model WNBA games and player props with league-specific roster, travel, availability, national-team/overseas context and smaller-sample uncertainty.

## Canonical sport truth

- teams, players, rosters, games, venues, coaches, lineups/substitutions and rule versions
- hardship/replacement/availability changes
- overseas/national-team/Olympic interruptions and special schedule context
- all state time-versioned

## Factual evidence

- PBP, box, lineup/substitution and shot/tracking data where available
- injuries/availability, starters, rotations, minute restrictions and transactions
- travel/rest/back-to-back/schedule density
- possession/shot/rebound/turnover/foul evidence validated on WNBA data

## Feature families

- opponent-adjusted offense/defense/pace and shooting/rebounding/turnover/free-throw components
- player minutes/opportunity/usage and lineup effects with strong shrinkage when needed
- roster continuity, travel/rest and replacement context
- league-specific shot/pace/rotation tendencies rather than NBA constants

## Target/market universe

- moneyline, spread, total, team totals
- supported quarter/half markets
- points/rebounds/assists/3PM/PRA combinations
- other props only with sufficient history

## Model Zoo direction

- WNBA-calibrated team-strength/efficiency baselines
- hierarchical lineup/player/minutes models
- nonlinear target models and possession simulation
- WNBA player usage/shot/rebound/assist specialists
- transfer learning from generic basketball tooling only when WNBA OOS evidence validates it

## Full build outline

| Phase | WNBA requirement |
|---|---|
| SB-0 | Create separate local authority even if implementation later shares packages with NBA. |
| SB-1 | Canonicalize roster/game/lineup/rule identity and special availability contexts. |
| SB-2 | Acquire PIT basketball/availability/schedule evidence and grade coverage. |
| SB-3 | Reconstruct active roster, starters, rotation and minutes state. |
| SB-4 | Build WNBA-calibrated possession/player/lineup/travel features. |
| SB-5 | Define supported game/player markets and settlement. |
| SB-6 | Establish WNBA baselines; NBA models may be benchmark comparators only. |
| SB-7 | Add WNBA-specific player/lineup/usage specialists with OOS proof. |
| SB-8 | Simulate possessions/scores/minutes/player outcomes and dependencies. |
| SB-9 | Calibrate/freeze independent WNBA Unified Line. |
| SB-10 | Join DDC market evidence only after freeze. |
| SB-11 | Apply WNBA Recommendation Gate and export SportDecisionPackage. |
| SB-12 | Evaluate by season phase, role, availability, rest and market. |
| SB-13 | Prove manual slate -> DLC/report handoff. |
| SB-14 | Later live basketball sibling with WNBA-specific calibration. |
| SB-15 | Automate only after manual certification. |

## Simulation / joint evidence

- propagate rotation/minutes uncertainty into player stats
- handle overtime and short-roster/role-concentration effects
- same-event joint evidence must be trained/validated on WNBA-relevant outcomes

## Uncertainty

Small league/sample size, travel/schedule interruptions and roster availability require explicit shrinkage. Low-volume prop markets may remain unsupported longer than NBA analogues.

## Live boundary

Live WNBA follows basketball state concepts but uses WNBA-trained/calibrated live models. Shared code is implementation reuse, not shared statistical authority.

## Anti-drift rules

- no "NBA model is WNBA-ready" claim without WNBA OOS proof
- no hiding smaller-sample uncertainty
- no forced prop coverage to match NBA
- no cross-sport product logic here

## Bridge stop conditions

Stop/escalate if a shared basketball model lacks WNBA validation, roster/availability state is incomplete, a prop lacks stable history/settlement, or competition interruptions cannot be PIT-reconstructed.

## Exit criteria

- WNBA-specific OOS calibration/uncertainty pass
- supported player markets have minutes/opportunity/settlement evidence
- SportDecisionPackage/DLC handoff sealed and replayable
- live/automation separately certified
