from pathlib import Path

from app.config import AppConfig
from app.matcher import analyze_match
from app.repository import (
    get_analysis_result,
    list_analysis_results,
    save_analysis_result,
)


TMP_DIR = Path(__file__).parent / ".tmp"


def test_save_and_read_analysis_result() -> None:
    TMP_DIR.mkdir(exist_ok=True)
    db_path = TMP_DIR / "history.db"
    if db_path.exists():
        db_path.unlink()

    result = analyze_match(
        "Python SQL Spark",
        "Python SQL Spark LLM RAG",
    )
    config = AppConfig(
        app_env="test",
        model_provider="mock",
        model_name="mock-skill-matcher",
        openai_api_key=None,
    )

    saved = save_analysis_result(
        resume_text="Python SQL Spark",
        job_description_text="Python SQL Spark LLM RAG",
        result=result,
        provider="mock",
        config=config,
        db_path=db_path,
    )
    found = get_analysis_result(saved.id, db_path=db_path)
    history = list_analysis_results(limit=5, db_path=db_path)

    assert found is not None
    assert found.id == saved.id
    assert found.result["missing_skills"] == ["llm", "rag"]
    assert history[0].id == saved.id
