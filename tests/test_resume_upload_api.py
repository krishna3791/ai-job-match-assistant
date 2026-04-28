from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_resume_analyze_upload_endpoint() -> None:
    response = client.post(
        "/resume/analyze",
        files={"resume_file": ("resume.txt", b"Python SQL Spark Airflow AWS", "text/plain")},
        data={"job_description_text": "Python SQL Spark Airflow AWS LLM RAG"},
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload["filename"] == "resume.txt"
    assert payload["analysis"]["score"] == 71
    assert payload["ats"]["score"] >= 0
    assert "llm" in payload["analysis"]["missing_skills"]


def test_resume_rewrite_upload_endpoint_returns_download() -> None:
    response = client.post(
        "/resume/rewrite",
        files={"resume_file": ("resume.txt", b"Python SQL Spark", "text/plain")},
        data={"job_description_text": "Python SQL Spark LLM"},
    )

    assert response.status_code == 200
    assert response.headers["content-disposition"] == 'attachment; filename="targeted_resume_rewrite.txt"'
    assert b"Targeted Resume Rewrite Draft" in response.content
