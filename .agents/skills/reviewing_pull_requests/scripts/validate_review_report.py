#!/usr/bin/env python3
"""
Script determinista para validar la estructura del reporte de PR Readiness Review.
"""
import sys
from pathlib import Path

REQUIRED_STRINGS = [
    "# PR Readiness Review",
    "## Review Context",
    "## Requirements / Acceptance Criteria Reviewed",
    "## Test Evidence",
    "## MUST FIX",
    "## SHOULD FIX",
    "## OPTIONAL",
    "## Final Review Summary",
    "Human decision required:",
]


def validate_report(report_path: str) -> bool:
    path = Path(report_path)
    if not path.exists():
        print(f"INVALID: File '{report_path}' does not exist.")
        return False

    content = path.read_text()
    missing = [s for s in REQUIRED_STRINGS if s not in content]

    if missing:
        print("INVALID: Missing required sections or strings:")
        for m in missing:
            print(f" - {m}")
        return False

    print("VALID: PR readiness review structure is complete.")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_review_report.py <path_to_report.md>")
        sys.exit(1)

    is_valid = validate_report(sys.argv[1])
    sys.exit(0 if is_valid else 1)