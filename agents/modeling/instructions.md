# Modeling Specialist Instructions

## Scientific contract

Before modeling, define the prediction target, event/prediction cutoff, eligible feature time, training window, OOS window, holdout policy, metrics, and market-independence policy.

## Requirements

- no post-kickoff/post-event information in pregame predictions;
- all feature inputs must be point-in-time reconstructable;
- keep true holdout evidence separate from tuning/training;
- compare against appropriate baselines;
- retain component model outputs and provenance;
- calibrators/stackers learn from eligible OOS predictions, not in-sample fits;
- learned ensemble importance must be auditable globally and conditionally;
- a weak overall model may retain narrow conditional weight only if OOS evidence supports it;
- market features are separate from market-independent model families unless the governing design explicitly permits them.

## Unified Line direction

Preserve independent component models, learn governed combination/stacking, calibrate final probabilities/lines, and expose attribution/ablation so the Unified Line is explainable and regressions can be isolated.

Never promote a model to production solely because a backtest improved. Return evidence for the target repo's registry/promotion gate.