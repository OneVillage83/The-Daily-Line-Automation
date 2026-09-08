# The Daily Line Video Engine — Production Architecture Index

Status: DOCUMENTED — REVIEW PENDING
Last updated: 2026-09-08

The Daily Line Video Engine (DLVE) is the production social-video subsystem of The-Daily-Line-Automation (TDLA). It converts sport-owned publishable facts into validated, branded, platform-ready video artifacts while preserving source authority, rights provenance, quality evidence, publication boundaries, and later performance-learning evidence.

DLVE is **not** a sports-model repository. Daily-MLB, Daily-NFL, Daily-NCAAF, and future Daily-* repositories retain authority for sport identity, prediction logic, recommendation semantics, explanations, settlement interpretation, and factual meaning. DLVE may transform approved facts creatively; it may not derive new betting conclusions.

## Architecture sequence V-0 through V-24

| Section | Topic | Authority document | Status |
|---|---|---|---|
| V-0 | Mission / boundaries / topology | `V00_SOCIAL_VIDEO_ENGINE_ARCHITECTURE_V1.md` | Documented |
| V-1 | Video job / publishable fact contracts | `V01_VIDEO_JOB_AND_FACT_CONTRACTS_V1.md` | Documented |
| V-2 | Brand / motion system | `V02_BRAND_MOTION_SYSTEM_V1.md` | Documented |
| V-3 | Template library | `V03_TEMPLATE_LIBRARY_V1.md` | Documented |
| V-4 | Render / asset / QC handoff | `V04_RENDER_ASSET_QC_HANDOFF_V1.md` | Documented |
| V-5 | Performance / experimentation foundation | `V05_PERFORMANCE_EXPERIMENTATION_V1.md` | Documented |
| V-6 | Script / narrative generation | `V06_SCRIPT_NARRATIVE_GENERATION_V1.md` | Documented |
| V-7 | Asset / media / rights | `V07_ASSET_MEDIA_RIGHTS_ARCHITECTURE_V1.md` | Documented |
| V-8 | Voice / audio | `V08_VOICE_AUDIO_ARCHITECTURE_V1.md` | Documented |
| V-9 | Captions / accessibility | `V09_CAPTIONS_ACCESSIBILITY_ARCHITECTURE_V1.md` | Documented |
| V-10 | Render runtime / deployment | `V10_RENDER_RUNTIME_DEPLOYMENT_ARCHITECTURE_V1.md` | Documented |
| V-11 | Quality control / certification | `V11_QC_CERTIFICATION_ARCHITECTURE_V1.md` | Documented |
| V-12 | Persistence / provenance ledger | `V12_PERSISTENCE_PROVENANCE_LEDGER_V1.md` | Documented |
| V-13 | Publication / distribution contract | `V13_PUBLICATION_DISTRIBUTION_CONTRACT_V1.md` | Documented |
| V-14 | Analytics ingestion / attribution | `V14_ANALYTICS_INGESTION_ATTRIBUTION_V1.md` | Documented |
| V-15 | Experimentation / causal learning | `V15_EXPERIMENTATION_CAUSAL_LEARNING_V1.md` | Documented |
| V-16 | Cost / resource / provider budgeting | `V16_COST_RESOURCE_BUDGETING_V1.md` | Documented |
| V-17 | Observability / alerting / incidents | `V17_OBSERVABILITY_ALERTING_INCIDENTS_V1.md` | Documented |
| V-18 | Security / secrets / service identity | `V18_SECURITY_SECRETS_SERVICE_IDENTITY_V1.md` | Documented |
| V-19 | HA / backup / disaster recovery | `V19_HA_BACKUP_DISASTER_RECOVERY_V1.md` | Documented |
| V-20 | CI/CD / release / certification | `V20_CI_CD_RELEASE_CERTIFICATION_V1.md` | Documented |
| V-21 | Multi-sport / multi-platform scaling | `V21_MULTI_SPORT_PLATFORM_SCALING_V1.md` | Documented |
| V-22 | Operator workflow / approvals | `V22_OPERATOR_WORKFLOW_APPROVALS_V1.md` | Documented |
| V-23 | Data retention / privacy / compliance | `V23_DATA_RETENTION_PRIVACY_COMPLIANCE_V1.md` | Documented |
| V-24 | Adaptive optimization | `V24_ADAPTIVE_OPTIMIZATION_ARCHITECTURE_V1.md` | Documented |

## Production invariant chain

```text
Daily-* certified sport pipeline
        |
        v
PublishableFactPackage
        |
        v
VideoStoryCandidate / VideoJob
        |
        v
ScriptArtifact + FactRefs
        |
        +-------> AssetManifest / RightsEvidence
        +-------> VoiceArtifact
        +-------> CaptionArtifact
        |
        v
VideoRenderSpec
        |
        v
RendererAdapter (Remotion V1)
        |
        v
RenderArtifact
        |
        v
QCEvidenceBundle
        |
        v
VideoPublicationPackage
        |
        v
TDLA A-18 publication/distribution
        |
        v
Platform receipt
        |
        v
PerformanceObservation
        |
        v
Experiment / CreativeRecommendationEvidence
        |
        v
V-24 / A-24 bounded adaptive policy
```

## Core non-negotiable rules

1. Sport facts and recommendations remain upstream authority.
2. Every factual script clause traces to source facts.
3. Numeric values cannot be freely rewritten by an LLM.
4. Unknown/stale fact authority blocks publication.
5. Unknown/expired asset rights block publication.
6. Render success is not publication success; QC evidence is mandatory.
7. Remotion is the initial renderer, not canonical DLVE identity authority.
8. Publication side effects remain TDLA A-18 authority.
9. Performance learning cannot mutate sport facts or compliance/QC rules.
10. Every production artifact is immutable, versioned, and provenance-linked.
11. Every material subsystem change must update durable repo documentation.

## Implementation milestones

Architecture is intentionally complete before implementation. Recommended build sequence:

- VM-0: canonical TypeScript/Python-neutral JSON Schemas, canonical digests, golden fixtures.
- VM-1: Remotion application scaffold and renderer adapter.
- VM-2: Daily Line brand foundation and `DailyLineBrandSting`.
- VM-3: shared visual/data/caption components.
- VM-4: `single_pick_v1` on synthetic facts.
- VM-5: fact-bound script generation + validator.
- VM-6: asset registry/broker + rights provenance.
- VM-7: voice/audio + captions/accessibility.
- VM-8: render worker + automated QC evidence.
- VM-9: provenance persistence/object storage.
- VM-10: manual publication bundle / A-18 package integration.
- VM-11: real Daily-MLB shadow videos.
- VM-12: template certification and supervised posting.
- VM-13: analytics ingestion.
- VM-14: controlled experiments.
- VM-15: NFL/NCAAF onboarding.
- VM-16: production auto-render certification.
- VM-17+: multi-platform scale, HA, cost optimization, adaptive creative selection after A-24 permits it.

## Relationship to TDLA architecture

DLVE specializes but does not override TDLA A-0 through A-24. In particular:
- A-11/A-12 govern retry/recovery/idempotency semantics;
- A-13 governs authoritative persistence/immutability mechanics;
- A-15 governs resource/provider budgeting at platform level;
- A-16/A-17 govern observability/incidents;
- A-18 governs publication/distribution side effects;
- A-19 governs operator authority;
- A-20/A-21/A-22 govern security, deployment, backup, CI/CD;
- A-23 governs multi-sport isolation;
- A-24 governs any future adaptive automation authority.

Where a future certified A-section is stricter than an early DLVE design assumption, DLVE must conform through an explicit versioned update rather than silently overriding TDLA.