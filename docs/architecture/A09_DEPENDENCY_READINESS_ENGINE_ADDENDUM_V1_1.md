# A-9 Dependency / Readiness Engine — Certification Addendum V1.1

Date: 2026-09-05  
Status: **CERTIFICATION CLARIFICATION — governs A-9 V1 together with the base document**

This addendum records clarifications identified during the independent A-9 conformance review. It does not replace `A09_DEPENDENCY_READINESS_ENGINE_V1.md`; the two documents together form the certified A-9 contract if certification is granted.

## 1. Deterministic reason sets do not require unnecessary external readiness calls

A-9 V1 prefers a complete deterministic generic reason set, but “complete” means complete for the gates that can be evaluated safely and are semantically reachable under the normative evaluation order.

If a prior authoritative gate already establishes that the stage cannot proceed and the plan does not require readiness evidence for diagnostic purposes, A-9 must not call a sport readiness service merely to discover extra reasons.

Examples:

```text
stage materialization superseded
-> report NOT_CURRENT + current-authority reasons
-> do not call sport readiness
```

```text
before earliest eligible time
-> report WAITING_TIME + known local dependency reasons if deterministically available
-> readiness call may be skipped according to the certified evaluation order
```

Within the set of gates actually evaluated, reasons are canonicalized deterministically.

This avoids turning “complete reasons” into unnecessary provider/service load or nondeterministic external calls.

## 2. DispatchEligibilityGrant is evidence, not a bearer capability

A `DispatchEligibilityGrant` is immutable handoff evidence only.

Possessing a syntactically valid grant does **not** authorize dispatch unless A-10/A-11 also confirm that all current-authority witnesses referenced by the grant remain current.

A grant is bound to exactly one:

- resolved-plan digest;
- stage materialization;
- sport scope/scope revision;
- schedule resolution when applicable;
- dependency/output authority set;
- readiness authority set;
- environment/mode;
- relevant execution-affecting policy/config authority.

It cannot be transferred to another stage, scope, revision, replay, reprocess, environment, or mode.

Grant validity must be bounded by the earliest applicable execution-semantic expiry, including:

- readiness validity/max-age;
- schedule/deadline/validity window;
- policy-defined maximum handoff age;
- any stricter execution-authority boundary.

If no safe nonzero validity window can be established, the grant requires immediate inline final revalidation rather than receiving an arbitrary TTL.

## 3. Readiness cache validity is the intersection of all authority/freshness bounds

A cached A-5 readiness result is reusable only while all applicable boundaries remain valid simultaneously.

Conceptually:

```text
cache_valid_until = min(
    sport_readiness_valid_until,
    plan_max_readiness_age_boundary,
    input/evidence freshness boundary,
    schedule/window validity boundary when relevant,
    policy-defined cache bound
)
```

In addition to clock expiry, **any incompatible authority revision invalidates the cache immediately**, including plan, stage, scope, schedule, readiness-contract, adapter-compatibility, or required evidence revision changes.

A timestamp that has not yet expired cannot make a cache entry valid across an authority revision.

TDLA may shorten validity; it may never extend validity beyond the strictest source/plan boundary.

## 4. Upstream output supersession/retraction invalidates dependent eligibility

A dependency can be satisfied only by output evidence that remains current for the resolved downstream authority.

If an upstream output/result is later superseded, retracted, invalidated, or replaced under a new authoritative lineage before downstream dispatch:

- the old dependency evaluation remains immutable historical evidence;
- any A-9 eligibility/grant depending on it becomes stale;
- downstream dispatch must fail current-authority revalidation;
- a new eligibility evaluation is required against current output authority.

A matching artifact digest alone does not override an explicit supersession/retraction state.

If downstream work already executed before the upstream correction, A-12/A-14 own recovery/reprocess behavior.

## 5. Composite readiness has explicit required/optional semantics

For V1 composite readiness:

- every predicate declared `required` under an `ALL_REQUIRED` composition must be current, valid, technically successful, and `READY` for the composite to satisfy readiness;
- `WAITING` on any required predicate yields waiting unless a stronger blocking/error disposition is present;
- `BLOCKED` on any required predicate yields blocked readiness;
- `NOT_APPLICABLE` follows the explicitly declared composition/applicability rule and cannot be guessed;
- a technical error on a required predicate is an evaluation error, not sport `BLOCKED`;
- an optional predicate cannot compensate for a required predicate that is missing, stale, waiting, blocked, or technically failed;
- optional predicate failure/degradation behavior must be explicitly declared by the versioned readiness composition contract.

No implicit boolean precedence or sport-specific reason interpretation is permitted.

## 6. Semantic evaluation identity is separate from causal trigger lineage

Two A-7 reevaluation requests may legitimately evaluate the exact same current authority/evidence state.

A-9 therefore distinguishes:

- **eligibility evaluation record identity** — unique immutable audit record;
- **eligibility semantic digest** — deterministic digest over execution-semantic authority/evidence/result;
- **causal reevaluation references** — audit lineage explaining why evaluation happened.

Causal trigger/reevaluation IDs are not automatically part of the semantic digest when the schema classifies them as audit lineage.

Therefore:

```text
cause A -> evaluation semantic digest X
cause B -> evaluation semantic digest X
```

is valid when plan/stage/scope/schedule/dependency/readiness/policy evidence and disposition are identical.

This supports safe coalescing/recovery without erasing either cause.

## Certification relationship

These six clarifications are normative for A-9 certification and future contract tests.

In particular, A-9 certification requires the DispatchEligibilityGrant/current-authority handoff to be implemented as **version-bound evidence plus final revalidation**, never as a reusable `ready=true` bearer token.