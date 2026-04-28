from app.matcher import analyze_match, find_skills, readiness_level


def test_find_skills_detects_known_skills_case_insensitively() -> None:
    text = "Built PYTHON and SQL pipelines with Airflow for RAG analytics."

    skills = find_skills(text)

    assert "python" in skills
    assert "sql" in skills
    assert "airflow" in skills
    assert "rag" in skills


def test_analyze_match_returns_score_and_missing_ai_skills() -> None:
    resume = "Data Engineer with Python, SQL, Spark, Airflow, and AWS experience."
    job = "Need Python, SQL, Spark, Airflow, AWS, LLM, RAG, and embeddings."

    result = analyze_match(resume, job)

    assert result.score == 62
    assert result.readiness_level == "good match with a few gaps"
    assert result.matched_skills == ["airflow", "aws", "python", "spark", "sql"]
    assert result.missing_skills == ["embeddings", "llm", "rag"]
    assert result.missing_skills_by_category == {
        "ai_engineering": ["embeddings", "llm", "rag"]
    }


def test_analyze_match_handles_job_with_no_detected_skills() -> None:
    result = analyze_match("Python and SQL experience.", "Friendly team player needed.")

    assert result.score == 0
    assert result.job_skills == []
    assert result.matched_skills == []
    assert result.missing_skills == []


def test_readiness_level_boundaries() -> None:
    assert readiness_level(80) == "strong match"
    assert readiness_level(60) == "good match with a few gaps"
    assert readiness_level(40) == "partial match with clear learning targets"
    assert readiness_level(39) == "early match, needs focused preparation"
