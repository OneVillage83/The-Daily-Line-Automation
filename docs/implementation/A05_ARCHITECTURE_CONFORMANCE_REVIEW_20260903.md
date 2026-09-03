# A-5 Sport Automation Adapter — Architecture Conformance Review

Review date: 2026-09-03  
Repository: `OneVillage83/The-Daily-Line-Automation`  
Architecture under review: `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_V1.md`  
Certification clarification: `docs/architecture/A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md`  
Related decision: `docs/adr/ADR-0002_TRANSPORT_NEUTRAL_SPORT_ADAPTER_PROTOCOL.md`

## Review purpose

A-5 was deliberately created as `DOCUMENTED — REVIEW PENDING`. This review tests whether the proposed Sport Automation Adapter contract is sufficiently sport-neutral, recoverable, idempotency-aware, vendor/transport-independent, and compatible with The Daily Line's current Daily-Data-Core / Daily-MLB / Daily-NFL architecture direction to become architecture authority for later implementation.

This is an architecture certification review only. It does not certify an actual adapter implementation, Prefect flow, database schema, or automated Daily-MLB/NFL/NCAAF production workflow.

---

# 1. Review sources

The review considered:

- TDLA A-0 through A-4 Foundation V1;
- `A00-A04_FOUNDATION_ADDENDUM_V1_1.md` nested lifecycle clarification;
- ADR-0001 vendor-neutral TDLA canonical identity;
- current Daily-Data-Core ownership/integration contracts;
- current Daily-MLB service/job boundary documented in its repository README;
- current Daily-NFL architecture rules, especially sport-owned identity/intelligence and pregame point-in-time semantics;
- the A-5 required stress cases captured in the prior TDLA resume point.

The goal was not to force existing sport repositories to already implement A-5. The goal was to ensure A-5 can wrap certified sport interfaces without moving their semantics into TDLA.

---

# 2. Certification criteria and result

| Criterion | Result | Review conclusion |
|---|---|---|
| Sport logic ownership | PASS | Readiness/result reasons remain sport-owned and opaque to generic TDLA orchestration. |
| DDC boundary | PASS | A-5 does not acquire/normalize odds, weather, venue, travel, or provider raw evidence. |
| Sport canonical identity | PASS | Scope references are sport-owned; TDLA stores references/revisions without resolving canonical game/player/team identity. |
| Multi-sport neutrality | PASS | No MLB/NFL/NCAAF-specific branch is required in generic adapter behavior. |
| Transport independence | PASS | Contract defines logical operations rather than REST routes, Python imports, or Prefect tasks. |
| Orchestrator independence | PASS | Canonical adapter/run identity remains outside Prefect, consistent with ADR-0001. |
| Version compatibility | PASS | Required capability/version mismatch fails closed before dispatch. |
| Idempotent async boundary | PASS with V1.1 clarification | Logical idempotency key is explicitly distinct from retry attempt IDs; lost-ack recovery is required. |
| Child lifecycle separation | PASS | Sport child/DDC identities remain nested provenance rather than being replaced by TDLA IDs. |
| Restart reconciliation | PASS | Async production integration must reconcile by child reference and by logical deduplication identity for lost acknowledgement. |
| Cancellation/timeout semantics | PASS | Outer timeout does not falsely imply child termination; cancellation is capability-declared and reconciled. |
| Success/output validation | PASS | Sport semantic success and TDLA generic contract success are distinct; manifest/result requirements remain enforceable. |
| Shadow/supervised safety | PASS with V1.1 clarification | Manual states do not grant automation authority; side-effect boundaries are explicit. |
| Production authorization | PASS with V1.1 clarification | Adapter capability does not equal certification/authorization. |
| Post-event compatibility | PASS | Settlement/evaluation are generic invocations whose sport meaning remains sport-owned. |
| Secret/service identity boundary | PASS at A-5 scope | Credentials stay in transport/security layer; A-20 retains detailed authority. |
| A-6/A-11/A-13 deferral discipline | PASS | A-5 avoids prematurely freezing stage graph, idempotency algorithm, or PostgreSQL DDL. |
| Documentation/resume discipline | PASS | Required architecture, ADR, review, change-log, status, and resume outputs are defined. |

No unresolved blocking architecture defect remains after the V1.1 clarification.

---

# 3. Cross-repository boundary review

## 3.1 Daily-Data-Core

Current DDC contracts own shared provider/evidence transport and sport-neutral facts such as sportsbook quotes/math, weather facts, venues, geospatial primitives, and neutral travel/rest facts. Sport repositories map those facts into their canonical sport identity/state/features.

A-5 conforms because:

- it does not call providers to create sport identity itself;
- scope discovery is explicitly a sport-owned canonical schedule/scope operation, not a new generic DDC sports-identity layer;
- adapter provenance may reference DDC acquisition evidence without making TDLA the owner of that evidence;
- A-5 artifact/result handoff is an orchestration boundary and does not replace DDC raw-evidence contracts.

Result: **PASS**.

## 3.2 Daily-MLB

The current Daily-MLB repository already demonstrates several primitives A-5 must be able to wrap:

- authenticated service invocation;
- a service-generated job/run ID;
- asynchronous status polling;
- durable run state;
- artifact retrieval;
- SQLite/raw-evidence provenance beneath the job.

This validates the nested model:

```text
TDLA logical stage/attempt
  -> MLB adapter/service invocation
      -> MLB child run ID
          -> MLB/DDC/provider evidence
```

Important compatibility finding:

The current starter Daily-MLB README describes starting a collection with `requested_date` and receiving a service-generated run ID, but it does not establish the caller-supplied logical idempotency/reconcile-by-idempotency behavior required by A-5 for production asynchronous dispatch.

Therefore:

- the existing service shape is **compatible in principle**;
- the current starter collector is **not automatically A-5 production-conforming**;
- the eventual certified MLB adapter/service wrapper must add/prove idempotent create or durable lookup by TDLA logical idempotency identity;
- this is expected future M13/M14 integration work, not a defect in A-5 architecture.

A-5 also correctly keeps probable-pitcher/lineup readiness and baseball-specific degradation meaning inside Daily-MLB.

Result: **PASS for architecture; implementation work explicitly remains future and uncertified**.

## 3.3 Daily-NFL / Daily-NCAAF compatibility

Daily-NFL architecture allows legitimately available pregame information through the prediction cutoff and requires football-specific identity/state/features to remain football-owned.

A-5 supports this by:

- carrying event start/cutoff context without computing football meaning;
- allowing readiness results to expire via `readiness_valid_until`/revision semantics;
- permitting later pregame readiness checks/snapshots under sport plans;
- retaining opaque football reason codes rather than putting injury/inactive/weather rules in TDLA;
- supporting game and slate scopes without requiring football-specific scheduler code.

The same boundary is suitable for Daily-NCAAF because conference/team/roster/schedule rules remain inside the NCAAF sport integration rather than TDLA.

Result: **PASS**.

---

# 4. Stress-case review

## 4.1 MLB probable pitcher/lineup initially unavailable

Path:

```text
check_readiness
-> WAITING
-> next_check_not_before / validity metadata
-> later check
-> READY
-> invoke same logical stage
```

The logical stage does not multiply merely because readiness was evaluated multiple times. TDLA records the sport reason without interpreting it.

Result: **PASS**.

## 4.2 MLB postponement/reschedule/doubleheader

The sport emits authoritative scope/schedule revision references. TDLA sees changed revision/timing and later A-8 will determine supersession/replanning behavior. Doubleheader games remain separate sport-owned event references.

TDLA never guesses identity from provider IDs or team/date strings.

Result: **PASS**.

## 4.3 NFL/NCAAF late inactive/injury/weather update before kickoff

Readiness may become stale and be reevaluated. The sport decides whether a new snapshot/stage is necessary; TDLA follows declared plan/timing. Cutoff context remains explicit.

Result: **PASS**.

## 4.4 No-games day

Discovery returns an authoritative empty result for the covered window, not an error.

Result: **PASS**.

## 4.5 Slate parent with game children

A-5 can carry parent and child scope references. Exact fan-out/dependency graph behavior is correctly deferred to A-6.

Result: **PASS**.

## 4.6 Optional provider degradation

The sport may report `SUCCEEDED_DEGRADED` when its certified minimum semantic contract is still met. TDLA does not decide whether missing weather/market/enrichment should be optional.

Result: **PASS**.

## 4.7 Child continues after TDLA worker/process dies

Child identity is independent. On recovery TDLA reconciles rather than creating a new operation.

Result: **PASS**.

## 4.8 Duplicate trigger/readiness events

A duplicate outer event may produce another physical scheduling/evaluation action, but invocation for the same logical operation carries the same logical idempotency identity. Retries receive new TDLA attempt IDs while the logical child identity remains deduplicated.

Result: **PASS after V1.1 clarification**.

## 4.9 Shadow mode

The architecture forbids uncontrolled customer/publication side effects. A monolithic auto-publishing sport executable is not shadow-certifiable until wrapped/split.

Result: **PASS**.

## 4.10 Supervised mode

Computation can complete while production side effects remain behind an explicit operator/TDLA gate. Adapter capability cannot bypass that gate.

Result: **PASS**.

## 4.11 Production mode

Requires capability support **and** actual certification/plan/environment/release authorization. The distinction was made normative in V1.1.

Result: **PASS**.

## 4.12 Settlement/evaluation after event completion

Uses the same generic adapter invocation/result/artifact machinery. The sport owns grading and evaluation semantics.

Result: **PASS**.

## 4.13 Incompatible adapter/TDLA protocol

Negotiation fails closed before dispatch. Existing historical runs retain their recorded older descriptor/version.

Result: **PASS**.

## 4.14 Lost acknowledgement before TDLA stores child ID

This case exposed the most important distributed-systems requirement in the review.

Safe behavior:

```text
TDLA logical idempotency key K
-> sport accepts child C
-> acknowledgement containing C is lost
-> TDLA restarts
-> reconcile/lookup(K)
-> recover C
```

A design that only supports `reconcile(child_id)` is insufficient because TDLA may never have received `child_id`.

A-5 V1 already required an equivalent lookup; V1.1 makes this explicitly production-critical.

Result: **PASS with V1.1 clarification**.

## 4.15 Child state remains unknown

`UNKNOWN`/`NOT_FOUND` is preserved honestly. TDLA does not invent success/failure and does not immediately redispatch. A-11/A-12 will define exact retry/escalation behavior.

Result: **PASS**.

---

# 5. Review findings and resolutions

## Finding A5-F1 — Physical attempt ID could be misused as child deduplication key

Risk:

A normal retry creates a new TDLA attempt ID. If the sport adapter keyed child creation on that value, every retry could start a duplicate child.

Resolution:

`A05_SPORT_AUTOMATION_ADAPTER_ADDENDUM_V1_1.md` makes logical idempotency identity the deduplication authority and labels attempt ID correlation-only.

Status: **RESOLVED**.

## Finding A5-F2 — Manual lifecycle state vs automation execution authority needed sharper wording

Risk:

`MANUAL_CERTIFIED` could be misunderstood as permission for unattended TDLA production dispatch.

Resolution:

V1.1 establishes manual values as onboarding/manual context. Unattended adapter automation authority is separately shadow/supervised/production and requires certification.

Status: **RESOLVED**.

## Finding A5-F3 — Capability declaration could be mistaken for production authorization

Risk:

An adapter that technically supports a production path could be accidentally treated as production-approved.

Resolution:

V1.1 explicitly states capability support is not authorization. Certification status, environment, plan, release, side-effect policy, and gates remain required.

Status: **RESOLVED**.

## Finding A5-F4 — Lost acknowledgement must be a first-class contract test

Risk:

Child accepted, response lost, outer process crashes, then blind retry creates duplicate expensive/model/publication work.

Resolution:

A-5 requires async production adapters to reconcile by logical idempotency identity/equivalent durable dedup handle, not only by a child ID that may never have been received.

Status: **RESOLVED**.

No additional blocking findings remain.

---

# 6. Deferred items verified as correctly deferred

The review confirms the following should **not** be solved by editing A-5 further:

- exact stage graph/plan serialization -> A-6;
- trigger identity/dedup semantics -> A-7;
- reschedule/replan algorithm -> A-8;
- dependency engine state -> A-9;
- transport/worker implementation -> A-10;
- exact idempotency key/retry construction -> A-11;
- orphan/unknown recovery/escalation -> A-12;
- PostgreSQL schema -> A-13;
- artifact retention/storage -> A-14;
- concurrency budgeting -> A-15;
- telemetry -> A-16;
- alerts/incidents -> A-17;
- publication channel/API -> A-18;
- human control UX/policy implementation -> A-19;
- security backend/service identity -> A-20.

This preserves architecture sequencing and prevents premature implementation constraints.

---

# 7. Certification decision

**A-5 Sport Automation Adapter is ARCHITECTURE-CERTIFIED as V1 governed together with the V1.1 certification addendum and ADR-0002.**

Certification authority includes:

- transport-neutral versioned adapter protocol;
- capability negotiation and fail-closed incompatibility;
- opaque sport-owned scope references;
- sport-owned discovery/planning/readiness meaning;
- logical idempotency propagation;
- async child acknowledgement/reconciliation requirements;
- explicit lost-acknowledgement recovery;
- cancellation/timeout distinction;
- semantic result/artifact handoff;
- shadow/supervised/production authority separation;
- settlement/evaluation hooks;
- security/provenance boundaries.

This does **not** certify any real sport adapter implementation.

Daily-MLB remains manual-first. The current starter job service is a useful compatibility reference but must not be treated as A-5 production-certified merely because its shape resembles the adapter contract.

## Next architecture checkpoint

**A-6 — Pipeline Plan / Stage Contracts.**

A-6 should freeze the generic plan graph, stage identity, dependency/fan-out structure, timing declarations, required/optional semantics, input/output contract declarations, side-effect classes, validity/revision rules, and how a sport adapter supplies/validates these without moving sport meaning into TDLA.
