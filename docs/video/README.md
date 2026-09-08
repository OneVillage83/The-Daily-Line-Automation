# The Daily Line Video Engine — Production Architecture Index

Status: **ARCHITECTURE-CERTIFIED — V1 + V1.1**
Last updated: 2026-09-08

The Daily Line Video Engine (DLVE) is the production social-video subsystem of The-Daily-Line-Automation (TDLA). It converts sport-owned publishable facts into validated, branded, platform-ready video artifacts while preserving source authority, media rights, quality evidence, publication boundaries, and performance-learning provenance.

DLVE is not a sports-model repository. Daily-MLB, Daily-NFL, Daily-NCAAF, and future Daily-* repositories retain authority for sport identity, prediction logic, recommendation semantics, explanations, settlement interpretation, and factual meaning.

## Certified architecture V-0 through V-24

| Section | Topic | Authority | Status |
|---|---|---|---|
| V-0 | Mission / boundaries / topology | `V00_SOCIAL_VIDEO_ENGINE_ARCHITECTURE_V1.md` + V1.1 | **CERTIFIED** |
| V-1 | Video job / fact contracts | `V01_VIDEO_JOB_AND_FACT_CONTRACTS_V1.md` + V1.1 | **CERTIFIED** |
| V-2 | Brand / motion system | `V02_BRAND_MOTION_SYSTEM_V1.md` + V1.1 | **CERTIFIED** |
| V-3 | Template library | `V03_TEMPLATE_LIBRARY_V1.md` + V1.1 | **CERTIFIED** |
| V-4 | Render / asset / QC handoff | `V04_RENDER_ASSET_QC_HANDOFF_V1.md` + V1.1 | **CERTIFIED** |
| V-5 | Performance foundation | `V05_PERFORMANCE_EXPERIMENTATION_V1.md` + V1.1 | **CERTIFIED** |
| V-6 | Script / narrative generation | `V06_SCRIPT_NARRATIVE_GENERATION_V1.md` + V1.1 | **CERTIFIED** |
| V-7 | Asset / media / rights | `V07_ASSET_MEDIA_RIGHTS_ARCHITECTURE_V1.md` + ADR-0009 | **CERTIFIED** |
| V-8 | Voice / audio | `V08_VOICE_AUDIO_ARCHITECTURE_V1.md` | **CERTIFIED** |
| V-9 | Captions / accessibility | `V09_CAPTIONS_ACCESSIBILITY_ARCHITECTURE_V1.md` | **CERTIFIED** |
| V-10 | Render runtime / deployment | `V10_RENDER_RUNTIME_DEPLOYMENT_ARCHITECTURE_V1.md` + ADR-0008 | **CERTIFIED** |
| V-11 | QC / certification | `V11_QC_CERTIFICATION_ARCHITECTURE_V1.md` | **CERTIFIED** |
| V-12 | Persistence / provenance ledger | `V12_PERSISTENCE_PROVENANCE_LEDGER_V1.md` | **CERTIFIED** |
| V-13 | Publication / distribution contract | `V13_PUBLICATION_DISTRIBUTION_CONTRACT_V1.md` | **CERTIFIED** |
| V-14 | Analytics / attribution | `V14_ANALYTICS_INGESTION_ATTRIBUTION_V1.md` | **CERTIFIED** |
| V-15 | Experimentation / causal learning | `V15_EXPERIMENTATION_CAUSAL_LEARNING_V1.md` + ADR-0010 | **CERTIFIED** |
| V-16 | Cost / resource budgeting | `V16_COST_RESOURCE_BUDGETING_V1.md` | **CERTIFIED** |
| V-17 | Observability / incidents | `V17_OBSERVABILITY_ALERTING_INCIDENTS_V1.md` | **CERTIFIED** |
| V-18 | Security / service identity | `V18_SECURITY_SECRETS_SERVICE_IDENTITY_V1.md` | **CERTIFIED** |
| V-19 | HA / backup / DR | `V19_HA_BACKUP_DISASTER_RECOVERY_V1.md` | **CERTIFIED** |
| V-20 | CI/CD / release certification | `V20_CI_CD_RELEASE_CERTIFICATION_V1.md` | **CERTIFIED** |
| V-21 | Multi-sport / platform scaling | `V21_MULTI_SPORT_PLATFORM_SCALING_V1.md` | **CERTIFIED** |
| V-22 | Operator workflow / approvals | `V22_OPERATOR_WORKFLOW_APPROVALS_V1.md` | **CERTIFIED** |
| V-23 | Retention / privacy / compliance | `V23_DATA_RETENTION_PRIVACY_COMPLIANCE_V1.md` | **CERTIFIED** |
| V-24 | Adaptive optimization | `V24_ADAPTIVE_OPTIMIZATION_ARCHITECTURE_V1.md` + ADR-0010 | **CERTIFIED** |

Governing cross-document correction authority: `V00-V24_PRODUCTION_ARCHITECTURE_ADDENDUM_V1_1.md`.

Certification evidence: `docs/implementation/DLVE_V00-V24_ARCHITECTURE_CONFORMANCE_REVIEW_20260908.md` (120 stress cases).

Subsystem status authority: `docs/implementation/DLVE_ARCHITECTURE_CERTIFICATION_LOG.md`.

## Production invariant chain

```text
Daily-* certified sport pipeline
        -> PublishableFactPackage
        -> VideoStory / VideoJob
        -> ScriptPackage + FactRefs
        -> AssetManifest / VoicePackage / CaptionPackage
        -> VideoRenderSpec
        -> RendererAdapter (Remotion V1)
        -> RenderManifest / RenderArtifact
        -> VideoQcReport
        -> VideoPublicationPackage
        -> TDLA A-18 publication/distribution
        -> platform receipt
        -> PlatformMetricSnapshot
        -> Experiment / CreativePolicyRecommendation
        -> V-24/A-24 bounded adaptive policy
```

## Non-negotiable rules

1. Sport facts and recommendations remain upstream authority.
2. Every factual clause traces to source authority.
3. Protected numbers/entities cannot drift during AI scripting.
4. Conflicting source packages fail closed; DLVE never reconciles sport truth heuristically.
5. Effective publishability uses the strictest fact/rights/policy validity bound.
6. Unknown or expired media rights block publication.
7. Generated/stock visuals cannot masquerade as documentary evidence.
8. Render success is not QC success.
9. Remotion is initial renderer, never canonical DLVE identity authority.
10. Actual external posting remains A-18 side-effect authority.
11. Performance learning cannot mutate facts, transparency, rights, compliance, or QC.
12. Adaptive selection is bounded to enumerated certified creative actions.
13. Historical evidence is immutable and correction/retraction is lineaged.

## Architecture is finished; implementation sequence is frozen

- VM-0: canonical JSON Schemas, canonical digests, golden fixtures, cross-language parity.
- VM-1: Remotion renderer scaffold and renderer adapter.
- VM-2: Daily Line brand foundation + `DailyLineBrandSting`.
- VM-3: shared data/caption components.
- VM-4: synthetic `single_pick_v1` reference composition.
- VM-5: fact-bound script generation/validation.
- VM-6: asset registry/broker + rights provenance.
- VM-7: voice/audio + captions/accessibility.
- VM-8: render worker + automated QC.
- VM-9: persistence/object-storage provenance.
- VM-10: publication package/manual bundle/A-18 integration.
- VM-11: real Daily-MLB shadow videos.
- VM-12: template certification/supervised posting.
- VM-13: analytics ingestion.
- VM-14: controlled experimentation.
- VM-15: NFL/NCAAF onboarding.
- VM-16: production auto-render certification.
- Later: scale/HA/cost/adaptive selection only under their certified parent policies.

No further greenfield video-architecture planning is required before VM-0. New findings during implementation must be handled as explicit versioned architecture changes, not ad hoc code decisions.