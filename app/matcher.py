from __future__ import annotations

from dataclasses import dataclass


SKILLS = [
    "python",
    "sql",
    "spark",
    "pyspark",
    "airflow",
    "dbt",
    "snowflake",
    "databricks",
    "aws",
    "azure",
    "gcp",
    "docker",
    "fastapi",
    "api",
    "machine learning",
    "ml",
    "llm",
    "rag",
    "embeddings",
    "vector database",
    "langchain",
    "llamaindex",
    "openai",
    "data pipeline",
    "etl",
    "elt",
    "data warehouse",
    "ci/cd",
    "kafka",
    "streaming",
]


@dataclass(frozen=True)
class MatchResult:
    score: int
    matched_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]


def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def find_skills(text: str) -> set[str]:
    normalized = normalize_text(text)
    return {skill for skill in SKILLS if skill in normalized}


def score_match(resume_skills: set[str], job_skills: set[str]) -> int:
    if not job_skills:
        return 0
    return round((len(resume_skills & job_skills) / len(job_skills)) * 100)


def build_suggestions(missing_skills: list[str]) -> list[str]:
    if not missing_skills:
        return [
            "Your resume already covers the main detected skills. Improve impact by adding measurable outcomes."
        ]

    suggestions = []
    for skill in missing_skills[:5]:
        suggestions.append(
            f"Add a resume bullet that shows hands-on experience with {skill} if you have used it."
        )
    return suggestions


def analyze_match(resume_text: str, job_description_text: str) -> MatchResult:
    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description_text)
    matched_skills = sorted(resume_skills & job_skills)
    missing_skills = sorted(job_skills - resume_skills)

    return MatchResult(
        score=score_match(resume_skills, job_skills),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        suggestions=build_suggestions(missing_skills),
    )
