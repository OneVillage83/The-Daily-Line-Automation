# A-6 Pipeline Plan / Stage Contracts — Certification Addendum V1.1

Date: 2026-09-03  
Status: **CERTIFICATION CLARIFICATION — governs A-6 V1 together with the base document**

This addendum records clarifications identified during the A-6 architecture conformance review. It does not replace `A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`; the two documents together form the certified A-6 contract when certification is granted.

---

## 1. `ScopeSetBinding` is a neutral binding of sport-owned references, not a new TDLA sport identity object

A-5 defines sport-owned `SportScopeRef` objects and discovery results. A-6 fan-out/fan-in requires an exact, revision-bound child membership set.

To bridge those contracts without making TDLA a sport identity authority, A-6 V1.1 defines a neutral resolved object:

```text
ScopeSetBinding
- binding_id
- source_sport_namespace
- source_discovery/plan revision reference
- source_scope_ref (optional parent/slate ref)
- ordered_or_set_semantics declaration
- exact member SportScopeRef values[]
- member scope revisions[]
- canonical_membership_digest
```

Rules:

1. Membership must originate from the sport adapter/sport-owned plan/discovery contract.
2. TDLA may normalize, sort where the schema declares set semantics, and hash the exact supplied member references for orchestration identity.
3. TDLA may not invent, merge, split, drop, or reinterpret members based on team names, dates, provider IDs, or sport rules.
4. A new sport-supplied membership/revision produces a new `ScopeSetBinding`/membership digest.
5. Fan-out and fan-in bind to the exact `ScopeSetBinding` digest they materialize/aggregate.
6. An empty sport-supplied member list is a valid binding when the stage's empty-set policy allows it.

The binding is orchestration evidence over sport-owned identities; it does not become canonical game/slate identity authority.

---

## 2. Canonical digest participation distinguishes semantic fields from presentation-only metadata

The plan digest must identify execution semantics, not incidental presentation edits.

Therefore every plan/fragment schema field is classified as one of:

- `SEMANTIC_DIGESTED` — participates in canonical semantic normalization and digest;
- `PRESENTATION_ONLY` — safe label/description/help text that does not affect execution and is excluded from semantic digest;
- `AUDIT_METADATA` — creation/documentation metadata retained alongside the object but excluded when it is not part of execution semantics.

Examples:

- stage identity/version, dependencies, scope bindings, timing declarations, required inputs/outputs, execution-mode restrictions, target bindings, side-effect classes, immutable policy bindings -> **semantic/digested**;
- safe display label -> **presentation-only** unless a future schema explicitly makes it semantic;
- documentation author or generated display timestamp -> **audit metadata**, not execution identity.

Rules:

1. Digest participation is defined by the versioned contract schema, not by ad-hoc implementation choices.
2. Unknown fields cannot be silently ignored for hashing unless the compatibility schema explicitly classifies them.
3. Two objects with identical execution semantics but different presentation-only labels must have the same semantic digest.
4. A semantic field change must change the corresponding digest.

M1 must provide canonicalization test vectors proving these rules.

---

## 3. Repeated snapshot identity uses an explicit logical schedule slot, not the resolved clock timestamp

A plan may intentionally request multiple similar operations relative to one event, for example an early context snapshot and a late pre-event snapshot.

Each repeated declaration/materialization must have an explicit stable logical slot identity:

```text
ScheduleSlotRef
- slot_id
- slot_contract_version
- timing_declaration_ref
```

Rules:

1. `slot_id` distinguishes intended repeated logical operations.
2. The resolved wall-clock timestamp is **not** itself the semantic slot identity.
3. Physical retries of one slot retain the same logical stage materialization/idempotency identity.
4. An event-time/scope revision may cause A-8 to recalculate/supersede pending work, but TDLA does not create a second logical snapshot solely because the clock target moved.
5. If the sport intends two distinct snapshots, the plan must declare two distinct slot identities (or an explicitly versioned deterministic slot template), even if their resolved times happen to coincide.

The exact A-8 reschedule/supersession algorithm remains deferred, but A-6 fixes the identity boundary.

---

## 4. Execution-affecting policy references must resolve to immutable version/digest bindings in the executable plan

A base fragment may reference a policy selector/name for reuse, but a production `ResolvedAutomationPlan` cannot depend on a mutable policy alias whose meaning may change after plan resolution.

For every execution-affecting policy used by the plan, resolution must retain an immutable binding such as:

```text
ResolvedPolicyBinding
- policy_namespace
- policy_id
- policy_version
- policy_digest
- policy_family
```

Rules:

1. The resolved plan digest includes execution-affecting immutable policy bindings.
2. Changing a retry/failure/scheduling/approval/publication/resource/security policy version that can affect execution produces a different resolved plan identity.
3. Presentation-only policy documentation metadata does not affect the semantic digest unless the policy schema marks it semantic.
4. A mutable alias such as `current-production-policy` may be used only during resolution; it must resolve to an immutable version/digest before production dispatch.
5. Missing or unresolvable required policy bindings fail closed.

This rule complements A-6's immutable execution-target requirement and prevents historical behavior from depending on whatever a mutable policy name means later.

---

## Certification relationship

These four clarifications are normative for A-6 certification and must be represented in future M1 plan/stage contract tests and canonical digest test vectors.
