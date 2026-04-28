from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from app.config import AppConfig
from app.database import DEFAULT_DB_PATH, get_connection, initialize_database
from app.matcher import MatchResult


@dataclass(frozen=True)
class AnalysisRecord:
    id: int
    created_at: str
    provider: str
    model_provider: str
    model_name: str
    score: int
    readiness_level: str
    resume_text: str
    job_description_text: str
    result: dict[str, object]


def match_result_to_dict(result: MatchResult) -> dict[str, object]:
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


def row_to_record(row: object) -> AnalysisRecord:
    return AnalysisRecord(
        id=row["id"],
        created_at=row["created_at"],
        provider=row["provider"],
        model_provider=row["model_provider"],
        model_name=row["model_name"],
        score=row["score"],
        readiness_level=row["readiness_level"],
        resume_text=row["resume_text"],
        job_description_text=row["job_description_text"],
        result=json.loads(row["result_json"]),
    )


def save_analysis_result(
    *,
    resume_text: str,
    job_description_text: str,
    result: MatchResult,
    provider: str,
    config: AppConfig,
    db_path: Path = DEFAULT_DB_PATH,
) -> AnalysisRecord:
    initialize_database(db_path)
    result_payload = match_result_to_dict(result)

    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO analysis_results (
                provider,
                model_provider,
                model_name,
                score,
                readiness_level,
                resume_text,
                job_description_text,
                result_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                provider,
                config.model_provider,
                config.model_name,
                result.score,
                result.readiness_level,
                resume_text,
                job_description_text,
                json.dumps(result_payload),
            ),
        )
        record_id = cursor.lastrowid

        row = connection.execute(
            "SELECT * FROM analysis_results WHERE id = ?",
            (record_id,),
        ).fetchone()

    return row_to_record(row)


def list_analysis_results(
    *, limit: int = 10, db_path: Path = DEFAULT_DB_PATH
) -> list[AnalysisRecord]:
    initialize_database(db_path)
    with get_connection(db_path) as connection:
        rows = connection.execute(
            """
            SELECT * FROM analysis_results
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [row_to_record(row) for row in rows]


def get_analysis_result(
    record_id: int, db_path: Path = DEFAULT_DB_PATH
) -> AnalysisRecord | None:
    initialize_database(db_path)
    with get_connection(db_path) as connection:
        row = connection.execute(
            "SELECT * FROM analysis_results WHERE id = ?",
            (record_id,),
        ).fetchone()

    if row is None:
        return None
    return row_to_record(row)
