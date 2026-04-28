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
    assert isinstance(payload["id"], int)
    assert payload["provider"] == "mock"
    assert payload["score"] == 62
    assert payload["missing_skills"] == ["embeddings", "llm", "rag"]
    assert payload["missing_skills_by_category"] == {
        "ai_engineering": ["embeddings", "llm", "rag"]
    }

    detail_response = client.get(f"/history/{payload['id']}")
    detail_payload = detail_response.json()

    assert detail_response.status_code == 200
    assert detail_payload["id"] == payload["id"]
    assert detail_payload["score"] == 62


def test_analyze_endpoint_validates_empty_input() -> None:
    response = client.post(
        "/analyze",
        json={"resume_text": "", "job_description_text": "Python"},
    )

    assert response.status_code == 422


def test_history_endpoint_returns_recent_items() -> None:
    response = client.get("/history?limit=5")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
