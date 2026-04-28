# Day 9: `/analyze` Endpoint

## What We Built

Today we added:

```text
POST /analyze
```

The endpoint accepts resume text and job description text, then returns a structured match analysis.

## Example Request

```json
{
  "resume_text": "Python SQL Spark Airflow AWS data pipeline",
  "job_description_text": "Python SQL Spark Airflow AWS LLM RAG embeddings"
}
```

## Interview Explanation

> I built a POST endpoint that accepts unstructured resume and job description text and returns structured skill-gap analysis.
