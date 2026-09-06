# A-10 Worker / Execution Backend Architecture V1

Date: 2026-09-05  
Status: **DOCUMENTED — REVIEW PENDING**

## 1. Purpose

A-10 defines the replaceable physical execution plane for The Daily Line Automation (TDLA).

A-0 through A-9 already define:

- canonical TDLA workflow/run/attempt identity;
- sport ownership boundaries;
- immutable resolved-plan/stage authority;
- durable triggers;
- event-relative schedule authority;
- dependency/readiness/current-authority eligibility;
- version-bound `DispatchEligibilityGrant` evidence.

A-10 begins only after those logical decisions exist.

Its job is to answer:

> **How does one already-eligible logical stage operation become a safely submitted, observable, cancellable, and reconcilable physical execution without making the backend, worker, queue, process, pod, container, or Prefect runtime the canonical workflow authority?**

A-10 intentionally does **not** finalize A-11 retry/idempotency algorithms, A-12 failure policy, A-13 PostgreSQL DDL/transactions, A-15 resource budgeting, A-20 service identity, or A-21 deployment/HA topology.

---

# 2. Governing rule

> **A worker/backend is an execution mechanism, not workflow authority. TDLA canonical StageRun/RunAttempt identity, immutable execution envelope, eligibility authority, and child-operation provenance remain valid when the physical backend changes. A backend acknowledgement or process exit code is never sufficient proof of semantic success.**

The canonical direction is:

```text
A-9 DispatchEligibilityGrant
        |
        v
A-10 final current-authority verification
        |
        v
A-11 logical execution / attempt authority
        |
        v
immutable ExecutionEnvelope
        |
        v
durable DispatchRecord / intent
        |
        v
backend submission
        |
        +---- backend-native execution handle
        |
        v
worker / transport
        |
        v
A-5 Sport Automation Adapter
        |
        +---- sport child execution ref
        |
        v
semantic SportExecutionResult + manifests
```

No arrow in this chain allows a lower physical layer to replace a higher canonical identity.

---

# 3. Ownership boundary

## 3.1 TDLA owns

TDLA owns generic execution-plane concepts including:

- execution backend descriptors;
- worker class/capability requirements;
- dispatch intent and assignment evidence;
- immutable execution envelopes;
- backend submission/reconciliation evidence;
- physical worker/backend cross-references;
- generic cancellation/timeout transport evidence;
- execution/result handoff into later TDLA state;
- final output/result contract validation coordination.

## 3.2 Sport repositories own

Sport repositories/services retain:

- sport-specific execution behavior;
- sport child-operation identity;
- internal sport worker/service decomposition;
- model/simulation/prediction logic;
- sport-specific result/degradation semantics;
- sport-specific readiness meaning;
- sport-specific settlement/evaluation meaning.

A-10 invokes sport work only through the certified A-5 adapter boundary.

## 3.3 Daily-Data-Core owns

DDC retains shared acquisition/provider/fact infrastructure and its nested acquisition/provider identities.

A-10 may carry/retain DDC-related provenance returned by sport execution but does not reimplement DDC acquisition logic.

---

# 4. Canonical identity layers

A-10 must keep the following identities distinct:

```text
TDLA WorkflowRun
TDLA StageRun
TDLA RunAttempt
A-9 DispatchEligibilityGrant
A-10 DispatchRecord / dispatch intent
A-10 WorkerAssignment
backend-native submission/job/task/message/process/pod handle
A-5 sport child execution ref
DDC acquisition/provider refs where applicable
```

A physical backend handle may be useful for reconciliation but is never canonical StageRun or RunAttempt identity.

Examples of non-canonical physical IDs:

- Prefect flow/task/deployment/run IDs;
- Kubernetes Job/Pod UID;
- Docker container ID;
- Celery/queue message ID;
- operating-system PID;
- hostname/VM ID;
- cloud batch-job ID.

These are provenance/cross-reference fields only.

---

# 5. ExecutionBackendDescriptor

Every production-capable backend exposes a versioned descriptor.

Conceptually:

```text
ExecutionBackendDescriptor
- backend_namespace
- backend_kind
- implementation_version
- immutable release/build identity
- submission_contract_version
- reconciliation_capabilities
- cancellation_capabilities
- callback/event capabilities
- supported worker classes
- supported environments
- supported execution modes
- trust/service-identity class refs
- generated_at
- descriptor_schema_version
- descriptor_digest
```

Possible backend kinds include:

- `LOCAL_SUBPROCESS`;
- `OCI_CONTAINER`;
- `SPORT_SERVICE`;
- `QUEUE_WORKER`;
- `PREFECT`;
- `KUBERNETES_JOB`;
- future remote/batch/GPU systems.

The enumeration is extensible. Canonical execution identity must not depend on one backend kind.

---

# 6. WorkerClassRef vs WorkerInstance

A-10 distinguishes logical worker requirements from ephemeral workers.

```text
WorkerClassRef
    = stable versioned capability target

WorkerInstance
    = ephemeral process/node/pod/container/agent
```

A plan/stage may declare a worker class or resource hint such as:

- standard CPU;
- heavy CPU;
- GPU class;
- isolated publication worker;
- controlled-network worker;
- research worker.

It must not bind business identity to `server-12`, pod UID, hostname, or one physical machine.

A worker-class descriptor is versioned/digested and can be superseded independently of individual workers.

---

# 7. Worker capability model

Generic worker/backend capability matching may include:

- OS/CPU architecture constraints when technically required;
- OCI/container support;
- memory/storage class;
- GPU accelerator class;
- network/egress class;
- provider/service-network reachability class;
- A-5 adapter transport/protocol compatibility;
- environment authorization;
- execution-mode authorization;
- secret/service-identity retrieval capability;
- filesystem/object-storage access class;
- customer-visible/destructive side-effect authorization class;
- cancellation/reconciliation support;
- worker capability descriptor version/digest.

Capability support does **not** itself grant production authority.

A compatible worker still requires current A-9 authority, later A-11 logical execution authority, immutable target/config, and all applicable certification/operator/side-effect gates.

If no compatible authorized worker/backend exists, dispatch fails closed with an operational disposition rather than being mislabeled as sport failure or sport readiness failure.

A-15 later owns capacity allocation, concurrency, quotas, and optimization.

---

# 8. A-9 DispatchEligibilityGrant consumption

Before any physical dispatch side effect, A-10 validates the supplied A-9 grant.

Required checks include:

1. grant schema/version/digest integrity;
2. exact stage materialization binding;
3. exact plan digest;
4. exact sport scope/scope revision;
5. exact schedule resolution/window authority when applicable;
6. exact environment/execution mode;
7. grant expiry/current validity;
8. dependency/output authority witnesses;
9. readiness authority/freshness witnesses;
10. execution-affecting policy/config witnesses;
11. any A-9 mandatory current-head revalidation.

If any witness is stale, superseded, retracted, expired, or incompatible:

```text
NO PHYSICAL DISPATCH
-> persist stale/rejected evidence
-> request/route eligibility reevaluation
```

A-10 must not silently create a replacement A-9 grant.

---

# 9. Boundary with A-11

A-10 verifies physical dispatch eligibility and constructs the immutable execution request.

A-11 will define:

- exact logical idempotency-key construction;
- whether an existing logical StageRun/attempt already satisfies or owns the operation;
- retry attempt creation rules;
- timeout/retry progression;
- duplicate-attempt prevention/coordination;
- ambiguous retry decisions.

Therefore the intended boundary is:

```text
A-9 grant current
      |
      v
A-10 physical/backend eligibility current
      |
      v
A-11 logical operation + RunAttempt authority
      |
      v
A-10 immutable envelope + physical submission
```

No backend submission happens before A-11 has granted the required logical attempt authority.

A-10 may define what the attempt/envelope must carry without pre-deciding A-11 key formulas or retry algorithms.

---

# 10. Immutable ExecutionEnvelope

Every physical attempt receives one immutable, schema-versioned execution envelope.

Conceptually:

```text
ExecutionEnvelope
- workflow_run_ref
- stage_run_ref
- run_attempt_ref
- stage_materialization_ref
- stage_ref + version
- resolved_plan_id/version/digest
- eligibility_evaluation_ref/digest
- dispatch_eligibility_grant_ref/digest
- sport_scope_ref + revision
- schedule_resolution/occurrence refs where applicable
- timing/deadline/cutoff context
- immutable sport execution target/release/image digest
- A-5 adapter descriptor/protocol/capability binding
- validated non-secret config ref/digest
- logical idempotency identity/ref supplied by A-11
- immutable input manifest/provenance refs
- expected output/result contract refs
- environment
- execution_mode
- side_effect_class/policy refs
- worker_class/backend requirement refs
- generic resource hints
- timeout/cancellation policy refs
- service-identity/secret logical refs only
- trace/correlation refs
- created_at
- envelope_schema_version
- envelope_digest
```

Raw secret values are never semantic envelope fields.

The envelope is immutable after dispatch authority is established. Changes require a new authority/attempt according to later A-11/A-12 rules rather than editing the old envelope.

---

# 11. ExecutionEnvelope digest semantics

Production envelope identity uses schema-controlled canonicalization.

Execution-semantic fields normally include:

- TDLA attempt/stage/plan authority;
- grant/current-authority binding;
- sport scope revision;
- immutable execution target;
- adapter version/protocol;
- configuration digest;
- logical idempotency identity;
- input manifests/provenance;
- expected output contract;
- environment/mode;
- side-effect policy;
- worker class/capability requirements;
- execution policy refs.

Audit-only physical metadata normally excludes:

- assigned hostname;
- pod/container ID;
- worker log path;
- backend callback ID;
- process PID;
- transient queue delivery tag.

Schema rules, not ad-hoc code, decide digest participation.

Equivalent semantic envelopes must canonicalize to the same semantic digest even when incidental serialization order differs.

---

# 12. Durable dispatch intent before external action

A-10 requires durable TDLA dispatch/attempt intent before irreversible backend submission.

Conceptual order:

```text
current eligibility verified
-> A-11 logical attempt authority exists
-> ExecutionEnvelope frozen
-> DispatchRecord/intent durably recorded
-> backend submission allowed
```

The forbidden order is:

```text
external child starts
-> maybe record TDLA attempt later
```

Exact PostgreSQL transaction/outbox/unique-key mechanics remain A-13.

The architecture nevertheless requires recovery to know whether intent existed before external action.

---

# 13. DispatchRecord

A durable dispatch record conceptually captures:

```text
DispatchRecord
- dispatch_id
- run_attempt_ref
- execution_envelope_ref/digest
- backend_descriptor_ref/digest
- worker_class_ref
- dispatch_intent_created_at
- submission_state
- backend_submission_ref when known
- worker_assignment_ref when known
- child_execution_ref when known
- reconciliation_state
- cancellation state refs
- result handoff refs
- schema/version
```

`dispatch_id` is TDLA-owned. Backend IDs remain cross-references.

---

# 14. WorkerAssignment and ExecutionHandle

`WorkerAssignment` records which physical worker/backend instance became responsible for observing/submitting/hosting an attempt.

`ExecutionHandle` is a generic wrapper around backend-native references required for reconciliation.

Conceptually:

```text
ExecutionHandle
- backend_namespace
- backend_descriptor_version
- backend_job/task/submission ref
- worker_instance ref when known
- created/observed timestamp
- safe opaque reconciliation metadata
```

Neither identity replaces TDLA RunAttempt.

One RunAttempt may accumulate multiple physical observations/assignments during recovery while remaining one logical physical attempt under A-11 semantics.

---

# 15. Dispatch acknowledgements

A backend acknowledgement is transport evidence only.

Possible generic acknowledgement dispositions:

- `ACCEPTED`;
- `ALREADY_EXISTS` when backend supports idempotent submission;
- `REJECTED`;
- `AMBIGUOUS` / no authoritative acknowledgement;
- `UNAVAILABLE`.

`ACCEPTED` does not prove:

- a worker started;
- the A-5 adapter was invoked;
- a sport child exists;
- the child succeeded;
- required outputs exist.

Likewise a queue broker acknowledgement proves only what its transport contract says, not semantic completion.

---

# 16. Two independent lost-acknowledgement layers

A-10 explicitly recognizes two distinct distributed-failure boundaries.

## 16.1 Backend submission acknowledgement loss

```text
TDLA records dispatch intent
-> submits backend job/message
-> backend accepts
-> acknowledgement lost
-> TDLA restarts
```

TDLA must reconcile whether the backend submission exists before creating another physical submission for the same attempt.

## 16.2 Sport child acknowledgement/reference loss

```text
worker/backend exists
-> A-5 adapter invokes sport child
-> sport child accepts
-> child ref/ack lost before TDLA records it
```

Recovery uses the A-5 logical idempotency/equivalent durable lookup contract before reinvocation.

These are different identities and both may occur in the same execution.

Backend reconciliation cannot substitute for sport-child reconciliation, and sport-child reconciliation cannot prove whether a backend job exists.

---

# 17. Backend reconciliation contract

A production-capable backend descriptor declares its safe reconciliation abilities.

Possible lookup keys include:

- TDLA dispatch/attempt identity;
- execution-envelope digest;
- backend submission idempotency token;
- backend job handle;
- worker assignment;
- queue message/dedup token;
- child-ref/logical-idempotency context where transport design exposes it.

Conceptual reconciliation result:

```text
BackendReconciliationResult
- dispatch_id / run_attempt_ref
- FOUND_RUNNING
- FOUND_TERMINAL
- NOT_FOUND_CONFIRMED
- AMBIGUOUS
- MULTIPLE_CONFLICT
- backend handle(s)
- observed_at
- safe diagnostics
- result/callback refs when available
```

`NOT_FOUND_CONFIRMED` is stronger than a transient lookup failure.

`AMBIGUOUS` is not permission to blindly resubmit.

For production side-effecting paths, a backend unable to reconcile ambiguous submissions must either have a proven A-11 compensating design or fail production certification.

---

# 18. Queue/claim/lease semantics

Queue claims and leases are runtime coordination, not canonical attempt identity.

A-10 requires:

- duplicate message delivery is possible;
- more than one worker may observe/claim the same dispatch under failure;
- lease expiration does not prove prior worker/process/child termination;
- claim loss does not grant permission for duplicate external side effects;
- worker/backend must retain enough identity to reconcile prior submission/child state;
- final duplicate logical work protection remains A-11.

Exact locking/lease SQL and broker semantics remain A-13/A-21 implementation concerns.

---

# 19. Worker heartbeat/liveness evidence

Heartbeat is operational evidence, not execution truth.

Heartbeat loss may mean:

- worker died before sport invocation;
- worker died after child invocation;
- worker is alive but partitioned;
- backend job continues without worker heartbeat;
- sport child continues independently;
- result already exists but reporting failed.

Therefore:

```text
heartbeat missing != attempt failed
heartbeat missing != child stopped
heartbeat missing != safe to retry
```

Reconciliation comes before destructive retry/resubmission decisions.

---

# 20. Worker crash boundaries

## 20.1 Crash before sport invocation

If assignment occurred but the worker died before A-5 invocation, reconciliation should prove no child was accepted before later A-11 retry progression.

## 20.2 Crash after child accepted but before child ref recorded

The immutable envelope must preserve the A-11 logical idempotency identity so A-5 child lookup/reconciliation can recover the existing operation.

## 20.3 Crash after child ref recorded

TDLA can continue child reconciliation independently of the original worker instance.

## 20.4 Crash after terminal result exists but before TDLA completion update

Recovery retrieves/validates the already-existing semantic result/manifests. It must not rerun simply because the worker died before acknowledgement.

---

# 21. Synchronous vs asynchronous A-5 invocation

A-10 supports both certified A-5 shapes.

## Synchronous

```text
worker invokes adapter
-> terminal SportExecutionResult returned
-> validate result/manifests
```

## Asynchronous

```text
worker invokes adapter
-> InvocationAcknowledgement + child ref / ALREADY_EXISTS
-> reconcile child until terminal or hand off event/poll path
-> fetch terminal SportExecutionResult
```

The same TDLA StageRun/RunAttempt/ExecutionEnvelope authority applies regardless of transport style.

---

# 22. Immutable execution target verification

Before starting production sport code, the physical execution mechanism must verify the immutable target declared by the envelope where verification is technically possible.

Production cannot silently execute:

- moving Git branches;
- mutable `latest` image tags;
- unpinned package versions;
- adapter implementation different from the resolved descriptor;
- configuration digest different from the envelope.

If a target resolves differently than the envelope authority, execution fails closed before sport work.

---

# 23. Input materialization and staging

Workers consume declared logical inputs/manifests rather than guessing filesystem names.

Generic responsibilities:

1. resolve declared input manifest references;
2. verify required schema/version/digest;
3. verify provenance/cutoff/freshness references already certified by the plan/A-9 contract;
4. stage read-only/local copies if necessary;
5. do not mutate source evidence;
6. preserve original provenance refs;
7. pass only declared inputs to the sport adapter/execution target;
8. publish results only through declared result/output contracts.

A-14 later defines artifact storage, retention, replay materialization, and object-store conventions.

---

# 24. Secret and service-identity boundary

The ExecutionEnvelope stores logical references only.

Example:

```text
secret_ref = odds_api_prod_v3
service_identity_ref = tdla_mlb_prod_executor
```

It never stores raw secret values.

Workers acquire secret material at runtime through an A-20-certified mechanism.

Raw secrets must not appear in:

- Git;
- envelope/result semantic digests;
- normal logs;
- manifests;
- safe diagnostics;
- dispatch records.

Any detected secret exposure becomes an incident/security event under later A-17/A-20 policy.

---

# 25. Network/access classes

Workers may be classified by generic connectivity/credential boundaries.

Examples:

- no external egress;
- limited provider egress;
- sport-service network access;
- object-store access;
- customer-publication endpoint access.

TDLA generic capability matching must not encode sport/provider business semantics such as “MLB pitcher feed worker.”

---

# 26. Side-effect authorization classes

A worker/backend may be technically capable of customer-visible or destructive side effects only when explicitly classified and authorized.

However:

> worker capability is not side-effect authority.

Production side effects still require:

- current resolved plan permission;
- execution mode/environment;
- A-9 eligibility;
- A-10/A-11 current/idempotent dispatch authority;
- A-19 approval where applicable;
- A-20 authenticated service identity;
- A-18 publication/distribution contract for publication work.

Shadow workers must not have uncontrolled customer-visible capabilities.

---

# 27. Timeout boundary

A-10 carries and may enforce backend-level deadline/timeout instructions referenced by the immutable envelope.

A-11 owns the exact timeout/retry state machine.

Certified semantic rule:

```text
TDLA timeout reached
!= backend job proven stopped
!= sport child proven stopped
!= safe duplicate redispatch
```

After timeout, state may become reconciliation/cancellation-required rather than immediate retry.

---

# 28. Cancellation boundary

Cancellation evidence must remain granular.

Distinguish at least:

- cancellation requested by TDLA/operator/policy;
- backend cancellation request accepted/rejected;
- worker observed cancellation;
- backend job terminal after cancellation;
- sport child cancellation requested;
- sport child cancellation accepted/rejected/not-supported;
- sport child actually terminal;
- cancellation outcome unknown.

`cancel request accepted` does not prove side effects stopped.

Cancellation cannot erase already-created external effects.

A-12/A-19 later define broader recovery/operator behavior.

---

# 29. Backend/runtime status vs semantic execution status

Physical runtime status and sport semantic result remain separate.

Examples:

```text
Prefect Completed
Docker exit 0
Kubernetes Job Complete
queue message acked
```

are not sufficient for `StageRun SUCCEEDED`.

Semantic completion requires the A-5/A-6 result/output contract, including as applicable:

- `SportExecutionResult`;
- required output manifests;
- schema/digest validation;
- provenance refs;
- declared semantic disposition;
- required artifact presence;
- degradation/failure metadata.

A backend may be `COMPLETED` while semantic result is `FAILED` or `SUCCEEDED_DEGRADED`.

---

# 30. Result commit boundary

Partial output files/artifacts are not terminal success.

A worker/execution target must expose an explicit final result/manifest commit point.

Conceptually:

```text
0..N partial/staged artifacts
        |
        v
final immutable manifest/result digest
        |
        v
eligible for semantic result validation
```

If a worker crashes before the final result/manifest authority exists, partial files cannot be treated as success.

If final authority exists and worker crashes before reporting it, reconciliation retrieves and validates that existing authority instead of rerunning.

A-13/A-14 later define atomic persistence/storage mechanics.

---

# 31. Generic execution/dispatch dispositions

A-10 needs operational states that do not masquerade as sport-state facts.

Conceptually:

- `READY_TO_SUBMIT`;
- `WAITING_BACKEND`;
- `NO_COMPATIBLE_WORKER`;
- `BACKEND_UNAVAILABLE`;
- `SUBMISSION_PENDING`;
- `SUBMITTED`;
- `SUBMISSION_AMBIGUOUS`;
- `ASSIGNED`;
- `RUNNING`;
- `RECONCILING`;
- `CANCEL_REQUESTED`;
- `BACKEND_TERMINAL`;
- `RESULT_VALIDATING`;
- `TRANSPORT_ERROR`.

These describe execution-plane state only. They are not A-5 sport readiness or semantic sport result dispositions.

Exact persisted state machine may be refined with A-11/A-12/A-13.

---

# 32. Queue ordering and stale queued work

A-10 assumes queue ordering is not business correctness.

FIFO or backend priority may optimize dispatch but cannot bypass:

- current schedule/deadline authority;
- current plan/scope/readiness/dependency authority;
- environment/mode;
- A-11 logical idempotency.

Before actual physical start, queued work must revalidate its A-9 grant/current authority.

If it became stale while queued:

```text
reject physical start
-> retain stale queue/dispatch evidence
-> request reevaluation/current replacement
```

A-15 later defines resource/deadline prioritization.

---

# 33. Environment isolation

Development, test, staging, shadow, supervised, and production execution must be separable through descriptors/capabilities/identity.

A staging worker may not silently consume a production envelope requiring customer-visible authority.

A production backend must verify:

- environment binding;
- execution mode;
- worker/service authorization class;
- immutable target;
- applicable side-effect restrictions.

A-21 later defines exact network/pool topology.

---

# 34. Shadow / supervised / production

## Shadow

- compute/evidence paths only as allowed by plan;
- no uncontrolled customer-visible/destructive side effects;
- isolated output/publication behavior.

## Supervised

- certified compute may execute;
- customer-visible/destructive path stops at explicit approval boundary;
- worker cannot self-approve.

## Production

- exact production-approved plan/grant/target/config/backend/service class required;
- backend cannot promote itself from staging/shadow/supervised to production.

---

# 35. Worker logs and telemetry

Logs are operational evidence, not result authority.

A-10 requires correlation fields sufficient to connect:

```text
workflow -> stage -> attempt -> dispatch -> backend handle -> worker -> sport child
```

Logs must be secret-sanitized.

A-16 later standardizes logging/tracing/metrics.

---

# 36. Orphan and ambiguity model

A-10 explicitly recognizes orphaned/inconsistent observations.

Examples:

1. TDLA dispatch says submitted, backend lookup says confirmed not found;
2. backend job exists but TDLA worker assignment stale/missing;
3. backend job running but worker heartbeat absent;
4. sport child exists but backend job disappeared;
5. child terminal but TDLA RunAttempt nonterminal;
6. backend terminal but child unknown;
7. result manifest exists but backend history expired;
8. multiple backend jobs found for one dispatch identity.

These states require reconciliation evidence before A-12 recovery policy chooses an action.

No ambiguity state is automatically equivalent to failure or retry permission.

---

# 37. Backend health/capacity boundary

Backend outage or exhausted capacity is an operational execution-plane condition.

It is not:

- sport `BLOCKED`;
- sport `WAITING`;
- dependency failure;
- semantic model failure.

The stage may remain eligible but unable to dispatch.

A-15 later defines quotas/capacity scheduling. A-17 later defines alert thresholds/incidents.

---

# 38. Backend replacement neutrality

Replacing a backend must not change canonical business/execution meaning.

A migration such as:

```text
local/Docker -> Prefect -> Kubernetes/queue
```

must preserve:

- WorkflowRun identity;
- StageRun identity;
- A-11 logical operation identity;
- RunAttempt lineage;
- A-9 eligibility/grant lineage;
- immutable execution-envelope semantics;
- A-5 sport child identity;
- result/artifact contracts;
- historical audit meaning.

Backend descriptors/handles show how work physically ran; they do not redefine what work was.

---

# 39. Failure-closed validation

A-10 must fail closed before physical execution for cases including:

- stale/expired A-9 grant;
- plan/scope/schedule authority changed;
- dependency/output witness retracted/superseded;
- no A-11 logical attempt authority;
- invalid envelope digest/schema;
- mutable production target;
- execution-target digest mismatch;
- incompatible adapter/backend/worker capabilities;
- wrong environment/mode;
- unauthorized side-effect worker class;
- missing/invalid required input manifest;
- secret-bearing unsafe envelope payload;
- backend ambiguous duplicate submission where no safe reconciliation exists.

---

# 40. Explicit non-authority of workers

Forbidden:

```text
worker receives queue message
-> trusts message age/contents
-> invokes sport code
```

Required conceptually:

```text
DispatchEligibilityGrant
+ current-authority revalidation
+ A-11 logical operation/attempt authority
+ immutable ExecutionEnvelope
+ durable DispatchRecord
+ compatible authorized backend/worker
        |
        v
physical submission/invocation
        |
        v
reconciliation + semantic result validation
```

---

# 41. Technology neutrality

This contract is intentionally not a Prefect, Docker, Kubernetes, Celery, or broker API design.

Those technologies may implement the contract later.

Canonical TDLA semantics must remain valid if any are replaced.

---

# 42. Deferred architecture

A-10 intentionally defers:

- exact logical idempotency keys, retry schedule, timeout state machine -> A-11;
- failure/degradation/recovery actions -> A-12;
- dispatch/outbox/lease/unique-key PostgreSQL DDL -> A-13;
- artifact retention/storage/replay materialization -> A-14;
- capacity/priority/concurrency/provider budgets -> A-15;
- detailed telemetry -> A-16;
- incidents/alerts -> A-17;
- publication transport -> A-18;
- approval controls -> A-19;
- service identity/secrets -> A-20;
- deployment/HA worker topology -> A-21;
- immutable build/release pipeline -> A-22.

These deferrals do not weaken A-10 identity/reconciliation requirements.

---

# 43. Certification expectations

A-10 should not be architecture-certified until review proves at minimum:

- stale queued grants cannot execute;
- backend-native IDs never become canonical RunAttempt identity;
- dispatch intent exists before external submission;
- backend acknowledgement loss is recoverable or fails closed;
- A-5 child acknowledgement/ref loss remains independently recoverable;
- worker/lease/heartbeat loss is not treated as proof child stopped;
- cancellation acknowledgement is not treated as terminal child proof;
- process/backend success does not replace semantic result validation;
- partial outputs cannot masquerade as terminal success;
- immutable target/input/config/envelope validation is explicit;
- environment/mode/side-effect worker capability is fail-closed;
- backend migration preserves TDLA identity;
- all 60 stress cases from `CURRENT_RESUME_POINT.md` pass.
