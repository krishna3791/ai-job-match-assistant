from __future__ import annotations

from dataclasses import dataclass


SKILL_CATEGORIES = {
    "programming": ["python", "sql", "api", "fastapi"],
    "data_engineering": [
        "spark",
        "pyspark",
        "airflow",
        "dbt",
        "data pipeline",
        "etl",
        "elt",
        "data warehouse",
        "kafka",
        "streaming",
    ],
    "cloud_and_platform": [
        "aws",
        "azure",
        "gcp",
        "snowflake",
        "databricks",
        "docker",
        "ci/cd",
    ],
    "ai_engineering": [
        "machine learning",
        "ml",
        "llm",
        "rag",
        "embeddings",
        "vector database",
        "langchain",
        "llamaindex",
        "openai",
    ],
}

SKILLS = sorted({skill for skills in SKILL_CATEGORIES.values() for skill in skills})


@dataclass(frozen=True)
class MatchResult:
    score: int
    readiness_level: str
    resume_skills: list[str]
    job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    missing_skills_by_category: dict[str, list[str]]
    suggestions: list[str]
    learning_plan: list[str]


def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def find_skills(text: str) -> set[str]:
    normalized = normalize_text(text)
    return {skill for skill in SKILLS if skill in normalized}


def score_match(resume_skills: set[str], job_skills: set[str]) -> int:
    if not job_skills:
        return 0
    return round((len(resume_skills & job_skills) / len(job_skills)) * 100)


def readiness_level(score: int) -> str:
    if score >= 80:
        return "strong match"
    if score >= 60:
        return "good match with a few gaps"
    if score >= 40:
        return "partial match with clear learning targets"
    return "early match, needs focused preparation"


def group_missing_skills(missing_skills: set[str]) -> dict[str, list[str]]:
    grouped = {}
    for category, skills in SKILL_CATEGORIES.items():
        category_missing = sorted(missing_skills & set(skills))
        if category_missing:
            grouped[category] = category_missing
    return grouped


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


def build_learning_plan(missing_skills: list[str]) -> list[str]:
    plan = []
    priority_order = [
        "llm",
        "rag",
        "embeddings",
        "vector database",
        "fastapi",
        "docker",
        "ci/cd",
    ]

    for skill in priority_order:
        if skill in missing_skills:
            plan.append(f"Build a small hands-on feature that uses {skill}.")

    if not plan:
        plan.append("Add measurable project outcomes and prepare interview explanations.")
    return plan[:5]


def analyze_match(resume_text: str, job_description_text: str) -> MatchResult:
    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description_text)
    matched_skills = sorted(resume_skills & job_skills)
    missing_skill_set = job_skills - resume_skills
    missing_skills = sorted(missing_skill_set)
    score = score_match(resume_skills, job_skills)

    return MatchResult(
        score=score,
        readiness_level=readiness_level(score),
        resume_skills=sorted(resume_skills),
        job_skills=sorted(job_skills),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        missing_skills_by_category=group_missing_skills(missing_skill_set),
        suggestions=build_suggestions(missing_skills),
        learning_plan=build_learning_plan(missing_skills),
    )
