from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_health_endpoint_returns_safe_config_metadata() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app_env": "development",
        "model_provider": "mock",
        "model_name": "mock-skill-matcher",
        "has_openai_api_key": False,
    }


def test_analyze_endpoint_returns_match_result() -> None:
    response = client.post(
        "/analyze",
        json={
            "resume_text": "Python SQL Spark Airflow AWS data pipeline",
            "job_description_text": "Python SQL Spark Airflow AWS LLM RAG embeddings",
        },
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload["provider"] == "mock"
    assert payload["score"] == 62
    assert payload["missing_skills"] == ["embeddings", "llm", "rag"]
    assert payload["missing_skills_by_category"] == {
        "ai_engineering": ["embeddings", "llm", "rag"]
    }


def test_analyze_endpoint_validates_empty_input() -> None:
    response = client.post(
        "/analyze",
        json={"resume_text": "", "job_description_text": "Python"},
    )

    assert response.status_code == 422
