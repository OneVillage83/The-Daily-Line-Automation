import {createHash} from 'node:crypto';

export const SAFE_INT = 9_007_199_254_740_991;

export const DIGEST_FIELDS: Record<string, string> = {
  'publishable-fact-package.v1': 'package_digest',
  'content-candidate.v1': 'candidate_digest',
  'creative-plan.v1': 'creative_plan_digest',
  'script-package.v1': 'script_digest',
  'fact-integrity-report.v1': 'report_digest',
  'asset-plan.v1': 'asset_plan_digest',
  'asset-manifest.v1': 'manifest_digest',
  'voice-package.v1': 'voice_digest',
  'caption-package.v1': 'caption_digest',
  'video-render-spec.v1': 'render_spec_digest',
  'render-manifest.v1': 'manifest_digest',
  'video-qc-report.v1': 'report_digest',
  'video-publication-package.v1': 'package_digest',
  'platform-metric-snapshot.v1': 'snapshot_digest',
};

const SET_ARRAY_KEYS = new Set([
  'source_run_refs','allowed_story_families','supersedes_package_refs','fact_refs','supporting_fact_refs',
  'fact_package_refs','story_family_eligibility','required_claim_refs','optional_claim_refs','allowed_cta_profiles',
  'claim_refs','explanation_refs','asset_slots','experiment_refs','allowed_source_classes','fallback_chain',
  'allowed_platforms','territories','use_classes','parent_asset_refs','segment_timing_refs','sfx_asset_refs',
  'platform_intent','evidence_refs','post_copy_trace_refs','source_fact_package_refs','source_metric_refs',
]);

const OBJECT_ARRAY_SORT_KEYS: Record<string, string[]> = {
  approved_claims: ['claim_id'], approved_facts: ['fact_id'], approved_explanations: ['explanation_id'],
  fact_package_bindings: ['ref','digest'], source_fact_package_bindings: ['ref','digest'], assets: ['asset_id'],
  normalized_metrics: ['metric_name','normalization_version'], platform_intents: ['platform','target_account_ref','publish_mode'],
  gate_results: ['gate_class','code'],
};

const utf8Compare = (a: string, b: string): number => Buffer.compare(Buffer.from(a, 'utf8'), Buffer.from(b, 'utf8'));

function assertDomain(value: unknown, path = '$'): void {
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return;
  if (typeof value === 'number') {
    if (!Number.isSafeInteger(value)) throw new Error(`non-safe-integer JSON number at ${path}; decimals use strings`);
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertDomain(item, `${path}[${index}]`));
    return;
  }
  if (typeof value === 'object') {
    for (const [key, item] of Object.entries(value as Record<string, unknown>)) assertDomain(item, `${path}.${key}`);
    return;
  }
  throw new Error(`unsupported JSON value at ${path}`);
}

function normalize(value: unknown, parentKey?: string): unknown {
  if (Array.isArray(value)) {
    const items = value.map((item) => normalize(item));
    if (parentKey && SET_ARRAY_KEYS.has(parentKey) && items.every((item) => typeof item === 'string')) {
      return [...items].sort((a, b) => utf8Compare(a as string, b as string));
    }
    const sortKeys = parentKey ? OBJECT_ARRAY_SORT_KEYS[parentKey] : undefined;
    if (sortKeys && items.every((item) => item !== null && typeof item === 'object' && !Array.isArray(item))) {
      return [...items].sort((a, b) => {
        for (const key of sortKeys) {
          const av = String((a as Record<string, unknown>)[key] ?? '');
          const bv = String((b as Record<string, unknown>)[key] ?? '');
          const c = utf8Compare(av, bv);
          if (c !== 0) return c;
        }
        return 0;
      });
    }
    return items;
  }
  if (value !== null && typeof value === 'object') {
    const input = value as Record<string, unknown>;
    const output: Record<string, unknown> = {};
    for (const key of Object.keys(input).sort(utf8Compare)) output[key] = normalize(input[key], key);
    return output;
  }
  return value;
}

export function canonicalize(value: unknown): Buffer {
  assertDomain(value);
  return Buffer.from(JSON.stringify(normalize(value)), 'utf8');
}

export function semanticDigest(document: Record<string, unknown>): string {
  const version = String(document.schema_version ?? '');
  const digestField = DIGEST_FIELDS[version];
  if (!digestField) throw new Error(`unsupported schema_version for digest: ${version}`);
  const payload = structuredClone(document);
  delete payload[digestField];
  return `sha256:${createHash('sha256').update(canonicalize(payload)).digest('hex')}`;
}
