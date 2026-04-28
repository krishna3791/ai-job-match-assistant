# Interview Guide

## 30-Second Explanation

I built an AI Job Match Assistant to demonstrate my transition from data engineering into AI engineering. It compares resumes against job descriptions, returns structured skill-gap analysis, stores results in SQLite, exposes a FastAPI backend, and includes a provider layer for both deterministic local analysis and future OpenAI structured-output analysis.

## Why I Built It

I wanted a project that connects directly to my career transition. My background is data engineering, so I focused on the parts of AI systems where data engineers are strong: clean inputs, APIs, persistence, testing, retrieval, and reliable structured outputs.

## Technical Decisions

- Started with a deterministic mock analyzer to keep development testable and cost-free.
- Added FastAPI so the logic can be consumed by a frontend or external client.
- Used Pydantic schemas to define API contracts.
- Added SQLite to persist analysis history.
- Added local vector search to demonstrate retrieval and similarity search concepts.
- Added an OpenAI provider path using structured outputs but kept mock as default.

## What I Would Improve Next

- Add real OpenAI API execution with retry/error handling.
- Add document upload support for PDF and DOCX resumes.
- Add a lightweight frontend.
- Replace local vector search with pgvector or a managed vector database.
- Add evaluation metrics for LLM output quality.
