# A-10 Worker / Execution Backend Architecture — Certification Addendum V1.1

Date: 2026-09-05  
Status: **CERTIFICATION CLARIFICATION — governs A-10 V1 together with the base document**

This addendum records clarifications identified during the A-10 architecture review. It does not replace `A10_WORKER_EXECUTION_BACKEND_V1.md`; the two documents together form the certified A-10 contract if certification is granted.

## 1. Final current-authority revalidation occurs immediately before irreversible submission

A-10 V1 requires A-9 grant/current-authority verification and then A-11 logical attempt authority before physical submission.

The review clarifies that a single early check is insufficient because authority can change while A-11 creates/reconciles attempt state or while the execution envelope is materialized.

The normative conceptual sequence is therefore:

```text
A-9 DispatchEligibilityGrant
        |
        v
A-10 preflight validation
        |
        v
A-11 logical StageRun/RunAttempt authority
        |
        v
A-10 build/freeze ExecutionEnvelope
        |
        v
A-10 FINAL current-authority revalidation
        |
        +-- stale --> no backend submission; retain attempt/validation evidence; reevaluate
        |
        +-- current
               |
               v
        durable DispatchRecord/intent
               |
               v
        irreversible backend submission
```

The final check must validate every A-9/ADR-0006 witness required at the side-effect boundary, including plan/scope/schedule/dependency/readiness/policy/environment/mode authority.

If the attempt was already created but final validation fails, that does not authorize submission merely because a RunAttempt exists. Exact attempt terminal/no-start classification remains A-11/A-12.

This closes the remaining TOCTOU gap between attempt creation and physical submission.

## 2. BackendSubmissionKey is stable for one RunAttempt submission authority

A-10 requires a durable backend-submission identity separate from transient delivery/callback IDs.

Conceptually:

```text
BackendSubmissionKey
- run_attempt_ref
- dispatch_ref
- execution_envelope_digest
- backend_namespace/contract version
- stable submission identity/digest
```

The exact formula remains A-11/A-13 implementation work, but these semantics are certified:

- repeated transport submission used only to recover an ambiguous acknowledgement for the **same RunAttempt** reuses the same stable backend-submission identity where the backend supports idempotent submission;
- a new queue delivery ID, HTTP request ID, Prefect request ID, or retry callback ID must not silently become a new logical backend submission;
- a genuinely new A-11 RunAttempt receives new attempt/submission authority;
- backend lookup/reconciliation should accept the stable submission identity where technically possible;
- if a production side-effecting backend cannot provide idempotent submission or authoritative lookup by a stable identity, it requires an explicitly certified compensating A-11 design or is not production-certifiable for that path.

A physical retransmission of the same idempotent submission is not automatically a new TDLA RunAttempt.

## 3. Backend callbacks/events are observations, not canonical lifecycle ordering

Backend events may be duplicated, delayed, or delivered out of order.

Examples:

```text
COMPLETED callback
RUNNING callback arrives later
```

or:

```text
RUNNING
RUNNING duplicate
COMPLETED duplicate
```

A-10 must not derive canonical state merely by applying callbacks in receipt order.

Instead:

- every callback/event is retained as operational evidence;
- callbacks bind exact backend handle/submission/attempt authority;
- conflicting/out-of-order evidence triggers backend/child/result reconciliation;
- older events cannot roll known authoritative execution state backward;
- backend callback ordering never overrides A-5 semantic child/result state or immutable result manifests.

Exact persistence/event-state machinery remains A-13.

## 4. Worker/backend capability must be revalidated at actual assignment/start

A worker or backend descriptor may change while work is queued.

A plan/grant/envelope may express required capability classes, but before actual start A-10 must confirm the selected backend/worker instance still conforms to a current compatible descriptor revision.

If a queued assignment was based on descriptor revision R1 and the worker/backend is now R2 with incompatible capability/authorization:

```text
old assignment -> stale
no execution
-> reselect compatible worker/backend or wait/fail operationally
```

This does **not** necessarily invalidate the A-9 sport/dependency readiness itself; it invalidates the physical worker/backend selection.

Worker capability revalidation includes environment, execution mode, service-identity/access class, side-effect authorization class, adapter compatibility, and required technical resources.

## 5. Final result/manifest authority must correlate to the exact attempt/envelope/child

The existence of a final-looking file or manifest is not sufficient terminal evidence.

A terminal result/manifest authority must bind or verifiably correlate at minimum:

- TDLA StageRun/RunAttempt;
- ExecutionEnvelope digest;
- resolved plan/stage/scope authority;
- A-5 sport child execution ref or synchronous invocation correlation where applicable;
- logical idempotency identity;
- result schema/version/digest;
- expected logical output contracts/manifests.

A manifest from another attempt, replay, scope, schedule revision, or execution target cannot satisfy the current attempt merely because filenames or artifact digests happen to match.

Partial/staged files remain nonterminal until the declared correlated immutable result/manifest commit point exists.

## 6. Backend execution handle and sport child ref remain distinct logical roles even if one implementation reuses the same external ID

Some integrations may collapse physical layers. For example, a direct authenticated sport-service backend may return one service job ID that is both the backend execution handle and the sport service's child reference.

A-10 does not require artificial duplicate external identifiers, but TDLA must retain the **logical role distinction**:

```text
backend execution handle role
sport child execution ref role
```

If the same opaque external value fills both roles, both typed fields/reference relationships remain explicit in TDLA provenance.

This preserves architecture if the backend later changes to a queue/container layer in front of the sport service.

## 7. Cancellation races never suppress terminal reconciliation

Cancellation is not a terminal truth source.

If cancellation races with completion:

```text
cancel requested
backend says cancellation accepted
sport child/result already completed
```

TDLA must still reconcile and retain the actual terminal sport result/output evidence.

Likewise:

- cancellation accepted by backend does not imply sport child cancellation;
- worker stopping does not prove child stopping;
- child may complete successfully or fail after a cancel request;
- result reconciliation continues until a trustworthy terminal state is established or A-12 declares an unresolved recovery state.

Cancellation evidence remains append-only alongside the actual terminal outcome.

## Certification relationship

These seven clarifications are normative for A-10 certification and future contract/integration tests.

In particular, production implementation must prove both final pre-submission current-authority revalidation and safe reconciliation of ambiguous backend submission independently from A-5 child-operation reconciliation.