from app.cli import result_to_dict
from app.matcher import analyze_match


def test_result_to_dict_includes_api_friendly_fields() -> None:
    result = analyze_match(
        "Python and SQL data pipeline experience.",
        "Python, SQL, data pipeline, LLM, and RAG experience required.",
    )

    payload = result_to_dict(result)

    assert payload["score"] == 60
    assert payload["readiness_level"] == "good match with a few gaps"
    assert payload["matched_skills"] == ["data pipeline", "python", "sql"]
    assert payload["missing_skills"] == ["llm", "rag"]
    assert "learning_plan" in payload
    assert "suggestions" in payload
