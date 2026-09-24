# DLADS Evaluation Gates

These are agent/workflow quality gates. They do not replace target-repository certification gates.

## Supervisor gate

PASS requires:

- target repo selected from verified current truth;
- exact governing docs identified;
- task is the highest-priority unblocked task or explicit user-selected track;
- scope/non-goals are explicit;
- correct specialist roles chosen;
- no authority boundary widened;
- exact next step remains recoverable if blocked.

Automatic fail examples: selecting a task from stale chat memory, skipping a newer repo-local resume point, or claiming certification without evidence.

## Engineering gate

PASS requires as applicable:

- diff conforms to target architecture/contracts;
- focused tests pass;
- type/lint/build checks appropriate to the repo pass;
- failure paths handled deliberately;
- no hidden dependency/config changes;
- migrations/version changes are explicit;
- change documentation/handoff is complete.

## Modeling gate

PASS requires as applicable:

- exact target and prediction cutoff are defined;
- point-in-time feature provenance is demonstrated;
- train/validation/OOS/holdout boundaries are leakage-safe;
- baselines exist;
- metrics match the target type;
- calibration/ensemble training uses eligible OOS evidence only;
- component models remain inspectable for attribution/ablation;
- no post-kickoff or post-event information contaminates pre-event inference;
- market information is isolated according to model independence policy;
- uncertainty and limitations are recorded.

## QA/Audit gate

PASS requires:

- independent review of completion claims;
- at least one adversarial/counterexample check for material logic changes;
- contract/temporal/failure evidence examined rather than only happy-path tests;
- exact source identity for evidence;
- `PASS_WITH_LIMITS` used when proof is bounded;
- unresolved substantive failures block promotion.

## Documentation gate

PASS requires:

- current vs historical state is unambiguous;
- exact continuation point exists;
- material change, reason, evidence, limits, rollback/recovery, and next step are recorded;
- cross-repo dependencies are linked rather than duplicated;
- DLADS state is updated only after authoritative repo docs/evidence are updated.

## Validation/CI gate

PASS requires:

- exact intended source/head verified;
- requested full suites/matrices completed;
- logs/run IDs/results retained as required;
- public mirrors, if used, have exact mapping to private source;
- transient vs substantive failures are classified;
- substantive failures are escalated, not papered over.

## GrokBot OpenAI Bridge / DLADS promotion gate

Before publishing any DLADS role as a persistent OpenAI runtime agent:

1. its manifest validates;
2. its instructions pass at least three representative dry-run evals;
3. one blocked-case eval proves it stops rather than inventing authority;
4. tool/data permissions are explicit and least-privilege;
5. expected model/tool cost is documented;
6. provider/runtime IDs remain metadata, not source-of-truth identifiers;
7. rollback to the prior agent version is possible.