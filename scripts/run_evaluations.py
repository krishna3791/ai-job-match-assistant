from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.evaluation import run_evaluations  # noqa: E402


def main() -> None:
    results = run_evaluations()
    payload = [
        {
            "name": result.name,
            "passed": result.passed,
            "score": result.score,
            "expected_missing_skills": result.expected_missing_skills,
            "actual_missing_skills": result.actual_missing_skills,
        }
        for result in results
    ]
    print(json.dumps(payload, indent=2))

    if not all(result.passed for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
