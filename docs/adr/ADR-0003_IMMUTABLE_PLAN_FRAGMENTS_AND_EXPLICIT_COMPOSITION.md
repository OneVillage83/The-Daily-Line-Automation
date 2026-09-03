# ADR-0003 — Immutable Plan Fragments, Explicit Composition, and Resolved Plan Authority

Date: 2026-09-03  
Status: **ACCEPTED**

## Context

A-5 permits a sport adapter to return or validate a sport-owned automation plan/plan fragment. TDLA also needs generic platform-owned operational stages such as approval, distribution, archival, or system-level evidence handling.

A naive design would make one side authoritative over the whole graph, allow TDLA to edit sport stages in place, or merge fragments using name matching/precedence. That would create several long-term risks:

- TDLA could accidentally absorb sport-domain meaning;
- a platform update could silently change a sport workflow;
- stage-name collisions could overwrite behavior;
- publication/approval wrappers could become coupled to sport-specific filenames or stage names;
- plan identity could become ambiguous because the authored sport plan and actually executed graph differ without a separate digest;
- reproducing a historical run would require reconstructing hidden merge behavior.

## Decision

TDLA adopts a four-layer plan identity model:

1. immutable `PlanFragment` objects contributed by one authority namespace (`SPORT` or `TDLA_PLATFORM`);
2. an immutable `PlanAssembly` that names exact fragment versions/digests and contains explicit cross-fragment port bindings;
3. an immutable `ResolvedAutomationPlan` produced after composition, scope binding, capability checks, policy binding, and immutable target resolution;
4. deterministic `StageMaterialization` identities produced from the resolved plan for concrete scope/schedule contexts.

### No silent precedence

Composition has no `TDLA wins`, `sport wins`, or `last writer wins` rule.

Conflicts fail closed.

This includes duplicate stage references, incompatible imported/exported port schemas, contradictory environment/mode constraints, ambiguous bindings, and contradictory target/policy constraints.

### Explicit cross-fragment ports

TDLA platform stages may consume sport outputs only through explicit typed port bindings recorded in `PlanAssembly`.

TDLA may not infer a connection from:

- a sport stage name;
- a filename;
- a directory path;
- a database table name;
- a sport-specific reason code;
- an assumed ordering convention.

### Sport-stage immutability

TDLA platform fragments may wrap or depend on sport outputs through declared ports but may not mutate a sport-owned stage definition in place.

If a sport stage needs different semantics, the sport fragment/version must change through the sport adapter boundary.

### Resolved plan is executable authority

The `ResolvedAutomationPlan`—not an unbound fragment and not a Prefect flow object—is the canonical executable plan authority for TDLA.

Its digest includes the exact contributing fragment digests, assembly bindings, bound scope/schedule revisions, applicable policy references, adapter descriptor identity, and immutable execution-target bindings required by A-6.

## Why this decision

This model keeps ownership explicit while still allowing The Daily Line to build reusable platform capabilities around every sport.

For example:

```text
Daily-MLB sport fragment
    exports typed publication-package port

TDLA publication fragment
    imports typed publication-package port

PlanAssembly
    explicitly binds those ports

ResolvedAutomationPlan
    contains both stages and the exact binding/digests
```

TDLA can distribute a package without understanding baseball report content.

## Alternatives considered

### Alternative 1 — Sport adapter returns the complete final graph

Rejected as the sole model because each sport would need to duplicate generic TDLA operational stages/policies and would become coupled to platform implementation concerns.

A sport may still return a complete sport-owned fragment, but generic platform stages remain composable outside it.

### Alternative 2 — TDLA owns the complete graph and calls sport functions

Rejected because this would move sport workflow meaning into the automation repository and create sport-specific branches.

### Alternative 3 — Merge YAML/JSON by stage name with override precedence

Rejected because it is difficult to audit, creates hidden authority rules, and makes historical plan reconstruction unsafe.

### Alternative 4 — Runtime orchestrator flow definition is the plan authority

Rejected under ADR-0001. Prefect or another runtime is an execution mechanism, not canonical TDLA business identity.

## Consequences

Positive:

- ownership remains explicit;
- sport and TDLA platform logic can evolve independently;
- historical resolved plans are reconstructable;
- cross-fragment dependencies are type-checkable;
- generic publication/approval infrastructure can be reused across sports;
- no accidental precedence rules;
- runtime/orchestrator replacement remains possible.

Costs:

- more contract objects and digests must be maintained;
- plan resolution requires a validation/composition step;
- port schemas must be versioned;
- implementation tests must include canonical composition/digest vectors.

These costs are accepted because ambiguity at the automation boundary is more expensive than explicit composition.

## Compatibility / migration impact

No production TDLA plan implementation exists yet, so there is no runtime migration.

Future sport adapters must either:

- return a certified sport fragment; or
- return a complete fragment that still conforms to A-6 ownership/port rules.

Existing manual pipelines are not required to restructure internally until their automation adapter is implemented; the adapter/wrapper may expose the required fragment contract around the certified manual interface.

## Security / operational impact

Explicit side-effect stages and port bindings make it possible to verify that shadow/supervised plans cannot accidentally connect directly to production publication paths.

Plan resolution failures are fail-closed and auditable.

## Validation required

A-6 certification must prove at architecture level that:

- duplicate stage identities fail;
- incompatible cross-fragment ports fail;
- TDLA platform stages cannot mutate sport stages;
- the same semantic assembly resolves deterministically;
- plan identity includes exact fragment and immutable target bindings;
- execution-mode/side-effect incompatibility fails before dispatch.

Implementation certification must later add contract tests/test vectors.

## Related architecture

- A-0 through A-4 Foundation V1/V1.1
- A-5 Sport Automation Adapter V1/V1.1
- A-6 Pipeline Plan / Stage Contracts V1
- ADR-0001 — canonical TDLA identity / replaceable orchestrator
- ADR-0002 — transport-neutral sport adapter protocol
