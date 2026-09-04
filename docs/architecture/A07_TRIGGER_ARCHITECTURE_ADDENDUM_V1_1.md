# A-7 Trigger Architecture — Certification Addendum V1.1

Date: 2026-09-04  
Status: **CERTIFICATION CLARIFICATION — governs A-7 V1 together with the base document**

This addendum records clarifications identified during the independent A-7 conformance review. It does not replace `A07_TRIGGER_ARCHITECTURE_V1.md`; the two documents together form the certified A-7 contract if certification is granted.

## 1. Source occurrence family identity vs event-revision identity

A source that supports corrections/revisions needs two related identities:

```text
TriggerOccurrenceKey
  = source namespace + stable source occurrence ID

TriggerEventRevisionKey
  = TriggerOccurrenceKey + source revision/version identity
```

The occurrence key groups revisions/corrections/retractions that refer to the same source occurrence family.

The revision key identifies one immutable semantic event revision.

Consequences:

- redelivery of the same occurrence + revision maps to the same immutable `TriggerEvent`;
- a correction with a new revision becomes a new immutable `TriggerEvent` linked to the same occurrence family;
- a retraction becomes another immutable revision/lineage event rather than deleting prior evidence;
- TDLA must not treat every correction as an unrelated event solely because its payload digest changed.

A source without native revision semantics may still represent correction/retraction lineage through an integration-specific versioned contract, but that behavior must be explicit.

## 2. Conflicting payload under the same claimed semantic event identity fails closed

If the same:

```text
source_namespace
+ source occurrence identity
+ source revision identity
```

arrives again with a different semantic payload digest, TDLA must not silently choose one payload, overwrite the earlier event, or label the delivery a harmless duplicate.

This is an **event-identity conflict**.

The delivery remains sanitized audit evidence and the event is quarantined/fails closed for authoritative reevaluation until the source-specific policy resolves the conflict.

This protects against:

- buggy providers reusing event IDs;
- mutable webhook payloads under supposedly immutable revisions;
- tampering/corruption;
- incorrect deterministic ingress identity strategies.

A later explicit correction/revision with a new revision identity is not an identity conflict.

## 3. Eligibility reevaluation has logical identity distinct from processing attempts

`EligibilityReevaluationRequest` is itself a logical work item and must not be identified solely by a physical trigger-evaluation worker attempt.

For the same target and same effective trigger cause/binding authority:

```text
logical reevaluation identity        SAME
trigger-evaluation processing attempt NEW on retry
```

A stable reevaluation identity must be derived/enforced from sufficient semantic material such as:

- exact target resolved-plan/stage/materialization authority;
- binding version/digest;
- trigger event/cause-set identity;
- relevant scope/revision context;
- environment/mode.

The exact hashing/database uniqueness algorithm remains deferred to A-11/A-13, but the logical-vs-physical separation is mandatory.

This prevents a crash after `TriggerEvaluation` persistence from creating uncontrolled duplicate reevaluation work on restart.

## 4. Accepted trigger evidence and reevaluation intent must be durable before downstream dispatch authority

A-7 V1 requires durable accepted evidence before irreversible action. Certification clarifies the minimum causal durability boundary:

```text
accepted TriggerDelivery/TriggerEvent evidence
        -> durable TriggerEvaluation / reevaluation intent
            -> downstream eligibility/execution processing
```

A crash after trigger receipt but before downstream execution must be recoverable from persisted evidence/intent without requiring the source to redeliver.

A crash after downstream eligibility evaluation but before dispatch remains protected by A-11 logical idempotency, but TDLA must still retain the durable trigger cause chain.

Exact transaction/outbox mechanics remain A-13.

## 5. Trust rejection cannot create an authoritative semantic TriggerEvent

A physically received external delivery may be recorded in sanitized rejected-delivery form for diagnostics, but if authentication/trust validation fails it cannot create an authoritative `TriggerEvent` eligible for binding evaluation.

Therefore:

```text
untrusted delivery
    -> sanitized rejected TriggerDelivery evidence (policy permitting)
    -> NO authoritative TriggerEvent
    -> NO eligibility reevaluation
```

This does not prevent A-20 from later defining richer quarantine/forensics behavior.

## 6. Coalescing cannot cross incompatible authority revisions silently

A `TriggerCauseSet` / debounce window may aggregate events only when the versioned coalescing policy declares them compatible for the same reevaluation target authority.

It must not silently combine events across incompatible:

- resolved plan digests;
- StageRef/materialization revisions;
- sport scope/schedule revisions;
- TriggerBinding versions;
- environments/execution modes.

If authority changes during a debounce window, the old cause set closes/supersedes according to policy and the new-authority event starts or joins the appropriate new cause set.

Raw events remain retained either way.

## Certification relationship

These clarifications are normative for A-7 certification and future trigger contract tests.

The exact Pydantic models, uniqueness constraints, database transactions, queue/outbox behavior, and retry algorithms remain implementation work under their respective later architecture sections.