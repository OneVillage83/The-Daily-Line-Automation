# The Daily Line Video Engine — V-22 Operator Workflow / Approval Controls V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define human controls for preview, approve, reject, regenerate, supersede, pause, and correct videos without bypassing immutable provenance.

## 2. Operator surfaces

Future UI/API should expose:
- candidate/story queue;
- source fact summary;
- script variants;
- asset preview/rights status;
- Remotion video preview;
- QC findings;
- cost estimate/actual;
- publication package/status;
- performance observations;
- experiment assignment;
- incident/correction actions.

## 3. Approval object

An approval binds operator identity, role, timestamp, exact artifact/package digest, environment/mode, decision, optional reason, and policy version. Approval of one digest does not approve a later regenerated artifact.

## 4. Actions

Allowed actions are role/policy scoped:
- approve;
- reject;
- request regenerate with declared creative change;
- choose among already-valid variants;
- pause template/sport/platform;
- mark asset unusable;
- initiate correction/retraction request;
- promote certified default after evidence/authorization.

## 5. No direct fact editing

Operators do not edit sport facts inside DLVE. Fact errors are corrected at the sport/source authority and flow through a new fact-package revision.

## 6. Regeneration

A regenerate request records what may change: hook, voice, asset, layout, etc. If script semantics or source facts change, a new appropriate artifact lineage is required.

## 7. Four-eyes option

High-risk actions such as rights override, production auto-publish enablement, or broad kill-switch release may require two-person approval under policy.

## 8. Audit

Every operator action is durable evidence. UI convenience cannot replace backend authorization and idempotency.

## 9. Tests

- approval invalidated by new digest;
- unauthorized production action;
- operator attempts direct fact edit;
- regenerate lineage;
- kill switch;
- correction request;
- optional four-eyes policy.

## 10. Definition of done

V-22 is implementation-ready when human intervention is precise, authenticated, auditable, and cannot silently rewrite source facts or historical evidence.