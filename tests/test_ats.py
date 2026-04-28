from app.ats import calculate_ats_report


def test_calculate_ats_report_scores_resume_quality() -> None:
    report = calculate_ats_report(
        resume_text="""
        Krishna
        krishna@example.com
        555-555-1212
        Summary
        Skills
        Python SQL Spark Airflow AWS
        Experience
        Built data pipelines and improved reliability by 20%.
        Education
        """,
        job_description_text="Python SQL Spark Airflow AWS LLM RAG",
    )

    assert report.score >= 70
    assert report.strengths
    assert isinstance(report.recommendations, list)
