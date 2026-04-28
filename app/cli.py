from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.config import load_config
from app.matcher import MatchResult, analyze_match


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def result_to_dict(result: MatchResult) -> dict[str, object]:
    return {
        "score": result.score,
        "readiness_level": result.readiness_level,
        "resume_skills": result.resume_skills,
        "job_skills": result.job_skills,
        "matched_skills": result.matched_skills,
        "missing_skills": result.missing_skills,
        "missing_skills_by_category": result.missing_skills_by_category,
        "suggestions": result.suggestions,
        "learning_plan": result.learning_plan,
    }


def print_text_report(result: MatchResult) -> None:
    print("AI Job Match Assistant")
    print("=" * 24)
    print(f"Score: {result.score}/100")
    print(f"Readiness: {result.readiness_level}")

    print("\nMatched Skills")
    for skill in result.matched_skills:
        print(f"- {skill}")

    print("\nMissing Skills By Category")
    if not result.missing_skills_by_category:
        print("- No major missing skills detected.")
    for category, skills in result.missing_skills_by_category.items():
        print(f"- {category}: {', '.join(skills)}")

    print("\nLearning Plan")
    for item in result.learning_plan:
        print(f"- {item}")

    print("\nResume Suggestions")
    for suggestion in result.suggestions:
        print(f"- {suggestion}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-job-match",
        description="Compare a resume against a job description.",
    )
    parser.add_argument("resume_file", type=Path, help="Path to a resume text file.")
    parser.add_argument(
        "job_description_file", type=Path, help="Path to a job description text file."
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format. Use json for APIs and automation.",
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Show safe config metadata without printing secret values.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    config = load_config()

    if args.show_config:
        print(
            json.dumps(
                {
                    "app_env": config.app_env,
                    "model_provider": config.model_provider,
                    "model_name": config.model_name,
                    "has_openai_api_key": config.has_openai_api_key,
                },
                indent=2,
            )
        )
        return

    resume_text = read_text_file(args.resume_file)
    job_description_text = read_text_file(args.job_description_file)
    result = analyze_match(resume_text, job_description_text)

    if args.format == "json":
        print(json.dumps(result_to_dict(result), indent=2))
        return

    print_text_report(result)


if __name__ == "__main__":
    main()
