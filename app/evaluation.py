from __future__ import annotations

from dataclasses import dataclass

from app.matcher import analyze_match


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    resume_text: str
    job_description_text: str
    expected_missing_skills: list[str]
    minimum_score: int


@dataclass(frozen=True)
class EvaluationResult:
    name: str
    passed: bool
    score: int
    expected_missing_skills: list[str]
    actual_missing_skills: list[str]


EVALUATION_CASES = [
    EvaluationCase(
        name="data-engineer-to-ai-data-engineer",
        resume_text="Python SQL Spark Airflow AWS data pipeline ETL Snowflake",
        job_description_text="Python SQL Spark Airflow AWS LLM RAG embeddings vector database",
        expected_missing_skills=["embeddings", "llm", "rag", "vector database"],
        minimum_score=45,
    ),
    EvaluationCase(
        name="strong-ai-data-match",
        resume_text="Python SQL Spark Airflow AWS LLM RAG embeddings vector database FastAPI",
        job_description_text="Python SQL Spark Airflow AWS LLM RAG embeddings vector database FastAPI",
        expected_missing_skills=[],
        minimum_score=90,
    ),
]


def run_evaluations() -> list[EvaluationResult]:
    results = []
    for case in EVALUATION_CASES:
        analysis = analyze_match(case.resume_text, case.job_description_text)
        missing_matches = analysis.missing_skills == case.expected_missing_skills
        score_matches = analysis.score >= case.minimum_score
        results.append(
            EvaluationResult(
                name=case.name,
                passed=missing_matches and score_matches,
                score=analysis.score,
                expected_missing_skills=case.expected_missing_skills,
                actual_missing_skills=analysis.missing_skills,
            )
        )
    return results
