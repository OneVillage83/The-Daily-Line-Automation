# A-5 — Sport Automation Adapter Contract V1

Status: **DOCUMENTED — REVIEW PENDING**  
Repository: `OneVillage83/The-Daily-Line-Automation`  
Architecture section: A-5  
Version: 1.0  
Initial documentation date: 2026-09-03

This document defines the sport-neutral contract by which Daily-MLB, Daily-NFL, Daily-NCAAF, and future Daily-* systems expose automation capabilities to The-Daily-Line-Automation (TDLA).

A-5 is a boundary contract. It defines what TDLA may ask a sport system to declare, evaluate, execute, reconcile, cancel, and return. It does **not** define sport logic and it does not freeze the complete pipeline/stage graph schema; the latter is owned by A-6.

---

# A-5.0 — Governing intent

The central rule is:

> **A Sport Automation Adapter is a versioned protocol boundary between TDLA and a sport-owned system. It is not a place for TDLA to import, copy, or reinterpret sport-domain logic.**

The adapter allows TDLA to coordinate a sport pipeline while the sport repository remains authoritative for:

- canonical sport identity;
- schedule interpretation;
- sport-specific readiness;
- lineup/injury/player/team meaning;
- feature/state construction;
- model and simulation behavior;
- prediction and Recommendation Gate semantics;
- sport-specific degradation/failure meaning;
- settlement/evaluation meaning;
- sport report/content generation.

TDLA remains authoritative for the outer automation lifecycle described by A-0 through A-4.

---

# A-5.1 — Design invariants

The following are mandatory for every certified adapter implementation.

1. **Sport logic remains sport-owned.** TDLA may record sport reason codes and result metadata but must not reproduce their calculation.
2. **The contract is transport-neutral.** HTTP, container/CLI, queue, RPC, or another execution mechanism may implement the boundary. Transport selection is not canonical adapter identity and is finalized under A-10.
3. **The contract is versioned and negotiated.** TDLA must fail closed when a required protocol version/capability is incompatible.
4. **Sport references remain sport-owned.** TDLA stores opaque/versioned references and neutral scheduling metadata without becoming canonical sport identity authority.
5. **Invocation is idempotency-aware.** A production-capable asynchronous adapter must provide a safe way to determine whether a previously requested child operation already exists after outer-process loss.
6. **Child execution identity remains distinct.** TDLA run/attempt IDs do not replace sport child-job IDs or DDC acquisition/provider IDs.
7. **Readiness is declarative.** The sport returns generic readiness disposition plus sport-defined reason/evidence; TDLA does not infer MLB/NFL/NCAAF meaning.
8. **Terminal success is contract-based.** A child process exit code or HTTP 200 is not enough; the adapter returns a versioned semantic result and required artifact/provenance references.
9. **Shadow mode is side-effect safe.** An adapter cannot be certified for `AUTOMATION_SHADOW` if the invoked path can produce uncontrolled production-visible side effects.
10. **Unknown child state is not permission to duplicate work.** Recovery/reconciliation precedes redispatch.
11. **Terminal evidence is immutable.** Later corrections are new versioned/lineaged operations, not silent mutation of the original TDLA evidence.
12. **Secrets do not cross the logical contract as data.** Authentication is provided by the execution/transport security mechanism; adapter results and diagnostics must be safe to persist.

---

# A-5.2 — Adapter identity and compatibility

Every adapter exposes a capability/compatibility descriptor before TDLA binds a plan to it.

## A-5.2.1 Required identity fields

Conceptually:

```text
AdapterDescriptor
- protocol_name                 = "tdla-sport-adapter"
- protocol_version              = semantic contract version
- adapter_namespace             = stable sport implementation namespace
- adapter_implementation_version
- sport_family                  = MLB / NFL / NCAAF / ... as declared metadata
- build/release identity        = immutable release/commit/image metadata when applicable
- capability_profile
- descriptor_generated_at
- descriptor_digest
```

`adapter_namespace` identifies the implementation family, not an individual service process/host.

## A-5.2.2 Version rules

The V1 policy is:

- protocol major-version mismatch is incompatible unless an explicit compatibility bridge exists;
- minor-version evolution is additive by default;
- optional fields/capabilities may be added without redefining old semantics;
- existing field meaning must never be silently changed in place;
- a required capability missing from the negotiated descriptor causes planning/dispatch to fail closed;
- the negotiated descriptor/version/digest used by a production run is retained in execution provenance.

Exact serialization/versioning mechanics will be frozen in implementation contracts, but these semantics are mandatory.

## A-5.2.3 Capability profile

The adapter declares capabilities rather than forcing TDLA to infer them from sport name.

Capabilities include at least whether the adapter supports:

- scope discovery;
- plan/plan-fragment resolution;
- readiness evaluation;
- synchronous invocation;
- asynchronous invocation;
- reconciliation by child reference;
- reconciliation/lookup by idempotency key or equivalent deduplication identity;
- cancellation;
- immutable result retrieval;
- artifact-manifest references;
- post-event settlement operation;
- post-event evaluation operation;
- declared shadow-safe execution;
- declared supervised execution;
- declared production execution.

A capability declaration is evidence of interface support, not proof of production certification. The certification log remains authority for whether a mode is actually authorized.

---

# A-5.3 — Transport neutrality and logical operations

A-5 defines logical adapter operations, not Python method names or HTTP routes.

A conforming implementation must provide equivalents of the following operations where its negotiated capabilities require them:

```text
describe_adapter
  -> AdapterDescriptor

discover_scopes
  -> ScopeDiscoveryResult

resolve_plan
  -> SportPlanFragment

check_readiness
  -> ReadinessResult

invoke
  -> InvocationAcknowledgement OR terminal SportExecutionResult

reconcile
  -> ChildExecutionSnapshot

cancel
  -> CancellationAcknowledgement

fetch_result
  -> SportExecutionResult
```

A local/container adapter may implement these through a wrapper executable. A service adapter may implement them through authenticated APIs. A queue-based adapter may use messages. TDLA canonical identity must remain unchanged across these transport choices.

---

# A-5.4 — Common request context

Every material adapter request carries or is bound to a common outer context sufficient for correlation and safe deduplication.

Minimum conceptual fields:

- `tdla_environment`;
- `tdla_workflow_run_id` where a workflow run exists;
- `tdla_stage_run_id` where a stage exists;
- `tdla_attempt_id` for physical dispatch/execution attempts;
- `tdla_logical_idempotency_key` or a derived stage-operation key;
- `execution_mode`;
- `adapter_protocol_version`;
- `scope_ref` when applicable;
- `plan_id/version/digest` when applicable;
- `requested_at` UTC;
- deadline/cutoff context when applicable;
- trace/correlation context;
- safe caller/service-principal reference where applicable.

The sport system must preserve enough of this context to make child reconciliation/provenance possible.

Raw credentials, provider tokens, API keys, passwords, or private certificates are not common-context fields.

---

# A-5.5 — Sport scope references

## A-5.5.1 Purpose

TDLA must coordinate work for games, slates, dates, historical ranges, and other units without becoming the permanent sport identity database.

A `SportScopeRef` therefore identifies a sport-owned scope through an opaque/versioned reference plus neutral metadata needed for orchestration.

## A-5.5.2 Conceptual contract

```text
SportScopeRef
- sport_namespace
- scope_kind
- opaque_scope_id
- scope_revision / schedule_revision reference when applicable
- effective_start/end when meaningful
- event_start_time when meaningful
- event_timezone when meaningful
- safe display metadata (optional, non-authoritative)
- scope_ref_digest/version
```

Examples of `scope_kind` may include:

- `event`;
- `slate`;
- `sport_day`;
- `league_day`;
- `batch`;
- `historical_range`;
- `settlement_cycle`;
- `evaluation_cycle`.

The list is extensible. TDLA must not branch on sport-specific values such as `doubleheader_game_2` to derive baseball meaning. The sport system must represent separate actionable events/scopes through its own references.

## A-5.5.3 Schedule revisions

If a sport system changes its authoritative interpretation of a scope's timing or composition, it supplies a new schedule/scope revision reference.

TDLA may use that revision to detect that existing planned work needs reevaluation/supersession under A-8, but TDLA does not decide whether two provider event IDs represent the same canonical game.

## A-5.5.4 No-games result

A successful discovery request over a defined coverage window may return an empty scope list.

`0 scopes` is a valid authoritative result when accompanied by:

- requested/covered window;
- sport namespace;
- discovery revision/digest;
- observed/generated timestamp;
- success status.

A no-games day must not be converted into a provider/adapter failure merely because no event exists.

---

# A-5.6 — Scope discovery

Scope discovery is optional as a distinct adapter capability but required somewhere in the sport integration path before TDLA can schedule dynamic real-world slates.

Conceptual request:

```text
DiscoveryRequest
- coverage window
- environment
- requested scope kinds
- execution mode/context
- prior discovery revision (optional)
```

Conceptual result:

```text
ScopeDiscoveryResult
- covered window
- sport namespace
- scope refs[]
- discovery revision/digest
- observed/generated timestamp
- completeness/diagnostic status
- safe diagnostics
```

The sport repository is responsible for mapping upstream schedules into its canonical scope references. TDLA does not query a league/provider and build sport canonical identity itself as a shortcut.

---

# A-5.7 — Planning interface

`resolve_plan` allows a sport system to supply or validate the automation plan/plan fragment applicable to a scope.

A-5 freezes the boundary expectations but defers the exact stage-graph schema to A-6.

At minimum the plan fragment must eventually provide or reference:

- plan identity/version/digest;
- scope reference(s);
- stage declarations with stable sport-owned stage codes;
- required vs optional stage classification;
- event-relative or deadline timing declarations;
- dependency declarations;
- readiness-check requirements;
- immutable execution target/release references where known;
- allowed execution modes;
- required adapter capabilities;
- generic side-effect classification/policy references;
- plan validity/effective interval and schedule revision;
- plan schema/version.

TDLA may validate generic graph/contract properties but may not infer that a stage called `FINAL_LINEUPS` means anything beyond the declarations supplied by the sport contract.

A plan that requires an unavailable adapter capability is invalid for dispatch and fails closed.

---

# A-5.8 — Execution modes and side-effect safety

A-5 recognizes the certified transition states established by A-0:

- `MANUAL_UNCERTIFIED`;
- `MANUAL_CERTIFIED`;
- `AUTOMATION_SHADOW`;
- `AUTOMATION_SUPERVISED`;
- `AUTOMATION_PRODUCTION`.

Adapter requests always identify the effective execution mode.

## A-5.8.1 Shadow

`AUTOMATION_SHADOW` may compute, persist explicitly isolated test/shadow evidence, and produce comparison artifacts, but it must not create uncontrolled production-visible publication or customer-facing effects.

A sport path that bundles prediction and unavoidable production publication is **not shadow-certifiable** until it is split or wrapped with a proven no-production-side-effect mechanism.

## A-5.8.2 Supervised

`AUTOMATION_SUPERVISED` permits automation to execute certified pre-publication work while an explicit TDLA/operator gate controls the production side-effect boundary.

A sport adapter must not silently bypass the gate by invoking a monolithic command that auto-publishes.

## A-5.8.3 Production

`AUTOMATION_PRODUCTION` is allowed only when:

- the sport/manual workflow and adapter integration have received explicit certification;
- required adapter capabilities are negotiated;
- the plan permits production mode;
- the invoked immutable target is production-approved;
- side-effect policy is satisfied.

Capability support alone never grants production authority.

---

# A-5.9 — Readiness contract

## A-5.9.1 Purpose

TDLA needs to know whether a stage can proceed without learning the sport-specific rules used to make that decision.

## A-5.9.2 Readiness dispositions

A sport readiness evaluation returns one of:

- `READY` — sport-defined prerequisites are satisfied for the requested stage at the evaluated time;
- `WAITING` — not ready yet; later reevaluation is expected to be meaningful;
- `BLOCKED` — a declared blocking condition exists and generic metadata explains whether reevaluation is meaningful;
- `NOT_APPLICABLE` — the stage does not apply to this scope/revision under the sport plan.

A-9 will define how TDLA maps these into dependency/scheduler state.

## A-5.9.3 Minimum result fields

```text
ReadinessResult
- disposition
- evaluated_at
- scope_ref + revision
- stage_code
- sport_reason_code
- safe reason summary/details
- retry/reevaluation hint
- next_check_not_before (optional)
- readiness_valid_until (optional)
- evidence/provenance refs
- freshness/quality refs or summaries
- adapter/result schema version
- result digest
```

The `sport_reason_code` is opaque to TDLA orchestration logic except for storage, observability, and policy references explicitly declared by the sport plan.

TDLA must not contain branches such as:

```text
if sport == MLB and reason == PROBABLE_PITCHER_NOT_CONFIRMED: ...
```

The sport plan/readiness result instead supplies generic `WAITING`, timing hints, and evidence.

## A-5.9.4 Readiness freshness

A `READY` result is not necessarily valid forever. The sport may provide `readiness_valid_until` or an equivalent revision/freshness boundary.

TDLA must not treat a stale readiness result as perpetual permission to execute when the plan requires a fresher check.

---

# A-5.10 — Invocation contract

## A-5.10.1 Invocation request

An invocation request binds a logical TDLA stage operation to an immutable sport execution target.

Minimum conceptual fields:

```text
InvocationRequest
- common request context
- scope_ref + revision
- stage_code
- plan id/version/digest
- immutable execution target/release reference
- logical idempotency key
- execution mode
- deadline/cutoff context
- validated non-secret configuration reference/digest
- input/provenance manifest references where required
- side-effect policy reference
```

TDLA must not dispatch a moving Git branch or mutable `latest` image as production authority.

## A-5.10.2 Invocation outcomes

The logical operation returns either:

1. a terminal `SportExecutionResult` for synchronous execution; or
2. an `InvocationAcknowledgement` for asynchronous execution.

Conceptual acknowledgement:

```text
InvocationAcknowledgement
- ACCEPTED | ALREADY_EXISTS | REJECTED
- child_execution_ref (when applicable)
- echoed logical idempotency/correlation identity
- accepted_at
- adapter/release identity
- safe diagnostics
```

`ALREADY_EXISTS` is a normal idempotency outcome when the same logical operation was previously accepted.

## A-5.10.3 Idempotent acceptance

For production-capable asynchronous execution, one of the following must be true:

- the sport service itself provides idempotent create/dispatch keyed by the supplied logical idempotency key; or
- the certified adapter/wrapper provides an equivalent durable deduplication mechanism.

Repeating the same logical request after a lost network acknowledgement must not blindly create another child operation.

If an integration cannot provide this property, it cannot be certified for production asynchronous dispatch until A-11 defines and implementation proves a safe compensating design.

---

# A-5.11 — Child execution identity and reconciliation

## A-5.11.1 Opaque child references

A child execution reference is owned by the sport service/adapter. TDLA stores it as provenance and uses it for reconciliation without redefining it.

Examples include an existing Daily-MLB service-generated job/run ID or a future NFL worker job reference.

## A-5.11.2 Required recovery path

An asynchronous production adapter must support safe recovery after any of these points:

```text
TDLA records intent
  -> request dispatched
      -> child accepted
          -> acknowledgement lost
              -> TDLA process/worker dies
```

After restart, TDLA must be able to determine whether the logical child operation exists before redispatching.

A conforming async adapter therefore supports:

- reconciliation by known child reference; and
- lookup/reconciliation by the logical idempotency key or an equivalent durable deduplication handle for the acknowledgement-lost case.

## A-5.11.3 Child execution snapshot

Generic child state is represented as:

- `PENDING`;
- `RUNNING`;
- `SUCCEEDED`;
- `FAILED`;
- `CANCELLED`;
- `UNKNOWN` / `NOT_FOUND` where distinguishable.

Minimum snapshot metadata includes:

- child reference when known;
- echoed idempotency/correlation key;
- observed state;
- observed_at;
- started/finished timestamps when available;
- terminal result reference when terminal;
- safe diagnostics;
- sport/provider nested provenance references when exposed.

`UNKNOWN` is not equivalent to `FAILED`, and it is not authorization to start a duplicate child.

A-12 will define platform recovery/escalation behavior for unresolved unknown state.

---

# A-5.12 — Cancellation and timeout contract

Cancellation is capability-declared.

A cancellation acknowledgement may report:

- `ACCEPTED` / `REQUESTED`;
- `ALREADY_TERMINAL`;
- `NOT_SUPPORTED`;
- `NOT_FOUND`;
- `REJECTED`.

Important invariants:

1. A TDLA timeout means the outer control plane reached a declared wait/execution boundary. It does not prove the child process stopped.
2. A cancellation request acknowledgement does not prove the child stopped.
3. After cancellation/timeout of an async child, reconciliation continues until terminal state or explicit orphan/unknown handling under A-12.
4. TDLA may not label a still-running child `CANCELLED` merely because the outer worker stopped waiting.
5. A sport system may refuse cancellation when its operation is not safely cancellable; this must be declared rather than faked.

---

# A-5.13 — Result contract

## A-5.13.1 Semantic terminal dispositions

A sport terminal result reports one of:

- `SUCCEEDED`;
- `SUCCEEDED_DEGRADED`;
- `FAILED`;
- `CANCELLED`;
- `NO_OP` where the plan explicitly permits an operation that validly has nothing to do.

TDLA separately determines the final outer stage state after validating generic contract requirements.

For example, a sport may report `SUCCEEDED`, but TDLA must not mark the stage successful if a required declared artifact manifest is absent or invalid.

## A-5.13.2 Minimum result metadata

```text
SportExecutionResult
- semantic disposition
- scope_ref + revision
- stage_code
- logical idempotency/correlation identity
- child execution ref (optional for direct synchronous execution)
- adapter protocol/implementation identity
- sport execution release/commit/image identity
- started/completed timestamps
- effective prediction/cutoff timestamp where applicable
- sport result schema/version
- result digest
- artifact manifest ref(s)
- input/provenance refs
- sport-provided model identity/version metadata when applicable
- sport-provided configuration/feature-contract metadata when applicable
- degradation/failure reason code(s)
- safe diagnostics
```

Result fields not applicable to a stage may be absent, but required fields are declared by the plan/result schema rather than guessed by TDLA from stage names.

## A-5.13.3 Failure/degradation meaning

The sport owns the meaning of sport-specific failure/degradation reasons.

It may also provide generic hints such as `retry_recommended` or a broad transient/permanent classification, but A-11/A-12 define how TDLA uses such hints. TDLA may enforce generic infrastructure failures independently.

## A-5.13.4 Result immutability

A terminal result reference/digest used by a completed production attempt is immutable evidence.

If the sport later produces corrected or newer output, it must be represented as a new lineaged execution/result or explicit versioned replacement rather than silently changing the content behind the old authoritative digest.

---

# A-5.14 — Artifact manifest handoff

A-5 freezes the adapter-level handoff while detailed artifact storage/retention architecture belongs to A-14.

An adapter result references one or more versioned manifests rather than requiring TDLA to know sport-specific filenames.

Minimum manifest-reference concepts:

- manifest schema/version;
- immutable manifest handle/location;
- manifest SHA-256 or equivalent approved content digest;
- artifact owner/retention authority;
- generated timestamp;
- scope/stage/result correlation.

A referenced manifest must be able to describe individual artifacts with concepts such as:

- logical artifact role/type;
- schema/media type;
- immutable location/handle;
- size;
- content hash;
- required/optional status;
- provenance/input references;
- retention/storage metadata where applicable.

Mutable convenience aliases such as `latest/report.json` may exist, but they are not historical production authority without the immutable digest/manifest behind them.

TDLA does not infer that `predictions.json` is required for MLB while some other filename is required for NFL; the plan/result contract declares required logical artifacts.

---

# A-5.15 — Settlement and evaluation operations

The same adapter boundary must support post-event workflows without teaching TDLA sport settlement logic.

A sport adapter may expose plan/stage operations for:

- settlement;
- grading;
- postgame feature/materialization;
- model evaluation;
- calibration/performance updates;
- report correction or other certified post-event operations.

TDLA supplies generic timing/scope/execution context and invokes the sport-owned operation.

The sport owns questions such as:

- whether a wager pushes;
- whether a suspended/postponed event is graded;
- how a specific market is settled;
- how a model metric is computed;
- whether a result is excluded under a sport-specific rule.

TDLA may persist the returned status/artifact/provenance metadata but cannot independently re-grade sport outcomes as orchestration logic.

---

# A-5.16 — Security and service identity boundary

1. Adapter transport must authenticate TDLA/service callers according to the deployment's service-identity policy.
2. Authorization must distinguish environments and, where needed, operation/side-effect classes.
3. The adapter validates that a production-only operation is not invoked with an unauthorized environment/mode.
4. Credentials are resolved by the transport/execution layer and are not returned in descriptors, readiness results, child snapshots, results, or artifact manifests.
5. Diagnostics/errors must redact secrets and sensitive headers/URLs.
6. A sport adapter must never require TDLA to persist raw provider secrets simply to reconcile a child job.
7. The effective authenticated principal/service identity should be auditable without persisting secret material.

Detailed service-identity/secrets architecture belongs to A-20.

---

# A-5.17 — Observability and provenance handoff

Every adapter operation must preserve correlation across the nested lifecycle:

```text
TDLA workflow/stage/attempt
  -> adapter operation
      -> sport child job
          -> DDC acquisition run(s)
              -> provider evidence/attempts
```

The adapter supports propagation or return of:

- TDLA correlation/trace context;
- child execution references;
- sport result/provenance references;
- DDC acquisition/raw-evidence references when the sport chooses to expose them through its result contract;
- immutable artifact/result digests;
- safe timestamps and state transitions.

TDLA must be able to trace the chain without claiming ownership of each nested identity.

Observability transport/metric naming is finalized under A-16.

---

# A-5.18 — Validation and malformed-response behavior

All adapter requests/responses used for production are schema validated.

TDLA must fail closed rather than silently coerce material contract violations such as:

- missing required protocol version;
- incompatible capability profile;
- invalid scope reference;
- malformed/naive production timestamp where an aware timestamp is required;
- result referring to the wrong TDLA logical identity;
- child acknowledgement returning a mismatched idempotency key;
- success result missing required manifest/reference;
- changed content under an allegedly immutable digest;
- unsafe secret-bearing fields where prohibited;
- production invocation against an unapproved execution mode/release.

Invalid adapter responses are infrastructure/contract failures distinct from sport semantic failure.

---

# A-5.19 — Compatibility and migration rules for existing sport systems

Existing sport repositories do not have to rewrite their internal architecture to look like TDLA.

A migration may use a thin sport-owned adapter/wrapper around an existing certified interface when the wrapper can prove:

- exact identity mapping;
- idempotent or safely reconciled invocation;
- stable child-job references when async;
- result/artifact contract compatibility;
- safe execution-mode behavior;
- immutable release targeting;
- no hidden sport logic added to TDLA;
- no production behavior change without its own sport-side certification.

For Daily-MLB, the existing pattern of an authenticated service-generated job ID, polling/status lookup, and artifact retrieval is compatible in principle with this architecture. The eventual MLB adapter must wrap the **certified final manual pipeline**, not assume the current starter collector is already the final production automation target.

Sport onboarding follows the manual-first certification sequence in `AGENTS.md`.

---

# A-5.20 — Required conformance scenarios

An A-5 implementation/candidate adapter must eventually pass contract tests corresponding to these scenarios.

## Scenario 1 — MLB probable pitcher/lineup not ready, then ready

Expected contract behavior:

- first readiness result: `WAITING` with sport-owned reason/evidence and next-check/freshness hints;
- TDLA records/waits without learning pitcher/lineup rules;
- later readiness check: `READY` for the same sport scope/stage when sport conditions change;
- no duplicate logical stage is created merely because readiness was checked more than once.

## Scenario 2 — MLB postponement/reschedule/doubleheader

Expected:

- sport system supplies revised/separate authoritative scope references and schedule revision metadata;
- TDLA does not decide canonical game identity from provider IDs;
- pending event-relative work can later be superseded/replanned under A-8;
- separate doubleheader games remain separately referenceable without baseball branches in TDLA.

## Scenario 3 — NFL/NCAAF late pre-kickoff update

Expected:

- sport owns whether injury/inactive/weather information changes readiness or warrants a later stage/snapshot;
- readiness validity/freshness can expire;
- TDLA can re-check/execute according to plan without a blanket prohibition on game-day information;
- post-kickoff data cannot be smuggled into a pregame stage merely through adapter timing.

## Scenario 4 — No-games day

Expected:

- scope discovery succeeds with zero scopes plus a covered-window/revision record;
- no false adapter/provider failure is created;
- downstream work may validly become `NO_OP`/not planned according to A-6/A-9 rules.

## Scenario 5 — Slate parent with event-level child work

Expected:

- sport plan may reference a slate scope and event child scopes;
- TDLA preserves the parent/child scope references;
- exact graph/fan-out semantics are delegated to A-6;
- TDLA does not derive event membership by parsing sport IDs.

## Scenario 6 — Optional provider degradation

Expected:

- sport decides whether minimum semantic success remains valid;
- result can be `SUCCEEDED_DEGRADED` with sport reason/evidence;
- TDLA validates generic required outputs but does not reinterpret the missing provider's sports meaning.

## Scenario 7 — TDLA dies after child accepts work

Expected:

- child may continue independently;
- after restart TDLA reconciles by child ref or idempotency key;
- no blind duplicate dispatch;
- terminal result/artifact can be recovered and linked to original outer logical run.

## Scenario 8 — Duplicate trigger/readiness event

Expected:

- identical logical operation retains one idempotency identity;
- adapter returns existing child/result or otherwise proves deduplication;
- duplicate user-visible side effect is prohibited.

## Scenario 9 — Shadow mode

Expected:

- adapter/path proves production-visible publication side effects are disabled;
- results/artifacts are still retained for comparison;
- shadow execution cannot silently become authoritative publication.

## Scenario 10 — Supervised mode

Expected:

- certified computation may finish;
- production side-effect stage remains behind an explicit TDLA/operator gate;
- adapter does not bypass the gate through a monolithic auto-publish operation.

## Scenario 11 — Production mode

Expected:

- negotiated capability + certified integration + production-approved immutable release + plan permission are all required;
- unsupported/incompatible mode fails closed.

## Scenario 12 — Settlement/evaluation after event

Expected:

- adapter exposes sport-owned post-event operation;
- TDLA invokes/records it generically;
- sport owns grading/evaluation meaning.

## Scenario 13 — Incompatible protocol/capability

Expected:

- negotiation fails before dispatch;
- no fallback guessing or silent field coercion;
- existing completed history remains valid under its recorded prior contract version.

## Scenario 14 — Lost acknowledgement before child ref is recorded

Expected:

- TDLA can query/reconcile using the original logical idempotency identity;
- existing child is recovered if it was accepted;
- a new child is not created solely because the first acknowledgement was lost.

## Scenario 15 — Child state is unknown

Expected:

- adapter returns `UNKNOWN`/`NOT_FOUND` honestly;
- TDLA does not label it failed/succeeded without evidence;
- redispatch awaits the recovery policy defined by A-11/A-12.

---

# A-5.21 — Explicit deferrals

A-5 intentionally does **not** freeze:

- exact pipeline/stage graph serialization — A-6;
- trigger deduplication/event schema — A-7;
- event-relative schedule recalculation algorithm — A-8;
- dependency evaluation persistence/state machine — A-9;
- HTTP/CLI/queue/Kubernetes worker implementation — A-10;
- exact idempotency-key construction/retry policy — A-11;
- orphan/unknown recovery escalation — A-12;
- PostgreSQL DDL and immutable ledger schema — A-13;
- object-storage/retention implementation — A-14;
- concurrency/provider budgeting — A-15;
- telemetry platform details — A-16;
- alert/incident routing — A-17;
- publication API/channel contract — A-18;
- operator UI/approval implementation — A-19;
- service-identity/secrets backend — A-20.

Implementations must not use these deferrals as permission to invent conflicting local semantics.

---

# A-5.22 — Certified-boundary summary

When A-5 is certified, the integration boundary is intended to be:

```text
TDLA
  owns outer plan/run/stage/attempt identity,
  scheduling, policy, generic validation, audit, recovery coordination
        |
        | versioned Sport Automation Adapter protocol
        v
Daily-* sport system
  owns sport scope identity/meaning,
  readiness, executable sport behavior, sport result semantics
        |
        +--> Daily-Data-Core/shared providers as sport runtime dependencies
```

The adapter makes sport behavior **orchestratable** without making it **automation-owned**.
