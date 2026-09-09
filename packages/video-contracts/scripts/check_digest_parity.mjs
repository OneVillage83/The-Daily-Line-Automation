#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SAFE_INT=9007199254740991;
const digestFields={
  'publishable-fact-package.v1':'package_digest','content-candidate.v1':'candidate_digest','creative-plan.v1':'creative_plan_digest','script-package.v1':'script_digest','fact-integrity-report.v1':'report_digest','asset-plan.v1':'asset_plan_digest','asset-manifest.v1':'manifest_digest','voice-package.v1':'voice_digest','caption-package.v1':'caption_digest','video-render-spec.v1':'render_spec_digest','render-manifest.v1':'manifest_digest','video-qc-report.v1':'report_digest','video-publication-package.v1':'package_digest','platform-metric-snapshot.v1':'snapshot_digest'
};
const setKeys=new Set(['source_run_refs','allowed_story_families','supersedes_package_refs','fact_refs','supporting_fact_refs','fact_package_refs','story_family_eligibility','required_claim_refs','optional_claim_refs','allowed_cta_profiles','claim_refs','explanation_refs','asset_slots','experiment_refs','allowed_source_classes','fallback_chain','allowed_platforms','territories','use_classes','parent_asset_refs','segment_timing_refs','sfx_asset_refs','platform_intent','evidence_refs','post_copy_trace_refs','source_fact_package_refs','source_metric_refs']);
const objectSort={approved_claims:['claim_id'],approved_facts:['fact_id'],approved_explanations:['explanation_id'],fact_package_bindings:['ref','digest'],source_fact_package_bindings:['ref','digest'],assets:['asset_id'],normalized_metrics:['metric_name','normalization_version'],platform_intents:['platform','target_account_ref','publish_mode'],gate_results:['gate_class','code']};
const cmp=(a,b)=>Buffer.compare(Buffer.from(a),Buffer.from(b));
function assertDomain(v,p='$'){if(v===null||typeof v==='string'||typeof v==='boolean')return;if(typeof v==='number'){if(!Number.isSafeInteger(v)||Math.abs(v)>SAFE_INT)throw new Error(`invalid numeric domain ${p}`);return;}if(Array.isArray(v)){v.forEach((x,i)=>assertDomain(x,`${p}[${i}]`));return;}if(typeof v==='object'){for(const [k,x] of Object.entries(v))assertDomain(x,`${p}.${k}`);return;}throw new Error(`unsupported ${p}`)}
function norm(v,parent){if(Array.isArray(v)){let x=v.map(y=>norm(y));if(setKeys.has(parent)&&x.every(y=>typeof y==='string'))x.sort(cmp);const keys=objectSort[parent];if(keys&&x.every(y=>y&&typeof y==='object'&&!Array.isArray(y)))x.sort((a,b)=>{for(const k of keys){const c=cmp(String(a[k]??''),String(b[k]??''));if(c)return c;}return 0});return x;}if(v&&typeof v==='object'){const out={};for(const k of Object.keys(v).sort(cmp))out[k]=norm(v[k],k);return out;}return v;}
function digest(doc){assertDomain(doc);const field=digestFields[doc.schema_version];const payload=structuredClone(doc);delete payload[field];const bytes=Buffer.from(JSON.stringify(norm(payload)),'utf8');return 'sha256:'+crypto.createHash('sha256').update(bytes).digest('hex');}
let failures=0;
for(const name of fs.readdirSync(path.join(root,'fixtures/valid/end-to-end')).filter(x=>x.endsWith('.json')).sort()){
 const doc=JSON.parse(fs.readFileSync(path.join(root,'fixtures/valid/end-to-end',name),'utf8')); const field=digestFields[doc.schema_version]; const got=digest(doc); if(got!==doc[field]){console.error(`FAIL ${name}: ${got} != ${doc[field]}`);failures++;} else console.log(`PASS digest parity ${name}`);
}
const stability=JSON.parse(fs.readFileSync(path.join(root,'fixtures/valid/digest-stability.json'),'utf8'));
if(!stability.matches||digest(stability.reordered_document)!==stability.original_digest){console.error('FAIL digest stability vector');failures++;}else console.log('PASS digest stability vector');
process.exitCode=failures?1:0;
