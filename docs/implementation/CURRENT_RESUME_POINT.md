# The Daily Line Automation — Current Resume Point

Last updated: 2026-09-03 (America/Los_Angeles)  
Authority: This file is the single exact continuation point for unfinished TDLA work. It does not override architecture/certification authority; it tells the next session where to resume.

## Current project state

- Repository constitution/documentation-memory policy is authoritative in `AGENTS.md`.
- A-0 through A-4 Foundation V1 + V1.1 nested-lifecycle addendum are **ARCHITECTURE-CERTIFIED**.
- A-5 Sport Automation Adapter V1 + V1.1 certification addendum are **ARCHITECTURE-CERTIFIED**.
- A-5 review evidence: `docs/implementation/A05_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md`.
- ADR-0001 establishes TDLA canonical automation identity and a replaceable orchestration runtime.
- ADR-0002 establishes the Sport Automation Adapter as a transport-neutral protocol boundary.
- No production implementation milestone is certified.
- No TDLA automation is production-authoritative.
- Daily-MLB remains manual-first; later automation must prove equivalence after its final manual production pipeline is certified.

## Certified adapter boundary from A-5

The canonical nested integration is now:

```text
TDLA WorkflowRun / StageRun
  -> TDLA RunAttempt
      -> versioned Sport Automation Adapter protocol
          -> sport child job/service operation
              -> DDC acquisition run(s) where used
                  -> provider evidence/attempts
```

Important locked A-5 rules:

1. TDLA never copies sport readiness/model/settlement logic into generic orchestration code.
2. Adapter integration is transport-neutral; HTTP, CLI/container, queue, RPC, etc. are implementation choices under A-10.
3. Sport scope identity/revision remains sport-owned and opaque to TDLA except for neutral orchestration metadata.
4. Adapter protocol/capability incompatibility fails closed.
5. Capability support does not equal production authorization.
6. Physical retry `attempt_id` is not child deduplication identity.
7. The logical idempotency identity remains stable across retries of the same logical operation.
8. Async production integration must reconcile by child ref and by logical idempotency/equivalent durable handle for the lost-acknowledgement case.
9. Unknown child state is not permission to duplicate dispatch.
10. Shadow mode must disable uncontrolled production-visible side effects.
11. Supervised mode must preserve an explicit production side-effect/operator gate.
12. Sport semantic success does not automatically equal TDLA stage success; declared generic result/artifact requirements must also validate.
13. Terminal result/artifact evidence is immutable/versioned.
14. Settlement/evaluation use the same generic invocation boundary while remaining sport-owned in meaning.

## Daily-MLB compatibility note that must not be forgotten

The current Daily-MLB starter service already demonstrates:

- authenticated asynchronous start;
- service-generated child run ID;
- polling/status lookup;
- persisted run state;
- artifact retrieval.

That makes its shape compatible with A-5 in principle.

However, the currently documented start request does **not** by itself prove caller-supplied idempotent child creation or lookup/reconciliation by TDLA logical idempotency identity when the acknowledgement is lost before TDLA stores the child run ID.

Therefore:

- do not label the current starter collector an A-5 production adapter;
- future M13 Daily-MLB adapter work must target the certified final manual MLB pipeline;
- that adapter/service/wrapper must add or prove A-5 idempotent async dispatch/reconciliation behavior before production certification.

## Exact next step — A-6 Pipeline Plan / Stage Contracts

Design the generic, versioned plan graph that A-5's `resolve_plan` operation returns or validates.

A-6 must make sport workflows declarative enough for TDLA to schedule/validate them without TDLA understanding sport stage meaning.

### A-6 must define at minimum

1. **AutomationPlan identity**
   - plan namespace / ID;
   - schema version;
   - plan version;
   - immutable plan digest;
   - effective/valid interval;
   - sport adapter descriptor/capability binding;
   - environment/execution-mode constraints.

2. **Stage identity**
   - stable stage code/ID;
   - stage version when semantics/output contract changes;
   - scope binding (`event`, `slate`, etc. through A-5 `SportScopeRef`);
   - stage code is opaque sport meaning to generic TDLA.

3. **Graph structure**
   - directed dependencies;
   - acyclic validation or explicitly defined non-DAG mechanism if ever needed;
   - parent/child/fan-out/fan-in representation;
   - slate parent to event children;
   - aggregate stage behavior without parsing sport IDs;
   - deterministic graph identity/digest.

4. **Stage classification**
   - required;
   - optional;
   - conditional / not-applicable;
   - side-effecting vs compute/read-only classification;
   - post-event/settlement/evaluation classification where useful generically.

5. **Timing declaration boundary**
   - absolute or event-relative timing expression;
   - earliest start;
   - target time;
   - deadline/cutoff;
   - validity window;
   - missed-window policy reference;
   - schedule revision binding.

   A-6 defines the declaration schema. A-8 owns actual event-relative recalculation/scheduler algorithm.

6. **Readiness declaration**
   - whether readiness must be evaluated before dispatch;
   - which adapter operation/stage context is used;
   - maximum acceptable readiness age / validity reference;
   - no sport-specific readiness branches in TDLA.

7. **Input contract**
   - required/optional logical inputs;
   - upstream stage/artifact/provenance references;
   - schema/version/digest requirements;
   - freshness/cutoff references where declared;
   - no sport filename guessing.

8. **Output/success contract**
   - required/optional logical outputs;
   - required manifest/result schemas;
   - generic validation requirements;
   - how `NO_OP` / `SUCCEEDED_DEGRADED` can satisfy or fail downstream requirements.

9. **Execution target binding**
   - immutable sport executable/release target reference;
   - adapter capability requirements;
   - configuration reference/digest;
   - resource/worker class hint boundary while deferring detailed scheduling/resource policy to A-10/A-15.

10. **Side-effect policy**
    - compute-only/internal evidence/external side-effect classification;
    - stage compatibility with shadow/supervised/production modes;
    - publication/customer-visible work cannot be hidden inside an otherwise compute-only stage.

11. **Policy references rather than premature algorithms**
    - retry/timeout/idempotency policy reference -> exact mechanics A-11;
    - failure/degradation policy reference -> A-12;
    - artifact retention policy reference -> A-14;
    - concurrency/resource policy reference -> A-15;
    - alert policy reference -> A-17;
    - operator approval policy reference -> A-19.

12. **Plan revisions and supersession**
    - changed plan/version/digest is new authority, not mutation of completed history;
    - future pending stages can be reevaluated/superseded;
    - completed stages remain associated with the exact plan/stage version they actually used;
    - exact reschedule algorithm remains A-8.

13. **Plan composition / ownership**
    - determine whether a sport adapter returns a complete executable plan, a sport-owned fragment composed with TDLA generic wrapper stages, or both through a formally defined composition rule;
    - composition must have deterministic precedence/digest and must never let TDLA inject sport meaning;
    - publication/operator/system-maintenance stages must have clear ownership.

14. **Validation / fail-closed conditions**
    - duplicate stage identities;
    - dependency cycles;
    - dangling dependencies;
    - incompatible adapter capabilities;
    - invalid scope refs;
    - invalid/naive timestamps;
    - impossible timing windows;
    - missing required output declarations;
    - side-effect classification inconsistent with execution mode;
    - mutable/non-immutable production target;
    - plan digest mismatch.

### A-6 stress cases before certification

1. MLB daily slate with zero games.
2. MLB normal slate with many game child scopes.
3. MLB doubleheader with two distinct event scopes.
4. MLB stage waits for lineup/probable-pitcher readiness, then proceeds without creating a duplicate logical stage.
5. A game has an optional enrichment stage fail while the certified required prediction path remains valid.
6. A required upstream stage fails and downstream prediction/publication does not run.
7. NFL/NCAAF plans with multiple event-relative snapshots (for example earlier context refresh plus late pre-kickoff refresh) without hardcoding football semantics in TDLA.
8. Authoritative kickoff/game time moves after future stages were planned.
9. Slate-level aggregation waits for the correct declared child set without parsing sport IDs.
10. Conditional stage becomes `NOT_APPLICABLE` and dependency semantics remain deterministic.
11. Shadow plan produces comparable artifacts but no production-visible publication stage/effect.
12. Supervised plan permits compute completion but stops at an explicit approval boundary.
13. Production plan permits automatic continuation only when certification/side-effect policy allows it.
14. Post-event settlement/evaluation stages activate only after their declared timing/dependencies.
15. Plan revision arrives while some stages are completed and others are pending; completed evidence remains immutable and pending work is deterministically reevaluated.
16. Invalid plan with a dependency cycle fails before dispatch.
17. Invalid plan with duplicate stage IDs or dangling dependency fails before dispatch.
18. Required adapter capability missing from descriptor fails before dispatch.
19. Stage claims compute-only classification but uses a target that can produce uncontrolled external side effects; fail closed.
20. Same logical plan content serializes deterministically to the same canonical digest under the approved canonicalization rules.

## Expected A-6 outputs

Create at minimum:

- `docs/architecture/A06_PIPELINE_PLAN_STAGE_CONTRACTS_V1.md`;
- A-6 conformance/certification review after stress testing;
- ADR(s) if plan composition/graph authority introduces a durable tradeoff;
- `CHANGE_JOURNAL.md` entry;
- updated `ARCHITECTURE_CERTIFICATION_LOG.md`;
- updated architecture index/root README as needed;
- updated current resume point.

## Do not do yet

Until A-6 is certified:

- do not implement final Pydantic stage/plan models as if the schema is frozen;
- do not build real MLB/NFL/NCAAF adapters;
- do not build production Prefect flows based on guessed stage structures;
- do not create PostgreSQL DDL around guessed plan/stage fields;
- do not hardcode sport stage names/semantics in TDLA;
- do not implement the final trigger/scheduler/retry algorithms ahead of A-7/A-8/A-11;
- do not enable production publishing.

## Required reading for next session

1. `README.md`
2. `AGENTS.md`
3. this file
4. `docs/implementation/ARCHITECTURE_CERTIFICATION_LOG.md`
5. `docs/architecture/A00-A04_AUTOMATION_FOUNDATION_V1.md`
6. `docs/architecture/A00-A04_FOUNDATION_ADDENDUM_V1_1.md`
7. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_V1.md`
8. `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md`
9. `docs/implementation/A05_ARCHITECTURE_CONFORMANCE_REVIEW_20260903.md`
10. `docs/adr/ADR-0001_CONTROL_PLANE_AND_VENDOR_NEUTRAL_IDENTITY.md`
11. `docs/adr/ADR-0002_TRANSPORT_NEUTRAL_SPORT_ADAPTER_PROTOCOL.md`
12. relevant current DDC / Daily-MLB / Daily-NFL governing contracts while designing A-6.
