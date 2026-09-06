# A-9 — Dependency / Readiness Engine V1

Status: **DOCUMENTED — REVIEW PENDING**  
Repository: `OneVillage83/The-Daily-Line-Automation`  
Architecture section: A-9  
Version: 1.0  
Initial documentation date: 2026-09-05

This document defines the generic eligibility engine that determines whether one exact TDLA stage materialization is currently eligible to proceed toward dispatch.

A-9 combines already-certified authority from:

- A-5 Sport Automation Adapter readiness evidence;
- A-6 resolved plan, dependency, input/output, fan-in, applicability, and policy contracts;
- A-7 durable eligibility-reevaluation causes;
- A-8 current schedule/time-window authority;
- A-0 through A-4 environment, mode, immutable identity, and audit rules.

A-9 does **not** execute sport work. It does **not** interpret sport readiness reason codes. It does **not** own worker selection, final logical execution idempotency, recovery policy, or persistence DDL.

---

# A-9.0 — Governing rule

The central A-9 rule is:

> **Eligibility is an immutable, versioned evaluation over exact current authority and evidence. `READY` is never a permanent mutable boolean and never direct execution authority. Any execution-affecting authority/evidence change can invalidate a previously-ready result before dispatch.**

The engine answers:

> **Is this exact StageMaterialization currently eligible to proceed toward dispatch, and if not, which generic gates prevent it?**

The answer must be reconstructable from immutable references rather than process-local booleans.

---

# A-9.1 — Design invariants

1. **Current authority is checked first and again before dispatch handoff.** Superseded plan/scope/schedule/materialization authority fails closed.
2. **Sport meaning remains sport-owned.** A-9 consumes A-5 readiness dispositions and opaque reason/evidence references without MLB/NFL/NCAAF branches.
3. **Dependency satisfaction is contract-driven.** `OPTIONAL`, `NO_OP`, `NOT_APPLICABLE`, and `SUCCEEDED_DEGRADED` have only the meanings declared by A-6 edge/output/policy contracts.
4. **Exact upstream evidence matters.** Matching a logical output name is insufficient; required authority/schema/manifest/digest/provenance must match.
5. **Time due is not readiness.** An A-8 due occurrence only satisfies the time gate if it remains current and the declared window/policy permits proceeding.
6. **Sport `READY` is not TDLA `READY_FOR_DISPATCH`.** Time, dependencies, applicability, mode/policy, current authority, and freshness must also pass.
7. **Eligibility evidence expires or invalidates.** It cannot be reused across incompatible plan/scope/schedule/readiness/output/policy revisions.
8. **Technical error is not domain state.** Adapter timeout/malformed response/capability failure cannot be relabeled as sport `WAITING`, `BLOCKED`, or `READY`.
9. **Evaluation causes and results are separate.** A-7 reevaluation requests cause evaluations but do not determine their result.
10. **Physical evaluation attempts are not logical evaluation identity.** Retries/crash recovery do not create contradictory semantic current state.
11. **No direct readiness-to-execution path exists.** A-9 only produces audited eligibility evidence for A-10/A-11.
12. **Final duplicate execution protection remains A-11.** A-9 may coalesce equivalent evaluations but cannot replace logical StageRun idempotency.

---

# A-9.2 — Canonical eligibility entities

A conforming implementation must preserve the following logical distinctions even if physical storage differs.

## A-9.2.1 EligibilityEvaluation

An immutable semantic evaluation of one exact `StageMaterialization` under a specific authority/evidence set.

Conceptual fields:

```text
EligibilityEvaluation
- eligibility_evaluation_id
- schema_version
- resolved_plan_id/digest
- stage_ref + stage_contract_version
- stage_materialization_ref
- sport_scope_ref + scope_revision when applicable
- schedule_resolution_ref/revision/digest when applicable
- schedule_occurrence_ref when applicable
- environment
- execution_mode
- evaluation_cause_refs[]
- dependency_evaluation_refs[]
- readiness_evaluation_refs[]
- time_eligibility_ref
- current_authority_check_ref/digest
- relevant policy/config bindings/digests
- evaluated_at_utc
- disposition
- deterministic_reason_set[]
- semantic_digest
```

## A-9.2.2 DependencyEvaluation

Immutable evidence describing whether one declared A-6 dependency/input/barrier contract is satisfied under exact current upstream authority.

## A-9.2.3 ReadinessEvaluationRef

A binding to exact A-5 readiness result identity/digest, freshness boundaries, scope/stage context, and adapter descriptor/release identity.

## A-9.2.4 TimeEligibilityRef

Evidence that the current A-8 schedule resolution/window permits this stage to proceed toward dispatch at the evaluated instant.

## A-9.2.5 CurrentAuthorityCheck

An immutable snapshot/check result showing which plan/scope/schedule/materialization/mode/policy authority was current at evaluation time.

## A-9.2.6 DispatchEligibilityGrant

A short-lived, non-transferable handoff proving that an A-9 evaluation passed under exact authority. It is **not** a bearer permission to execute blindly; A-10/A-11 must verify that the referenced authority is still current before dispatch.

The exact semantics are defined in A-9.16 and the A-9 certification addendum/ADR if accepted.

---

# A-9.3 — Eligibility evaluation request

An evaluation request conceptually carries:

```text
EligibilityEvaluationRequest
- logical reevaluation request id from A-7
- target StageMaterialization
- expected ResolvedAutomationPlan digest
- current sport scope/scope revision reference
- expected current schedule authority when time-bound
- environment/mode
- evaluation policy/config refs
- correlation/trace context
- requested_at_utc
```

The request is not allowed to override the resolved plan. If the request references stale authority, the result is a stale/not-current disposition rather than mutation to make the request current.

Multiple A-7 causes may be associated with one semantic current evaluation where their target authority is identical and coalescing is safe.

---

# A-9.4 — Deterministic gate order

V1 uses a normative correctness-first evaluation order:

1. **Target existence and terminal-state check** — confirm the stage materialization still exists and is not already completed/terminal in a way that forbids ordinary reevaluation.
2. **Current-authority/applicability check** — resolved plan, stage, sport scope/revision, schedule resolution, environment, mode, relevant immutable policy/config bindings.
3. **Time/window eligibility** — evaluate current A-8 resolution and missed/grace/currentness semantics.
4. **Static/local dependency evaluation** — graph edges, upstream terminal states, exact manifests/outputs, fan-in membership, input freshness metadata already available.
5. **Readiness cache validity check** — determine whether exact-authority readiness evidence remains valid.
6. **Refresh A-5 readiness if required** — only when declared by the plan and no valid compatible result exists.
7. **Composite readiness evaluation** — combine multiple declared generic readiness predicates using explicit versioned composition semantics.
8. **Final current-authority recheck** — detect authority/evidence change during evaluation.
9. **Produce immutable EligibilityEvaluation** — complete deterministic reasons and digest.
10. **Issue DispatchEligibilityGrant only if ready** — version-bound and short-lived; never direct dispatch.

This order avoids unnecessary sport-service calls when static gates already fail while preserving correctness.

An implementation may parallelize independent evidence collection, but final semantic evaluation must be equivalent to this deterministic order and canonical reason computation.

---

# A-9.5 — Current-authority gate

Before any `READY_FOR_DISPATCH` result can exist, A-9 must confirm the target remains current under the certified authority graph.

At minimum validate as applicable:

- `ResolvedAutomationPlan` ID/version/digest;
- plan effective/valid interval;
- stage definition/ref/version;
- exact `StageMaterialization` identity;
- A-5 `SportScopeRef` and scope revision;
- A-6 `ScopeSetBinding` membership revision/digest for fan-out/fan-in;
- A-8 `ScheduleResolution` revision/digest and currentness;
- stage applicability/not-applicable resolution;
- environment;
- execution mode;
- immutable execution-affecting eligibility/failure/degradation policy bindings;
- non-secret effective config digest where eligibility semantics depend on it.

If any execution-semantic authority has been superseded, the evaluation cannot become ready merely because old readiness/dependency evidence was valid.

Possible generic result: `NOT_CURRENT` with structured stale-authority reasons.

Completed historical evidence remains immutable and is never rewritten to the new authority.

---

# A-9.6 — Time eligibility

A-9 consumes A-8 scheduling authority rather than trusting the existence of a `TIME_DUE` event alone.

For time-bound stages it validates:

- the schedule resolution is the current allowed resolution for this materialization/slot;
- the evaluation instant is not before `earliest_eligible_at`/not-before boundary;
- target/due semantics have been reached when required;
- deadline/validity end has not been exceeded unless the certified missed-window policy explicitly routes to reevaluation;
- grace is still valid when a grace-based reevaluation path is used;
- the occurrence is not superseded/cancelled/not applicable;
- current plan/scope/schedule authority matches the due occurrence.

A stale old `TIME_DUE` trigger can remain historical evidence while the time gate returns `NOT_CURRENT` or `MISSED_TIME_WINDOW`.

No time result itself starts execution.

---

# A-9.7 — Dependency edge evaluation

A-9 implements only generic dependency semantics declared by A-6.

Dependency predicates may include conceptually:

- upstream stage reached declared success-compatible terminal state;
- upstream stage produced required logical output;
- output manifest/schema/digest/provenance satisfies the declared contract;
- declared terminal-failure evidence exists when intentionally consumed;
- explicit `NO_OP` accepted by the edge contract;
- `NOT_APPLICABLE` accepted by declared edge/empty-set semantics;
- degraded success accepted for the exact required output under the bound policy;
- exact fan-in barrier membership has reached declared satisfying dispositions.

A stage marked `OPTIONAL` is **not automatically ignorable**. If a downstream required input depends on it, that input remains unsatisfied unless the contract explicitly provides another valid path.

---

# A-9.8 — Exact upstream/output binding

A downstream dependency must bind exact evidence, not a convenient nearby artifact.

A dependency evaluation records or references at minimum as applicable:

```text
DependencyEvidence
- upstream stage materialization ref
- upstream StageRun logical identity
- upstream terminal result identity/status
- upstream plan digest
- upstream scope/schedule/materialization revision
- logical output port/name
- artifact/output manifest ref
- manifest schema/version
- artifact/output digest(s)
- provenance/cutoff/freshness metadata required by contract
- policy binding used for degraded/no-op acceptance
```

Fail closed if an otherwise similarly named artifact comes from:

- a superseded plan;
- a different sport scope revision;
- a different schedule slot/materialization;
- a replay/reprocess lineage not explicitly selected;
- an incompatible schema;
- a mismatching digest;
- a source whose availability/freshness violates the declared contract.

TDLA never guesses filenames.

---

# A-9.9 — Fan-in and barrier semantics

Fan-in evaluation binds the exact A-6 `ScopeSetBinding` membership revision/digest and the exact child materialization set resolved from it.

For each member, the barrier contract must define whether the following count as satisfying, unsatisfying, or policy-routed:

- `SUCCEEDED`;
- `SUCCEEDED_DEGRADED`;
- successful `NO_OP`;
- `NOT_APPLICABLE`;
- terminal failure;
- cancelled;
- superseded;
- missing/unmaterialized;
- still-running/non-terminal.

V1 has **no implicit vacuous-success rule** for empty membership. Empty-set behavior must be explicit in the resolved plan.

If membership revision changes, the old barrier evaluation does not silently absorb the new set. New current authority requires reevaluation against the new exact membership digest.

TDLA never infers slate membership from dates, team names, or provider event IDs.

---

# A-9.10 — A-5 readiness integration

When a stage declares readiness is required, A-9 consumes A-5 readiness evidence with one of:

- `READY`;
- `WAITING`;
- `BLOCKED`;
- `NOT_APPLICABLE`.

A-9 maps these only to generic eligibility behavior.

Examples:

```text
A-5 READY
  -> readiness gate satisfied if result is current/fresh/compatible

A-5 WAITING
  -> WAITING_READINESS

A-5 BLOCKED
  -> BLOCKED_READINESS

A-5 NOT_APPLICABLE
  -> NOT_APPLICABLE / terminal-no-action according to plan contract
```

The sport reason code remains opaque for diagnostics, policy references explicitly declared by the sport plan, and audit.

Generic TDLA must never contain logic such as:

```text
if reason == MLB_PROBABLE_PITCHER_CHANGED: ...
if reason == NFL_INACTIVES_FINAL: ...
```

---

# A-9.11 — Readiness freshness and caching

A readiness result is reusable only when **all** relevant compatibility and freshness requirements remain valid.

At minimum validate:

- exact stage/scope/revision;
- readiness contract/schema version;
- adapter descriptor/implementation/release compatibility;
- `evaluated_at`;
- adapter-supplied `readiness_valid_until` where present;
- A-6 maximum acceptable readiness age where present;
- evidence/provenance revision/digest requirements;
- current plan/schedule/scope authority;
- any required input freshness boundary.

The effective validity boundary is the strictest applicable bound. TDLA cannot extend a sport readiness result beyond the sport-provided validity or the plan's stricter maximum age.

A cache hit across an incompatible revision is forbidden.

Expired `READY` evidence is not permission to dispatch.

---

# A-9.12 — Multiple readiness predicates

If a stage requires more than one readiness dimension, composition must be explicit and versioned.

V1 supports generic declared composition such as:

- `ALL_REQUIRED` — every required predicate must be current and `READY`;
- required plus optional predicates where optional absence does not satisfy a required dependency;
- named readiness predicates/ports supplied by the sport adapter or platform contract.

No implicit boolean precedence exists.

If the composition contract references a missing predicate/capability or has incompatible schemas, fail closed as technical/contract error rather than guessing readiness.

A-9 does not learn the domain meaning of each predicate name.

---

# A-9.13 — Input freshness and PIT contract enforcement

A-9 may enforce generic declared temporal/provenance constraints such as:

- evidence defensibly available at/before a cutoff;
- maximum age at evaluation/dispatch;
- source observation/availability timestamp requirements;
- artifact creation/cutoff metadata;
- exact upstream snapshot/slot binding.

Sport repositories remain responsible for defining the sport-specific PIT meaning and producing the necessary provenance metadata.

If a pregame input is declared to require availability at or before a prediction cutoff and its evidence shows availability after that cutoff, the dependency is unsatisfied.

A-9 must not “helpfully” use newer information to satisfy a historical/PIT-bound contract.

---

# A-9.14 — Eligibility dispositions and deterministic reasons

V1 defines the following conceptual disposition families:

- `NOT_CURRENT`;
- `NOT_APPLICABLE`;
- `WAITING_TIME`;
- `MISSED_TIME_WINDOW`;
- `WAITING_DEPENDENCY`;
- `BLOCKED_DEPENDENCY`;
- `WAITING_READINESS`;
- `BLOCKED_READINESS`;
- `BLOCKED_POLICY`;
- `READY_FOR_DISPATCH`;
- `TERMINAL_NO_ACTION`;
- `EVALUATION_ERROR_RETRYABLE`;
- `EVALUATION_ERROR_TERMINAL`.

Exact implementation enums may refine names but may not collapse materially different meanings.

## Complete deterministic reason set

A-9 should report the complete set of safely-computable generic blocking/satisfaction reasons rather than only whichever branch happened to execute first.

Reasons are canonicalized in deterministic order by stable reason code + affected authority reference.

Examples of generic reasons:

- `PLAN_SUPERSEDED`;
- `SCHEDULE_RESOLUTION_SUPERSEDED`;
- `BEFORE_EARLIEST_ELIGIBLE_TIME`;
- `DEADLINE_EXPIRED`;
- `REQUIRED_UPSTREAM_NONTERMINAL`;
- `REQUIRED_OUTPUT_MISSING`;
- `OUTPUT_SCHEMA_MISMATCH`;
- `OUTPUT_DIGEST_MISMATCH`;
- `READINESS_WAITING`;
- `READINESS_BLOCKED`;
- `READINESS_EXPIRED`;
- `READINESS_TECHNICAL_ERROR`;
- `APPROVAL_REQUIRED` where the generic policy contract exposes that gate.

Sport reason codes may be nested diagnostic evidence but are not TDLA branching enums.

---

# A-9.15 — Evaluation identity and semantic digest

Two `EligibilityEvaluation` records are semantically equivalent only when all execution-affecting evaluation inputs are equivalent under the versioned canonicalization schema.

The semantic digest includes at least:

- resolved plan digest;
- stage materialization identity/version;
- scope/scope revision;
- schedule/time authority reference/digest;
- dependency evaluation identities/digests;
- readiness result identities/digests/freshness bounds;
- relevant policy/config digests;
- environment/mode;
- disposition;
- deterministic reason set;
- schema version.

Causal trigger IDs may be retained as audit lineage without forcing a distinct semantic eligibility digest when two causes legitimately evaluate the exact same authority/evidence state. The implementation schema must explicitly classify audit-only vs semantic fields.

Presentation text does not alter semantic identity unless the schema declares it semantic.

---

# A-9.16 — DispatchEligibilityGrant

A-9 V1 uses an explicit `DispatchEligibilityGrant` as the handoff to A-10/A-11 when an evaluation is `READY_FOR_DISPATCH`.

Conceptual fields:

```text
DispatchEligibilityGrant
- grant_id
- schema_version
- eligibility_evaluation_id/digest
- resolved_plan_digest
- stage_materialization_ref
- scope/scope_revision
- schedule_resolution_ref/digest when applicable
- dependency_authority_digest
- readiness_authority_digest
- relevant policy/config digests
- environment
- execution_mode
- issued_at_utc
- expires_at_utc OR explicit revalidation-before-dispatch marker
- grant_digest
```

The grant has these semantics:

1. It is immutable evidence that A-9 gates passed at issuance.
2. It is bound to one exact stage materialization and authority set.
3. It is not transferable to another plan/scope/schedule/materialization/environment/mode.
4. It is not a bearer capability that can bypass current-state checks.
5. A-10/A-11 must verify the grant is unexpired and that all current-authority witnesses still match before dispatch.
6. If authority changed, the grant is stale and fails closed; a new A-9 evaluation is required.
7. A grant cannot authorize a replay/reprocess unless it was issued for that explicit lineage.
8. A grant cannot authorize a customer-visible/destructive stage whose independent approval/certification/resource/idempotency gates are unsatisfied.

The grant solves handoff/audit identity; it does not pretend distributed state cannot change after evaluation.

---

# A-9.17 — TOCTOU final revalidation

A-9 explicitly addresses time-of-check/time-of-use races.

Example:

```text
12:40:00  A-9 evaluates READY
12:40:01  sport schedule revision changes
12:40:02  A-10 receives the old grant
```

The old grant must fail current-authority verification.

Before dispatch, A-10/A-11 must compare at least the grant's current-authority witnesses against authoritative current heads/revisions/digests for:

- resolved plan;
- stage materialization/applicability;
- sport scope revision;
- schedule resolution/time validity;
- dependency/output authority when mutable/supersedable;
- readiness validity/revision;
- relevant policy/config/environment/mode;
- explicit operator approval state where required later by A-19.

Exact transaction/locking implementation is deferred to A-10/A-11/A-13, but fail-closed revalidation is normative.

A long-running dispatch queue may therefore require re-evaluation rather than treating an old grant as permanent permission.

---

# A-9.18 — Invalidation and supersession

A previously-ready evaluation/grant becomes stale when execution-affecting authority changes, including as applicable:

- new resolved plan revision;
- stage materialization superseded/not-applicable;
- sport scope/schedule revision change;
- A-8 schedule resolution superseded/deadline expires;
- required upstream artifact/result superseded/retracted;
- readiness result expires or incompatible newer readiness authority arrives;
- policy/config binding changes through a new resolved plan/authority;
- execution mode/environment authorization changes.

Old evaluations/grants remain immutable audit evidence.

They are not edited to `false`; they are simply no longer current authority.

If the stage already dispatched/executed, A-12/A-14 determine correction/recovery/reprocess behavior.

---

# A-9.19 — Concurrent reevaluations and coalescing

Multiple triggers/workers may evaluate the same current stage simultaneously.

Allowed:

- multiple physical evaluation attempts;
- equivalent immutable evaluation evidence when race-free deduplication is not available;
- causal links from many A-7 reevaluation requests to one semantically equivalent current evaluation.

Required:

- equivalent evaluations canonicalize to the same semantic digest;
- no evaluation attempt directly creates a duplicate StageRun;
- A-11 final logical idempotency remains authoritative;
- coalescing must not cross incompatible plan/scope/schedule/materialization/environment/mode/readiness authority.

A-13 may later enforce unique/current-head constraints for efficiency and recovery.

---

# A-9.20 — Terminal stage behavior

Ordinary reevaluation of a stage already terminal does not create new sport work.

Examples:

- already `SUCCEEDED` -> `TERMINAL_NO_ACTION`/already-terminal evidence;
- terminal failed -> remain terminal unless an explicit recovery transition is authorized by A-12;
- superseded/cancelled -> no ordinary redispatch;
- replay/reprocess/backfill -> separate explicit A-14 lineage and eligibility authority.

A trigger does not convert a completed production stage into a replay.

---

# A-9.21 — Technical error vs domain waiting

A-9 keeps these distinct:

```text
sport readiness = WAITING
sport readiness = BLOCKED
adapter timeout
adapter unavailable
malformed readiness schema
readiness capability missing
cached result expired
cached result valid but source temporarily unavailable
```

A technical failure can yield `EVALUATION_ERROR_RETRYABLE` or `EVALUATION_ERROR_TERMINAL` according to the applicable technical contract/policy.

It cannot be silently mapped to sport `READY`, `WAITING`, or `BLOCKED`.

A valid exact-authority cached readiness result may be used while the adapter is unavailable only if its certified validity/freshness remains intact.

---

# A-9.22 — Execution mode, policy, and approval boundaries

A-9 evaluates the current resolved mode/policy constraints known at this layer.

Examples:

- shadow compute path may become ready if side-effect classification is shadow-safe;
- a customer-visible stage disabled/not-applicable in shadow cannot become ready because sport readiness says `READY`;
- supervised customer-visible stage may remain `BLOCKED_POLICY`/approval-required after sport/time/dependency readiness passes;
- production eligibility requires current production-authorized plan/integration/mode policy;
- A-19 owns the actual operator approval action and identity mechanics.

A-9 cannot promote an integration's certification status.

---

# A-9.23 — Post-event settlement/evaluation

The same engine supports post-event stages.

Generic gates may include:

- current post-event schedule/time condition;
- upstream prediction artifact/evidence;
- sport result input availability;
- A-5 sport settlement/evaluation readiness;
- exact output/dependency contracts;
- publication/evaluation policy constraints.

TDLA does not interpret sport grading/settlement rules.

---

# A-9.24 — Recovery after process loss

Correctness must not depend on a process-local `ready` variable.

After restart, TDLA must be able to reconstruct/re-evaluate from durable authority/evidence:

- pending A-7 reevaluation requests;
- current plan/stage/scope/schedule authority;
- upstream terminal/output evidence;
- readiness evidence/cache validity;
- prior immutable eligibility results/grants;
- whether the stage is already terminal/dispatched under A-11 identity.

If an eligibility result was durably persisted but acknowledgement/reevaluation-request bookkeeping was lost, recovery may reuse semantically equivalent immutable evidence when still current rather than invent contradictory eligibility state.

Exact persistence/outbox/current-head transaction mechanics remain A-13.

---

# A-9.25 — Technology neutrality

Canonical eligibility identity/state must not depend on:

- Prefect task/run state;
- Celery result state;
- Redis lock keys;
- queue acknowledgement IDs;
- process memory;
- a particular SQL row surrogate ID alone;
- worker host identity.

Such values may be runtime cross-references.

The certified semantic authority is the TDLA plan/stage/scope/schedule/dependency/readiness/evaluation/grant contract.

---

# A-9.26 — No direct readiness-to-execution path

The following is prohibited:

```text
sport adapter returns READY
-> execute model
```

The certified path is:

```text
A-7 reevaluation cause
        +
A-8 current time authority
        +
A-6 dependency/output contracts
        +
A-5 readiness evidence where required
        +
current plan/scope/materialization/mode/policy authority
        |
        v
A-9 EligibilityEvaluation
        |
        v
DispatchEligibilityGrant
        |
        v
A-10/A-11 final current-authority + idempotency + dispatch gates
        |
        v
sport adapter invocation
```

A-9 therefore cannot publish, execute, or create a child sport job.

---

# A-9.27 — Deferred architecture boundaries

A-9 intentionally does **not** freeze:

- worker selection, dispatch transport, queueing, leases, capacity -> A-10;
- exact StageRun logical idempotency key, retry/timeouts, lost-dispatch acknowledgement -> A-11;
- failure propagation/recovery/correction/orphan policy -> A-12;
- PostgreSQL DDL, current-head/unique constraints, outbox/transactions -> A-13;
- replay/backfill/reprocess artifact lineage mechanics -> A-14;
- concurrency/resource/provider budgets -> A-15;
- telemetry -> A-16;
- alerts/incidents -> A-17;
- publication contracts -> A-18;
- operator override/approval implementation -> A-19;
- service identity/authentication -> A-20.

These deferrals are deliberate. Later architecture must conform to A-9 eligibility semantics rather than redefine `READY` as a mutable runtime flag.

---

# A-9.28 — Fail-closed validation requirements

Before a production `READY_FOR_DISPATCH` result/grant is valid, fail closed on at least:

- missing/current plan digest mismatch;
- superseded stage materialization;
- wrong sport scope/scope revision;
- stale/superseded schedule resolution;
- invalid/missed time window not permitted by policy;
- dangling/missing upstream dependency evidence;
- wrong upstream plan/scope/slot/lineage;
- missing required output;
- output manifest/schema mismatch;
- output digest/provenance mismatch;
- fan-in membership revision mismatch;
- readiness required but absent;
- readiness expired/stale/incompatible;
- malformed readiness result;
- required readiness capability missing;
- undeclared/malformed composite readiness contract;
- PIT/freshness contract violation;
- incompatible environment/mode;
- required approval/policy gate unsatisfied;
- eligibility/grant semantic digest mismatch;
- naive timestamps in eligibility/freshness boundaries;
- current-authority change detected during final recheck.

---

# A-9.29 — Certification requirements

A-9 may be architecture-certified only after review demonstrates at minimum:

- no sport readiness semantics leaked into generic TDLA;
- correct A-6 dependency/output/no-op/degraded/fan-in behavior;
- exact revision/digest binding prevents stale output reuse;
- readiness freshness/cache rules fail closed;
- technical failures remain distinct from domain waiting/blocked;
- current A-8 schedule authority overrides stale due events;
- deterministic complete reason sets;
- equivalent evaluations canonicalize consistently;
- concurrent reevaluations do not imply duplicate StageRuns;
- TOCTOU between READY and dispatch is closed by version-bound grant + final current-authority verification;
- terminal stages do not implicitly replay;
- shadow/supervised/production policy boundaries remain intact;
- restart recovery does not depend on process-local booleans;
- all 60 handoff stress cases pass at architecture-contract level.

Certification is architecture authority only. It will not certify Pydantic models, database schema, Prefect tasks, readiness service calls, worker dispatch, or production sport automation.