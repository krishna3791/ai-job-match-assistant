from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_create_and_search_jobs() -> None:
    create_response = client.post(
        "/jobs",
        json={
            "title": "AI Data Engineer",
            "company": "ExampleCo",
            "description": "Python SQL Spark Airflow RAG embeddings vector database",
        },
    )

    assert create_response.status_code == 200
    assert create_response.json()["title"] == "AI Data Engineer"

    search_response = client.post(
        "/jobs/search",
        json={"query_text": "Python Spark RAG embeddings", "limit": 3},
    )

    assert search_response.status_code == 200
    assert search_response.json()[0]["company"] == "ExampleCo"
    assert search_response.json()[0]["similarity"] > 0
