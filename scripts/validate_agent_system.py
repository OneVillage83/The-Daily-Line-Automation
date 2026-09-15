from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
STATE = ROOT / "docs" / "agent-system" / "state" / "program_state.json"

REQUIRED_MANIFEST = {
    "schema_version",
    "id",
    "version",
    "name",
    "role",
    "purpose",
    "instructions_file",
    "authority",
    "capabilities",
    "prohibited",
    "evaluation_gates",
    "runtime",
}

REQUIRED_STATE = {
    "schema_version",
    "updated_at",
    "authority",
    "current_phase",
    "current_task",
    "macro_sequence",
    "repositories",
    "policy",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    raise AssertionError("unreachable")


def validate_manifest(path: Path) -> None:
    data = load_json(path)
    missing = REQUIRED_MANIFEST - data.keys()
    if missing:
        fail(f"{path.relative_to(ROOT)} missing keys: {sorted(missing)}")
    if data["schema_version"] != "1.0":
        fail(f"{path.relative_to(ROOT)} unsupported schema_version")
    instructions = ROOT / data["instructions_file"]
    if not instructions.is_file():
        fail(f"{path.relative_to(ROOT)} points to missing instructions: {data['instructions_file']}")
    runtime = data.get("runtime", {})
    if runtime.get("status") not in {"not_published", "candidate", "staging", "production", "retired"}:
        fail(f"{path.relative_to(ROOT)} invalid runtime.status")
    if runtime.get("provider_agent_id") and runtime.get("status") == "not_published":
        fail(f"{path.relative_to(ROOT)} has provider_agent_id while not_published")


def main() -> int:
    state = load_json(STATE)
    missing = REQUIRED_STATE - state.keys()
    if missing:
        fail(f"program_state.json missing keys: {sorted(missing)}")
    if state["authority"] != "program-coordination-only":
        fail("program state authority must remain program-coordination-only")

    manifests = sorted(AGENTS_DIR.glob("*/agent.json"))
    if not manifests:
        fail("no agent manifests found")
    for manifest in manifests:
        validate_manifest(manifest)

    skill_files = sorted((ROOT / "codex" / "skills").glob("*/SKILL.md"))
    if len(skill_files) < 3:
        fail("expected at least three Codex skill bundles")

    print(f"DLADS validation PASS: {len(manifests)} agent manifests, {len(skill_files)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
