from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.matcher import analyze_match  # noqa: E402


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare a resume against a job description."
    )
    parser.add_argument("resume_file", type=Path)
    parser.add_argument("job_description_file", type=Path)
    args = parser.parse_args()

    resume_text = read_text_file(args.resume_file)
    job_description_text = read_text_file(args.job_description_file)
    result = analyze_match(resume_text, job_description_text)

    print(
        json.dumps(
            {
                "score": result.score,
                "matched_skills": result.matched_skills,
                "missing_skills": result.missing_skills,
                "suggestions": result.suggestions,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
