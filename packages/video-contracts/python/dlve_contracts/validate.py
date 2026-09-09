from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from .canonical import DIGEST_FIELDS, semantic_digest

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = PACKAGE_ROOT / "schemas"
CATALOG_PATH = PACKAGE_ROOT / "schema-catalog.json"

REQUIRED_QC_GATES = {
    "contract", "fact", "asset_rights", "asset_integrity", "layout", "safe_zone",
    "text_overflow", "captions", "audio", "render_probe", "duration_profile",
    "disclaimer", "metadata", "publication_package",
}

@dataclass(frozen=True)
class ContractValidationError:
    code: str
    message: str
    path: str = "$"


def _parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return dt.astimezone(timezone.utc)


def _load_schema_registry() -> tuple[dict[str, Any], Registry]:
    schemas: dict[str, Any] = {}
    registry = Registry()
    for path in SCHEMA_DIR.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas[path.name] = schema
        if "$id" in schema:
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return schemas, registry


def _catalog() -> dict[str, dict[str, str | None]]:
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return {row["schema_version"]: row for row in data["schemas"]}


def validate_document(document: dict[str, Any], *, verify_digest: bool = True) -> list[ContractValidationError]:
    schemas, registry = _load_schema_registry()
    catalog = _catalog()
    version = document.get("schema_version")
    if version not in catalog:
        return [ContractValidationError("SCHEMA_VERSION_UNSUPPORTED", f"unsupported schema_version {version!r}")]
    schema = schemas[catalog[version]["filename"]]
    validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    errors: list[ContractValidationError] = []
    for error in sorted(validator.iter_errors(document), key=lambda e: list(e.absolute_path)):
        path = "$" + "".join(f"[{i}]" if isinstance(i, int) else f".{i}" for i in error.absolute_path)
        errors.append(ContractValidationError("JSON_SCHEMA", error.message, path))
    if errors:
        return errors
    if verify_digest:
        field = DIGEST_FIELDS[version]
        expected = semantic_digest(document)
        if document.get(field) != expected:
            errors.append(ContractValidationError("DIGEST_MISMATCH", f"{field} does not match canonical semantic digest", f"$.{field}"))
    errors.extend(_semantic_checks(document))
    return errors


def _duplicates(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    dup: set[str] = set()
    for value in values:
        if value in seen:
            dup.add(value)
        seen.add(value)
    return dup


def _semantic_checks(doc: dict[str, Any]) -> list[ContractValidationError]:
    v = doc["schema_version"]
    out: list[ContractValidationError] = []
    if v == "publishable-fact-package.v1":
        if _parse_time(doc["valid_from"]) >= _parse_time(doc["expires_at"]):
            out.append(ContractValidationError("INVALID_VALIDITY_WINDOW", "valid_from must be before expires_at"))
        groups = [("fact", doc["approved_facts"], "fact_id"), ("claim", doc["approved_claims"], "claim_id"), ("explanation", doc["approved_explanations"], "explanation_id")]
        for name, items, key in groups:
            for duplicate in _duplicates(item[key] for item in items):
                out.append(ContractValidationError("DUPLICATE_ID", f"duplicate {name} id {duplicate}"))
        fact_ids = {f["fact_id"] for f in doc["approved_facts"]}
        for claim in doc["approved_claims"]:
            missing = set(claim["fact_refs"]) - fact_ids
            if missing:
                out.append(ContractValidationError("UNRESOLVED_FACT_REF", f"claim {claim['claim_id']} references missing facts {sorted(missing)}"))
        for expl in doc["approved_explanations"]:
            missing = set(expl["supporting_fact_refs"]) - fact_ids
            if missing:
                out.append(ContractValidationError("UNRESOLVED_FACT_REF", f"explanation {expl['explanation_id']} references missing facts {sorted(missing)}"))
    elif v == "content-candidate.v1":
        if doc["recommended_duration_band"]["min_ms"] > doc["recommended_duration_band"]["max_ms"]:
            out.append(ContractValidationError("INVALID_DURATION_BAND", "min_ms cannot exceed max_ms"))
        refs = set(doc["fact_package_refs"])
        bound = {x["ref"] for x in doc["fact_package_bindings"]}
        if refs != bound:
            out.append(ContractValidationError("PACKAGE_BINDING_MISMATCH", "fact_package_refs and fact_package_bindings must identify the same packages"))
    elif v == "creative-plan.v1":
        positions = [x["position"] for x in doc["scene_plan"]]
        if len(set(positions)) != len(positions):
            out.append(ContractValidationError("DUPLICATE_SCENE_POSITION", "scene positions must be unique"))
        scene_ids = [x["scene_id"] for x in doc["scene_plan"]]
        if _duplicates(scene_ids):
            out.append(ContractValidationError("DUPLICATE_ID", "scene_id values must be unique"))
    elif v == "script-package.v1":
        for segment in doc["segments"]:
            factual_refs = segment["claim_refs"] or segment["fact_refs"] or segment["explanation_refs"]
            if not segment.get("non_factual_language", False) and not factual_refs:
                out.append(ContractValidationError("UNTRACED_FACTUAL_SEGMENT", f"segment {segment['segment_id']} has no fact/claim/explanation trace"))
            for token in segment["protected_tokens"]:
                if token["render_value"] not in segment["text"]:
                    out.append(ContractValidationError("PROTECTED_TOKEN_MISMATCH", f"segment {segment['segment_id']} does not contain protected render value {token['render_value']!r}"))
    elif v == "fact-integrity-report.v1":
        if doc["status"] == "PASS":
            if doc["unsupported_claims"] or doc["missing_required_claims"] or doc["protected_token_mismatches"] or doc["expired_fact_refs"] or any(c["status"] != "PASS" for c in doc["checks"]):
                out.append(ContractValidationError("FALSE_PASS", "PASS fact-integrity report contains failing evidence"))
    elif v == "asset-manifest.v1":
        for asset in doc["assets"]:
            if asset["policy_status"] == "PASS" and (not asset["allowed_platforms"] or not asset["territories"] or not asset["use_classes"]):
                out.append(ContractValidationError("INCOMPLETE_RIGHTS_SCOPE", f"asset {asset['asset_id']} has PASS policy without complete use scope"))
            if asset["source_class"] == "generated" and asset["documentary_status"] == "authentic_documentary":
                out.append(ContractValidationError("GENERATED_DOCUMENTARY_PROHIBITED", f"generated asset {asset['asset_id']} cannot be authentic documentary evidence"))
            if asset["source_class"] == "generated" and asset["generated_metadata"] is None:
                out.append(ContractValidationError("MISSING_GENERATION_PROVENANCE", f"generated asset {asset['asset_id']} lacks generated_metadata"))
    elif v == "caption-package.v1":
        last_start = -1
        for cue in doc["cues"]:
            if cue["end_ms"] <= cue["start_ms"]:
                out.append(ContractValidationError("INVALID_CAPTION_WINDOW", f"cue {cue['cue_id']} end_ms must exceed start_ms"))
            if cue["start_ms"] < last_start:
                out.append(ContractValidationError("CAPTION_ORDER", "caption cues must be ordered by start_ms"))
            last_start = cue["start_ms"]
    elif v == "video-render-spec.v1":
        rp = doc["render_profile"]
        if rp["min_duration_ms"] > rp["max_duration_ms"]:
            out.append(ContractValidationError("INVALID_DURATION_PROFILE", "min_duration_ms cannot exceed max_duration_ms"))
        if (doc["voice_package_ref"] is None) != (doc["voice_package_digest"] is None):
            out.append(ContractValidationError("VOICE_BINDING_MISMATCH", "voice reference and digest must both be null or both be populated"))
    elif v == "render-manifest.v1":
        if _parse_time(doc["render_started_at"]) > _parse_time(doc["render_finished_at"]):
            out.append(ContractValidationError("INVALID_RENDER_TIMING", "render_started_at cannot be after render_finished_at"))
    elif v == "video-qc-report.v1":
        gate_classes = {g["gate_class"] for g in doc["gate_results"]}
        if doc["status"] == "PASS":
            missing = REQUIRED_QC_GATES - gate_classes
            if missing:
                out.append(ContractValidationError("QC_GATE_MISSING", f"PASS report missing required gates {sorted(missing)}"))
            if any(g["status"] != "PASS" for g in doc["gate_results"]):
                out.append(ContractValidationError("FALSE_PASS", "PASS QC report contains non-PASS gate"))
    elif v == "video-publication-package.v1":
        for intent in doc["platform_intents"]:
            window = intent["scheduled_window"]
            if _parse_time(window["not_before"]) > _parse_time(window["not_after"]):
                out.append(ContractValidationError("INVALID_SCHEDULE_WINDOW", "not_before cannot be after not_after"))
            if _parse_time(window["not_after"]) > _parse_time(doc["content_valid_until"]):
                out.append(ContractValidationError("SCHEDULE_AFTER_CONTENT_EXPIRY", "scheduled window extends after content_valid_until"))
        refs = set(doc["source_fact_package_refs"])
        bound = {x["ref"] for x in doc["source_fact_package_bindings"]}
        if refs != bound:
            out.append(ContractValidationError("PACKAGE_BINDING_MISMATCH", "source fact refs and bindings differ"))
    return out


def validate_scenario(scenario: dict[str, Any]) -> list[ContractValidationError]:
    docs = scenario["documents"]
    out: list[ContractValidationError] = []
    for name, doc in docs.items():
        for err in validate_document(doc):
            out.append(ContractValidationError(err.code, f"{name}: {err.message}", err.path))
    if out:
        return out

    as_of = _parse_time(scenario["as_of"])
    packages = [d for d in docs.values() if d.get("schema_version") == "publishable-fact-package.v1"]
    for package in packages:
        if as_of >= _parse_time(package["expires_at"]):
            out.append(ContractValidationError("PACKAGE_EXPIRED", f"package {package['package_id']} expired before scenario as_of"))
        for fact in package["approved_facts"]:
            if as_of >= _parse_time(fact["valid_until"]):
                out.append(ContractValidationError("FACT_EXPIRED", f"fact {fact['fact_id']} expired before scenario as_of"))

    # Fail closed on unresolved protected-value conflicts across composite source packages.
    by_conflict: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = {}
    for package in packages:
        for fact in package["approved_facts"]:
            if fact.get("conflict_key"):
                by_conflict.setdefault(fact["conflict_key"], []).append((package, fact))
    for key, entries in by_conflict.items():
        values = {fact["formatted_value"] for _, fact in entries}
        if len(values) > 1:
            package_ids = {p["package_id"] for p, _ in entries}
            has_declared_supersession = any(package_ids.intersection(set(p.get("supersedes_package_refs", []))) for p, _ in entries)
            if not has_declared_supersession:
                out.append(ContractValidationError("UNRESOLVED_SOURCE_CONFLICT", f"conflict_key {key!r} has values {sorted(values)} without declared supersession"))

    publication = next((d for d in docs.values() if d.get("schema_version") == "video-publication-package.v1"), None)
    qc = next((d for d in docs.values() if d.get("schema_version") == "video-qc-report.v1"), None)
    assets = next((d for d in docs.values() if d.get("schema_version") == "asset-manifest.v1"), None)
    if publication:
        if qc and qc["status"] != "PASS":
            out.append(ContractValidationError("PUBLICATION_WITHOUT_QC_PASS", "publication package references non-PASS QC"))
        controlling_times: list[datetime] = []
        for package in packages:
            controlling_times.append(_parse_time(package["expires_at"]))
            controlling_times.extend(_parse_time(x["valid_until"]) for x in package["approved_facts"])
            controlling_times.extend(_parse_time(x["valid_until"]) for x in package["approved_claims"])
            controlling_times.extend(_parse_time(x["valid_until"]) for x in package["approved_explanations"])
        if assets:
            controlling_times.extend(_parse_time(a["expiry"]) for a in assets["assets"] if a["expiry"] is not None)
            targets = {i["platform"] for i in publication["platform_intents"]}
            for asset in assets["assets"]:
                missing = targets - set(asset["allowed_platforms"])
                if missing:
                    out.append(ContractValidationError("ASSET_RIGHTS_PLATFORM_MISMATCH", f"asset {asset['asset_id']} not cleared for {sorted(missing)}"))
                if asset["policy_status"] != "PASS":
                    out.append(ContractValidationError("ASSET_RIGHTS_NOT_PASS", f"asset {asset['asset_id']} policy_status={asset['policy_status']}"))
        if controlling_times:
            strictest = min(controlling_times)
            if _parse_time(publication["content_valid_until"]) > strictest:
                out.append(ContractValidationError("CONTENT_VALIDITY_TOO_LATE", "content_valid_until exceeds strictest source/rights validity bound"))
        if as_of >= _parse_time(publication["content_valid_until"]):
            out.append(ContractValidationError("PUBLICATION_PACKAGE_EXPIRED", "publication package is stale at scenario as_of"))
    return out
