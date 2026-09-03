# A-5 Sport Automation Adapter — Certification Addendum V1.1

Date: 2026-09-03  
Status: **CERTIFICATION CLARIFICATION — governs A-5 V1 together with the base document**

This addendum records clarifications identified during the independent A-5 conformance review. It does not replace `A05_SPORT_AUTOMATION_ADAPTER_V1.md`; the two documents together form the certified A-5 contract.

## 1. Logical idempotency identity vs physical attempt identity

A TDLA physical `attempt_id` is correlation/audit metadata only.

It must **never** be used by a sport adapter as the deduplication identity for a logical child operation, because retries intentionally create new physical attempt IDs.

For a retry of the same logical sport operation:

```text
logical stage/run identity        SAME
logical idempotency key           SAME
TDLA physical attempt ID          NEW
sport child operation             SAME logical child / safely recovered existing child
```

An adapter that keys child creation on `attempt_id` rather than the logical idempotency identity would create duplicates on normal retry and is non-conforming.

The exact construction of the logical idempotency key remains deferred to A-11.

## 2. Manual lifecycle states are not unattended-dispatch authority

`MANUAL_UNCERTIFIED` and `MANUAL_CERTIFIED` are onboarding/certification lifecycle states established by A-0.

They do **not** authorize TDLA to perform unattended production automation merely because the adapter technically accepts the value.

For adapter-driven automation, the relevant execution-authority modes are:

- `AUTOMATION_SHADOW`;
- `AUTOMATION_SUPERVISED`;
- `AUTOMATION_PRODUCTION`.

A manually initiated diagnostic/wrapper invocation may carry manual-state context for provenance, but it remains a manual/operator-controlled operation and cannot be mistaken for certified automation authority.

## 3. Capability support is not authorization

An `AdapterDescriptor` may declare that an implementation technically supports shadow, supervised, or production behavior.

That declaration means only **interface capability**.

Actual authority to execute in a mode requires all applicable controls, including:

- architecture/integration certification status;
- environment authorization;
- plan permission;
- immutable approved release/target;
- side-effect policy;
- operator gate where required.

Therefore:

```text
capability_profile.supports_production == true
```

must never be treated as equivalent to:

```text
this integration is authorized for production automation
```

The certification log remains the authority record for onboarding/promotion.

## 4. Lost-acknowledgement reconciliation requirement is production-critical

For asynchronous adapters, the acknowledgement-loss window is explicitly part of the certified A-5 boundary:

```text
child accepted
-> response lost before TDLA persists child_execution_ref
-> TDLA restarts
```

A production-capable adapter must be able to reconcile that logical operation using the stable logical idempotency identity or an equivalent durable deduplication handle.

Reconciliation solely by a child ID that TDLA may never have received is insufficient for production asynchronous certification.

## Certification relationship

These clarifications are normative for A-5 certification and must be included in future adapter contract tests.
