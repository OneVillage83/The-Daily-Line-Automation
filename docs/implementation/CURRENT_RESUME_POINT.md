# The Daily Line Automation — Current Resume Point

Last updated: 2026-09-04 (America/Los_Angeles)  
Authority: This file is the single exact continuation point for unfinished TDLA work. It does not override architecture/certification authority; it tells the next session where to resume.

## Current project state

- Repository constitution/documentation-memory policy is authoritative in `AGENTS.md`.
- A-0 through A-4 Foundation V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-5 Sport Automation Adapter V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-6 Pipeline Plan / Stage Contracts V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-7 Trigger Architecture V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-8 Event-Relative Scheduling Engine V1 + V1.1 are **ARCHITECTURE-CERTIFIED**.
- A-8 review evidence: `docs/implementation/A08_ARCHITECTURE_CONFORMANCE_REVIEW_20260904.md`.
- ADR-0001: TDLA canonical identity / replaceable orchestration runtime.
- ADR-0002: transport-neutral Sport Automation Adapter protocol.
- ADR-0003: immutable plan fragments / explicit composition / resolved-plan authority.
- ADR-0004: durable trigger evidence / reevaluation-only trigger authority.
- ADR-0005: stable schedule slots / immutable resolved-time authority / reevaluation-only due events.
- No production implementation milestone is certified.
- No TDLA automation is production-authoritative.
- Daily-MLB remains manual-first; later automation must prove equivalence after its final manual production pipeline is certified.

## Certified nested architecture through A-8

```text
sport-owned scope/discovery/plan fragment
        +
TDLA platform fragment(s)
        |
        v
explicit PlanAssembly + typed bindings
        |
        v
immutable ResolvedAutomationPlan
        |
        v
StageDefinition / StageMaterialization
        |
        +------------------------------+
        |                              |
        v                              v
A-6 TimingDeclaration             A-7 TriggerBinding
        |                              |
        v                              v
A-8 ScheduleResolution        TriggerDelivery
        |                              |
        v                              v
A-8 ScheduleOccurrence        immutable TriggerEvent
        |                              |
        +------ TIME_DUE ------------> TriggerEvaluation
                                       |
                              EligibilityReevaluationRequest
                                       |
                                       v
                           A-9 dependency/readiness/current-
                              authority eligibility engine
                                       |
                                       v
                              later StageRun / RunAttempt
                                       |
                                       v
                         A-5 Sport Automation Adapter
                                       |
                                       v
                            sport child job/service
                                       |
                                       v
                         DDC/provider evidence where used
```

## Important locked A-7 rules

1. A trigger requests eligibility reevaluation only; it never grants execution or side-effect authority.
2. Physical `TriggerDelivery`, semantic `TriggerEvent`, source occurrence/revision, `TriggerEvaluation`, logical `EligibilityReevaluationRequest`, StageRun, and RunAttempt are separate identities.
3. Corrections/retractions are immutable linked revisions; same source occurrence/revision with conflicting semantic payload fails closed.
4. Accepted trigger evidence and causal reevaluation intent must be durable before downstream irreversible action.
5. Trigger deduplication and A-11 final StageRun idempotency are separate defenses.
6. Stale/out-of-order trigger evidence cannot roll plan/scope/schedule authority backward.
7. Sport-change hints remain opaque; A-5 sport readiness remains authoritative when required.
8. No timer/webhook/callback/operator trigger can directly execute or publish.

## Important locked A-8 rules

1. `ScheduleSlotRef` is stable logical scheduling intent; resolved wall-clock timestamp is not snapshot/stage identity.
2. Production `ScheduleResolution` binds exact plan, stage materialization, timing declaration, sport scope/schedule revision, anchor value/revision, resolved window, missed-policy, environment, and mode authority.
3. Event/schedule changes create new immutable schedule resolutions and supersede pending old authority rather than mutate history.
4. A new sport schedule revision remains new authority even if the absolute UTC start instant is unchanged; runtime timer wakeups may be reused without collapsing provenance.
5. `ScheduleOccurrence` is logical due identity; physical scheduler callback/scan/claim IDs are not canonical.
6. One logical `ScheduleOccurrence` maps to at most one canonical semantic A-7 `TIME_DUE` TriggerEvent for that exact authority.
7. Due-time boundary selection is explicit. A declaration cannot silently guess between earliest/target/anchor/recurrence time.
8. Earlier reschedules that make slots overdue are classified independently through immutable missed-window policy; there is no "run every missed stage immediately" behavior.
9. Normative missed-window policy families are reevaluation-only: `SKIP_MISSED`, `REQUEST_REEVALUATION_IF_WITHIN_GRACE`, `REQUEST_IMMEDIATE_REEVALUATION`, `SUPERSEDE_NO_ACTION`, `REQUIRE_OPERATOR_REVIEW`.
10. Missed/grace handling never directly executes sport work.
11. TBD/unresolved event anchors receive no invented placeholder time.
12. Stale old timer callbacks cannot revive superseded work.
13. An old already-emitted `TIME_DUE` event remains historical evidence but must be revalidated against current schedule authority before later dispatch.
14. Scheduler restart/downtime/multiple replicas must converge on the same logical occurrence/event evidence.
15. Event-relative duration arithmetic uses resolved UTC instants; local recurring schedules explicitly handle DST ambiguous/nonexistent civil times.
16. Customer-visible/destructive late work gets no generic catch-up permission.
17. Prefect/APScheduler/CronJob/queue/cron IDs are runtime cross-references only.
18. No direct scheduler-to-executor path exists.

## Daily-MLB / football compatibility note that must not be forgotten

Future sport integrations remain responsible for canonical event/schedule identity and readiness meaning.

TDLA must not implement:

```text
if MLB lineup posted -> READY
if probable pitcher changed -> rerun
if NFL inactive list final -> READY
if weather changed enough -> rerun
```

A future sport adapter instead provides opaque sport scope/revision, readiness disposition/evidence, and plan/output contracts. A-8 handles only generic time authority.

Current Daily-MLB remains manual-first and is **not** production scheduled merely because A-8 is certified.

---

# Exact next step — A-9 Dependency / Readiness Engine

Design the deterministic eligibility engine that combines:

- A-6 dependency/input/output graph contracts;
- A-5 sport-provided readiness evaluations;
- A-7 logical eligibility-reevaluation causes;
- A-8 current schedule/time authority;
- current plan/stage/scope/materialization authority;

into one auditable answer to:

> **Is this exact stage materialization currently eligible to proceed toward dispatch, and if not, precisely what generic gate is holding it?**

The central A-9 rule should be:

> **`READY` is a derived, versioned eligibility result over exact current authority and evidence—not a permanent mutable flag. Any execution-affecting authority/evidence change can invalidate it before dispatch, so stale eligibility evidence must fail closed or be reevaluated.**

A-9 must not interpret sport meaning and must not itself execute the stage.

## A-9 must define at minimum

### 1. Eligibility authority entities

Define clear identities/contracts for concepts such as:

- `EligibilityEvaluation` / immutable evaluation result;
- `DependencyEvaluation`;
- `ReadinessEvaluationRef` / A-5 readiness evidence binding;
- `TimeEligibilityRef` / current A-8 schedule authority binding;
- `CurrentAuthorityCheck`;
- `EligibilityDisposition`;
- logical reevaluation request identity from A-7;
- physical evaluation attempt identity;
- eligibility result digest/version;
- optional short-lived `DispatchEligibilityGrant` or equivalent current-authority handoff if architecture review supports it.

Exact names may change, but immutable evaluation identity and physical attempt identity must remain separate.

### 2. Current-authority gate first

Before evaluating readiness/dependencies for dispatch authority, confirm the evaluation targets the current allowed:

- resolved plan digest;
- stage definition/materialization;
- sport scope/scope revision;
- schedule resolution/occurrence when time-bound;
- execution mode/environment;
- policy/config references relevant to eligibility.

A superseded plan/scope/schedule/materialization cannot become current simply because old dependencies/readiness were once satisfied.

### 3. Generic eligibility dispositions

Define a state/result vocabulary that distinguishes at minimum conceptually:

- `NOT_CURRENT` / superseded authority;
- `NOT_APPLICABLE`;
- `WAITING_TIME` / not yet time-eligible;
- `MISSED_TIME_WINDOW` / late policy says no normal proceed;
- `WAITING_DEPENDENCY`;
- `WAITING_READINESS`;
- `BLOCKED_DEPENDENCY`;
- `BLOCKED_READINESS`;
- `BLOCKED_POLICY` / generic contract/policy gate where appropriate;
- `READY_FOR_DISPATCH`;
- `TERMINAL_NO_ACTION` where plan semantics resolve no work;
- evaluation error/retryable/terminal states without conflating them with domain blocked states.

Exact enum names can be refined, but reasons must remain distinguishable.

### 4. Dependency edge evaluation

Implement the semantics already declared by A-6, including generic edge/input requirements such as:

- upstream terminal success;
- required logical output exists and validates;
- specific accepted terminal disposition when intentionally consumed;
- fan-in exact membership completion;
- declared optional/conditional behavior;
- `NO_OP` satisfaction only where explicitly permitted;
- `SUCCEEDED_DEGRADED` satisfaction only for validated outputs/dependencies allowed by policy.

Do not treat `OPTIONAL` as automatically ignorable.

### 5. Exact upstream revision/output binding

Dependency satisfaction must bind the exact upstream StageRun/materialization/output manifest/schema/digest required by the resolved plan.

A downstream stage cannot silently consume:

- an artifact from a superseded plan;
- the wrong event/scope revision;
- a stale output from an older schedule slot;
- a similarly named file from another run;
- an output whose schema/digest contract no longer matches.

### 6. Fan-in/barrier semantics

For slate/aggregate stages, bind exact A-6 `ScopeSetBinding` membership revision/digest.

Define how barrier satisfaction treats each declared child disposition:

- succeeded;
- degraded;
- no-op;
- not applicable;
- failed terminal;
- cancelled/superseded;
- missing/unmaterialized.

TDLA cannot guess "all games are done" by parsing sport IDs or current date.

### 7. A-5 readiness evaluation

When the plan declares readiness is required, A-9 requests/uses A-5 `ReadinessResult`:

- `READY`;
- `WAITING`;
- `BLOCKED`;
- `NOT_APPLICABLE`.

The sport-provided reason code remains opaque except for declared generic routing/diagnostic use.

TDLA must not encode sport reason branches.

### 8. Readiness freshness / validity

A readiness result can expire or become stale.

A-9 must respect:

- evaluated_at;
- readiness_valid_until when supplied;
- max acceptable age from A-6 declaration;
- scope/schedule/readiness evidence revision;
- required input freshness/provenance references.

A once-`READY` result is not permanent permission.

### 9. Readiness revision/change invalidation

If new sport scope/state/readiness authority arrives after an evaluation:

- old readiness remains historical evidence;
- current eligibility may require reevaluation;
- no mutable `ready=true` flag is silently carried forward;
- if the stage already dispatched, later A-12/reprocess/correction policy decides what follows.

### 10. Time gate from A-8

A-9 validates current time authority rather than trusting that an old `TIME_DUE` trigger exists.

Confirm as applicable:

- correct current schedule resolution;
- slot is time-eligible;
- deadline/validity/grace policy permits reevaluation/proceeding;
- old superseded `TIME_DUE` is not current authority;
- stage did not become no-longer-applicable after reschedule.

### 11. Dependency vs readiness ordering

Choose a deterministic evaluation order optimized for correctness and avoiding unnecessary external sport calls.

Likely generic order:

1. current authority/applicability;
2. time/window eligibility;
3. static/known dependency satisfaction;
4. readiness freshness/cache eligibility;
5. call/refresh A-5 readiness if required;
6. final authority recheck before granting dispatch eligibility.

Review whether this order is normative or policy-controlled, but the final result must not depend nondeterministically on worker timing.

### 12. TOCTOU / final revalidation

Critical boundary:

```text
A-9 evaluates READY at 12:40:00
sport schedule revision changes at 12:40:01
worker attempts dispatch at 12:40:02
```

A stale eligibility result cannot be treated as permanent permission.

Define a final current-authority check or a short-lived/version-bound dispatch eligibility handoff so plan/scope/schedule/dependency/readiness authority cannot silently change between evaluation and dispatch.

A-10/A-11 implementation will consume this contract.

### 13. Eligibility result identity/digest

An immutable evaluation should bind at least:

- resolved plan digest;
- stage materialization;
- scope/schedule revision;
- current schedule resolution/time evaluation where applicable;
- dependency evaluations/upstream result refs;
- readiness result ref/digest/freshness;
- relevant policy/config digests;
- trigger/reevaluation causal refs;
- evaluated_at;
- disposition/reason set;
- schema/version/digest.

Presentation text does not affect semantic identity unless schema declares it semantic.

### 14. Cause vs result separation

A-7 `EligibilityReevaluationRequest` is a cause to evaluate, not the eligibility result itself.

Many trigger events may coalesce into one current evaluation when authority permits, while all raw causes remain linked/auditable.

Repeated evaluation attempts do not create new sport work by themselves.

### 15. Dependency state changes as reevaluation causes

When an upstream stage changes terminal/output state, affected downstream materializations may receive an A-7 dependency-change reevaluation cause.

A-9 evaluates current graph authority; it does not rely solely on push delivery correctness. Recovery/scans can reconstruct current dependency status.

### 16. Terminal upstream failure behavior boundary

A-9 decides generic dependency satisfaction from the resolved contract.

It does not invent generalized recovery action.

Examples:

- required success edge + upstream terminal failure -> blocked/unsatisfied;
- terminal-evidence-consuming edge may be satisfied if explicitly declared;
- optional branch may allow continuation if no required downstream output depends on it.

A-12 owns broader failure/degradation/recovery policy.

### 17. `NO_OP` / `NOT_APPLICABLE`

Preserve distinct meanings:

- plan/materialization `NOT_APPLICABLE` means no dispatch for that stage authority;
- successful `NO_OP` can satisfy only edge/output contracts that explicitly permit it;
- a `NO_OP` cannot fabricate an absent required output.

### 18. Degraded success

`SUCCEEDED_DEGRADED` may satisfy only the exact downstream requirements whose validated outputs/policy allow degradation.

A generic downstream stage cannot assume all degraded upstream outputs are usable.

### 19. Input freshness / PIT boundary

When resolved contracts require input freshness/cutoff constraints, A-9 must validate the declared generic metadata/provenance requirements.

Sport interpretation remains sport-owned.

For pregame predictions, nothing in A-9 may allow information with defensible availability after the applicable prediction cutoff to satisfy a PIT-bound input contract.

Exact sport PIT semantics remain in sport repos; A-9 enforces the declared contract metadata.

### 20. Readiness source failure

Distinguish:

- sport readiness returns `WAITING`/`BLOCKED` as domain result;
- adapter/readiness call fails technically;
- cached prior readiness is still valid;
- cached prior readiness expired;
- adapter capability unavailable/incompatible.

Do not convert a technical readiness failure into `READY` or a sport-defined `BLOCKED` silently.

A-12 owns broader retry/recovery classification.

### 21. Multiple readiness dimensions

If a stage requires more than one readiness predicate/service result, define an explicit composite contract rather than hardcoded sport logic.

Possible generic composition:

- `ALL_REQUIRED`;
- declared optional readiness dimensions;
- versioned named predicates/ports supplied by sport adapter.

Do not invent implicit boolean precedence.

### 22. Readiness caching

Caching can reduce sport-service calls but cache identity must bind:

- stage/scope/revision;
- readiness contract version;
- evidence/result digest;
- validity/freshness boundary.

A cache hit cannot cross incompatible authority revisions.

### 23. Concurrency / simultaneous reevaluations

Two trigger causes or workers may evaluate the same stage concurrently.

Both may produce equivalent evaluation evidence, but they must not create duplicate StageRuns.

A-11 remains final logical execution idempotency defense.

Determine whether A-9 should deduplicate/coalesce equivalent current eligibility evaluations for efficiency while retaining causal links.

### 24. READY does not equal dispatched

`READY_FOR_DISPATCH` means all A-9 gates pass under exact recorded authority at evaluation time.

It does not mean:

- a worker is available;
- resource budgets permit immediate start;
- A-10 dispatch succeeded;
- A-11 idempotency/retry gate passed;
- side effect executed.

Keep these lifecycle stages separate.

### 25. Current-authority handoff to A-10/A-11

Define what evidence A-10/A-11 must receive to prove that dispatch corresponds to the exact A-9 evaluation authority.

Potential contract:

```text
DispatchEligibilityGrant
- eligibility evaluation id/digest
- stage materialization
- plan/scope/schedule revisions
- readiness/dependency authority digests
- issued_at
- expires_at or revalidation requirement
- environment/mode
```

Review whether a grant object is best or whether dispatch performs inline final revalidation. Whichever approach is certified must fail closed on stale authority.

### 26. Supersession after READY but before dispatch

If plan/scope/schedule/materialization becomes superseded after READY:

- old eligibility remains audit evidence;
- old grant/evaluation cannot authorize new dispatch;
- current reevaluation happens under new authority;
- no mutation of old evidence.

### 27. Stage already terminal

A reevaluation request for a stage already terminal should generally resolve to explicit no-current-action/terminal disposition rather than launch duplicate work.

Replay/reprocess are separate explicitly lineaged operations under A-14.

### 28. No-games / empty-set behavior

A zero-game slate may have no event StageMaterializations.

Do not fabricate dependency work.

A declared aggregate/platform stage may evaluate against the explicit empty `ScopeSetBinding` behavior certified in A-6.

### 29. Shadow / supervised / production

A-9 includes execution mode/current plan authority in eligibility.

- shadow readiness can become ready only for shadow-safe path;
- supervised customer-visible downstream stage may remain policy/approval-blocked even when sport readiness is ready;
- production eligibility requires production-authorized current plan/integration policy.

A-19 owns explicit approval action mechanics.

### 30. Post-event settlement/evaluation

The same dependency/readiness engine supports postgame work:

- event completion/timing condition;
- required final result inputs;
- sport-owned settlement readiness;
- upstream artifact dependencies.

TDLA still does not interpret sport settlement rules.

### 31. Deterministic reason sets

Eligibility should retain structured generic blocking/satisfaction reasons.

Multiple gates may be unsatisfied simultaneously. Decide whether evaluation reports:

- first blocking gate only; or
- complete deterministic reason set.

Preference for review: complete deterministic reason set when safely available, while preserving deterministic ordering/canonicalization.

### 32. Error vs domain waiting distinction

Do not conflate:

- `WAITING_READINESS` because sport says not ready;
- technical adapter timeout/error;
- malformed readiness result;
- stale cache;
- missing capability.

Operational failures are evidence for later retry/incident behavior, not sport-state facts.

### 33. Evaluation recovery after crash

Durable reevaluation cause/evidence must allow evaluation to retry after process loss.

If the evaluation result was already durably recorded but acknowledgement/state update was lost, recovery should find/reuse equivalent immutable evidence where appropriate rather than create contradictory current states.

A-13 will define transaction/unique-key mechanics.

### 34. Technology neutrality

Do not make eligibility identity/state depend canonically on:

- Prefect task state;
- Celery result state;
- queue acknowledgement;
- process-local booleans;
- Redis lock identity.

These may be runtime cross-references only.

### 35. No direct readiness-to-execution path

Prohibit:

```text
sport adapter returns READY -> run model immediately
```

Require:

```text
A-5 readiness evidence
    + A-6 dependency/output contracts
    + A-8 current time authority
    + current plan/scope/materialization authority
        -> A-9 eligibility result
            -> A-10/A-11 dispatch/idempotency path
```

---

# A-9 stress cases before certification

At minimum test:

1. Time due, dependencies satisfied, readiness `READY` -> `READY_FOR_DISPATCH` under current authority.
2. Time not yet eligible but readiness already `READY` -> `WAITING_TIME`.
3. Time due, required upstream still running -> `WAITING_DEPENDENCY`.
4. Time due/dependencies satisfied, readiness `WAITING` -> `WAITING_READINESS`.
5. Readiness `BLOCKED` with sport-defined opaque reason -> generic blocked disposition without sport branching.
6. Readiness `NOT_APPLICABLE` -> no dispatch, explicit applicability result.
7. A readiness result was `READY` but `readiness_valid_until` expired one second before dispatch.
8. Readiness max-age from A-6 is stricter than adapter's own validity interval.
9. New sport scope/readiness revision arrives after prior `READY` evaluation.
10. Event reschedule supersedes old A-8 resolution after `TIME_DUE` emitted but before dispatch.
11. Plan revision supersedes a previously `READY` stage.
12. Stage materialization becomes `NOT_APPLICABLE` after previous waiting state.
13. Required upstream succeeds but required output manifest is missing.
14. Required output exists but schema version incompatible.
15. Required output exists but digest/provenance reference mismatches plan contract.
16. Upstream `SUCCEEDED_DEGRADED` produces required output that policy explicitly accepts.
17. Upstream degraded result lacks one downstream-required output.
18. Upstream successful `NO_OP` where downstream edge permits no-op.
19. Upstream `NO_OP` but downstream requires an output not produced.
20. Optional upstream fails but downstream has no dependency on its output.
21. Optional upstream fails but downstream explicitly requires its output.
22. Required upstream terminal failure blocks dependent stage.
23. Downstream stage intentionally consumes upstream terminal-failure evidence under explicit edge contract.
24. Fan-in over 10 event children all successful.
25. Fan-in child membership revision changes after 8 of 10 old children completed.
26. Fan-in empty set with explicit empty-set success behavior.
27. Fan-in empty set where aggregate contract forbids vacuous success.
28. Old artifact from superseded plan has same logical output name as current artifact.
29. Old snapshot output from prior schedule slot is accidentally presented to current slot.
30. Two simultaneous trigger causes request reevaluation of same stage.
31. Two evaluator workers race and both compute equivalent READY results.
32. Stage is already `SUCCEEDED` when new trigger requests reevaluation.
33. Stage is terminal failed and ordinary trigger arrives; no implicit replay.
34. Historical replay/reprocess stage uses separate explicit lineage and does not reuse production eligibility blindly.
35. Readiness adapter call times out technically.
36. Readiness adapter returns malformed/incompatible schema.
37. Cached readiness is valid and exact-authority compatible after adapter is temporarily unavailable.
38. Cached readiness is expired when adapter is unavailable.
39. Required adapter readiness capability disappears/incompatible descriptor revision.
40. MLB opaque readiness reason changes from waiting to ready; generic TDLA never parses probable-pitcher/lineup meaning.
41. NFL/NCAAF opaque readiness behaves the same for late inactive/weather context.
42. PIT-bound input metadata shows availability after prediction cutoff -> dependency/input contract unsatisfied.
43. Input freshness boundary expires while evaluation is in progress.
44. Eligibility computed READY; current schedule resolution changes before A-10 dispatch handoff.
45. Eligibility computed READY; upstream artifact is superseded/retracted before dispatch.
46. Shadow path ready for computation but customer-visible stage is disabled/not applicable.
47. Supervised compute ready but customer-visible side effect remains approval-blocked.
48. Production path has all A-9 gates ready but A-11 later detects existing logical run; no duplicate dispatch.
49. Postgame settlement stage time/dependencies ready but sport settlement readiness still waiting.
50. No-games day has no event materializations and no fake readiness checks.
51. Eligibility evaluation crash before durable result persistence.
52. Crash after durable result persistence but before reevaluation request marked handled.
53. Same evaluation semantic inputs serialize differently; canonical digest remains deterministic.
54. Superseded old eligibility evidence is presented to current dispatcher; fail closed.
55. Technical readiness failure is not mislabeled as sport `BLOCKED`.
56. Multiple generic blocking reasons exist simultaneously; deterministic reason set/order.
57. Dependency output becomes available, generating reevaluation, but schedule window has since closed.
58. Readiness becomes READY before time due; later TIME_DUE reuses only still-valid readiness evidence.
59. Time due before readiness; readiness later becomes READY under same authority and stage proceeds without duplicate materialization.
60. Plan/scope/schedule/readiness all unchanged but duplicate reevaluation cause arrives; no duplicate logical sport work.

---

# Expected A-9 outputs

Create at minimum:

- `docs/architecture/A09_DEPENDENCY_READINESS_ENGINE_V1.md`;
- A-9 V1.1 addendum if review exposes ambiguities;
- A-9 architecture conformance/certification review with stress matrix;
- ADR if eligibility-grant/current-authority/TOCTOU semantics introduce a durable tradeoff;
- updated ADR index;
- updated architecture index;
- updated `ARCHITECTURE_CERTIFICATION_LOG.md`;
- detailed `CHANGE_JOURNAL.md` entry;
- updated root `README.md`;
- updated `CURRENT_RESUME_POINT.md` pointing to A-10.

## Do not do yet

Until A-9 is certified:

- do not implement final eligibility/readiness Pydantic models as frozen authority;
- do not add production Prefect dependency/readiness flows;
- do not design PostgreSQL eligibility/dependency tables around guessed fields;
- do not wire real Daily-MLB/NFL/NCAAF readiness into production automation;
- do not hardcode sport readiness reason codes in generic TDLA;
- do not treat `READY` as a persistent mutable boolean;
- do not let stale readiness/schedule/dependency evidence authorize dispatch;
- do not implement A-10 worker backend or A-11 final idempotency ahead of their architecture sections;
- do not enable production publication.

## Required reading for next session

1. `README.md`
2. `AGENTS.md`
3. this file
4. `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`
5. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_V1.md`
6. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md`
7. `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`
8. `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_ADDENDUM_V1_1.md`
9. `docs/architecture/A07_TRIGGER_ARCHITECTURE_V1.md`
10. `docs/architecture/A07_TRIGGER_ARCHITECTURE_ADDENDUM_V1_1.md`
11. `docs/architecture/A08_EVENT_RELATIVE_SCHEDULING_ENGINE_V1.md`
12. `docs/architecture/A08_EVENT_RELATIVE_SCHEDULING_ENGINE_ADDENDUM_V1_1.md`
13. `docs/implementation/A08_ARCHITECTURE_CONFORMANCE_REVIEW_20260904.md`
14. `docs/adr/ADR-0004_DURABLE_TRIGGER_EVIDENCE_AND_REEVALUATION_ONLY_AUTHORITY.md`
15. `docs/adr/ADR-0005_STABLE_SCHEDULE_SLOTS_AND_RESOLVED_TIME_AUTHORITY.md`
16. current A-5/A-6 sport readiness/dependency contracts.

The next architecture checkpoint is **A-9 Dependency / Readiness Engine**.
