from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from app.config import AppConfig
from app.database import DEFAULT_DB_PATH, get_connection, initialize_database
from app.matcher import MatchResult
from app.vector_search import build_embedding, cosine_similarity


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


@dataclass(frozen=True)
class JobDescriptionRecord:
    id: int
    created_at: str
    title: str
    company: str
    description: str
    similarity: float | None = None


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


def row_to_job_record(row: object, similarity: float | None = None) -> JobDescriptionRecord:
    return JobDescriptionRecord(
        id=row["id"],
        created_at=row["created_at"],
        title=row["title"],
        company=row["company"],
        description=row["description"],
        similarity=similarity,
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


def save_job_description(
    *,
    title: str,
    company: str,
    description: str,
    db_path: Path = DEFAULT_DB_PATH,
) -> JobDescriptionRecord:
    initialize_database(db_path)
    embedding = build_embedding(description)

    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO job_descriptions (
                title,
                company,
                description,
                embedding_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (title, company, description, json.dumps(embedding)),
        )
        record_id = cursor.lastrowid
        row = connection.execute(
            "SELECT * FROM job_descriptions WHERE id = ?",
            (record_id,),
        ).fetchone()

    return row_to_job_record(row)


def list_job_descriptions(
    *, limit: int = 10, db_path: Path = DEFAULT_DB_PATH
) -> list[JobDescriptionRecord]:
    initialize_database(db_path)
    with get_connection(db_path) as connection:
        rows = connection.execute(
            """
            SELECT * FROM job_descriptions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [row_to_job_record(row) for row in rows]


def search_similar_jobs(
    *, query_text: str, limit: int = 5, db_path: Path = DEFAULT_DB_PATH
) -> list[JobDescriptionRecord]:
    initialize_database(db_path)
    query_embedding = build_embedding(query_text)

    with get_connection(db_path) as connection:
        rows = connection.execute("SELECT * FROM job_descriptions").fetchall()

    scored_records = []
    for row in rows:
        job_embedding = json.loads(row["embedding_json"])
        similarity = cosine_similarity(query_embedding, job_embedding)
        scored_records.append(row_to_job_record(row, similarity=round(similarity, 4)))

    return sorted(scored_records, key=lambda record: record.similarity or 0, reverse=True)[
        :limit
    ]
