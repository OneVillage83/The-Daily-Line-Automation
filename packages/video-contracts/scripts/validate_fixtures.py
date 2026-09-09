#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from dlve_contracts.validate import validate_document, validate_scenario


def main() -> int:
    failures = 0
    valid_dir = ROOT / "fixtures" / "valid" / "end-to-end"
    for path in sorted(valid_dir.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_document(doc)
        if errors:
            failures += 1
            print(f"FAIL valid fixture {path.name}")
            for e in errors:
                print(f"  {e.code}: {e.message} @ {e.path}")
        else:
            print(f"PASS valid fixture {path.name}")

    invalid_dir = ROOT / "fixtures" / "invalid"
    for path in sorted(invalid_dir.glob("*.json")):
        fixture = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_document(fixture["document"], verify_digest=fixture.get("verify_digest", True))
        codes = {e.code for e in errors}
        expected = set(fixture["expected_error_codes"])
        if not expected.issubset(codes):
            failures += 1
            print(f"FAIL invalid fixture {path.name}: expected {sorted(expected)}, got {sorted(codes)}")
        else:
            print(f"PASS invalid fixture {path.name}: {sorted(expected)}")

    scenarios_dir = ROOT / "fixtures" / "scenarios"
    for path in sorted(scenarios_dir.glob("*.json")):
        scenario = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_scenario(scenario)
        codes = {e.code for e in errors}
        expected = set(scenario["expected_error_codes"])
        if codes != expected:
            failures += 1
            print(f"FAIL scenario {path.name}: expected exactly {sorted(expected)}, got {sorted(codes)}")
            for e in errors:
                print(f"  {e.code}: {e.message}")
        else:
            print(f"PASS scenario {path.name}: {sorted(expected) if expected else 'no errors'}")
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
