from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

SAFE_INT = 9_007_199_254_740_991

DIGEST_FIELDS = {
    "publishable-fact-package.v1": "package_digest",
    "content-candidate.v1": "candidate_digest",
    "creative-plan.v1": "creative_plan_digest",
    "script-package.v1": "script_digest",
    "fact-integrity-report.v1": "report_digest",
    "asset-plan.v1": "asset_plan_digest",
    "asset-manifest.v1": "manifest_digest",
    "voice-package.v1": "voice_digest",
    "caption-package.v1": "caption_digest",
    "video-render-spec.v1": "render_spec_digest",
    "render-manifest.v1": "manifest_digest",
    "video-qc-report.v1": "report_digest",
    "video-publication-package.v1": "package_digest",
    "platform-metric-snapshot.v1": "snapshot_digest",
}

# Arrays listed here are semantic sets in V1. They are normalized before hashing.
SET_ARRAY_KEYS = {
    "source_run_refs", "allowed_story_families", "supersedes_package_refs",
    "fact_refs", "supporting_fact_refs", "fact_package_refs", "story_family_eligibility",
    "required_claim_refs", "optional_claim_refs", "allowed_cta_profiles", "claim_refs",
    "explanation_refs", "asset_slots", "experiment_refs", "allowed_source_classes",
    "fallback_chain", "allowed_platforms", "territories", "use_classes", "parent_asset_refs",
    "segment_timing_refs", "sfx_asset_refs", "platform_intent", "evidence_refs",
    "post_copy_trace_refs", "source_fact_package_refs", "source_metric_refs",
}

OBJECT_ARRAY_SORT_KEYS = {
    "approved_claims": ("claim_id",),
    "approved_facts": ("fact_id",),
    "approved_explanations": ("explanation_id",),
    "fact_package_bindings": ("ref", "digest"),
    "source_fact_package_bindings": ("ref", "digest"),
    "assets": ("asset_id",),
    "normalized_metrics": ("metric_name", "normalization_version"),
    "platform_intents": ("platform", "target_account_ref", "publish_mode"),
    "gate_results": ("gate_class", "code"),
}


def _assert_canonical_domain(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (str, bool)):
        if isinstance(value, str):
            for char in value:
                cp = ord(char)
                if 0xD800 <= cp <= 0xDFFF:
                    raise ValueError(f"unpaired surrogate forbidden at {path}")
        return
    if isinstance(value, int) and not isinstance(value, bool):
        if abs(value) > SAFE_INT:
            raise ValueError(f"integer outside JavaScript-safe range at {path}")
        return
    if isinstance(value, float):
        raise ValueError(f"floating JSON number forbidden in canonical contracts at {path}; use a decimal string")
    if isinstance(value, list):
        for i, item in enumerate(value):
            _assert_canonical_domain(item, f"{path}[{i}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"non-string object key at {path}")
            _assert_canonical_domain(key, f"{path}.<key>")
            _assert_canonical_domain(item, f"{path}.{key}")
        return
    raise ValueError(f"unsupported JSON value {type(value)!r} at {path}")


def _utf8_key(text: str) -> bytes:
    return text.encode("utf-8")


def _normalize(value: Any, parent_key: str | None = None) -> Any:
    if isinstance(value, dict):
        return {k: _normalize(value[k], k) for k in sorted(value, key=_utf8_key)}
    if isinstance(value, list):
        items = [_normalize(item, None) for item in value]
        if parent_key in SET_ARRAY_KEYS:
            if all(isinstance(item, str) for item in items):
                return sorted(items, key=_utf8_key)
        sort_keys = OBJECT_ARRAY_SORT_KEYS.get(parent_key or "")
        if sort_keys and all(isinstance(item, dict) for item in items):
            def obj_key(item: dict[str, Any]) -> tuple[bytes, ...]:
                return tuple(str(item.get(key, "")).encode("utf-8") for key in sort_keys)
            return sorted(items, key=obj_key)
        return items
    return value


def canonicalize(value: Any) -> bytes:
    _assert_canonical_domain(value)
    normalized = _normalize(value)
    text = json.dumps(normalized, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return text.encode("utf-8")


def semantic_payload(document: dict[str, Any]) -> dict[str, Any]:
    version = document.get("schema_version")
    if version not in DIGEST_FIELDS:
        raise ValueError(f"unsupported schema_version for digest: {version!r}")
    payload = deepcopy(document)
    payload.pop(DIGEST_FIELDS[version], None)
    return payload


def semantic_digest(document: dict[str, Any]) -> str:
    payload = semantic_payload(document)
    return "sha256:" + hashlib.sha256(canonicalize(payload)).hexdigest()


def apply_semantic_digest(document: dict[str, Any]) -> dict[str, Any]:
    version = document["schema_version"]
    field = DIGEST_FIELDS[version]
    out = deepcopy(document)
    out[field] = semantic_digest(out)
    return out
