# Day 10: Typed API Schemas

## What We Built

Today we added typed request and response models in `app/schemas.py`.

These schemas define:

- `AnalyzeRequest`
- `AnalyzeResponse`
- `HealthResponse`

## Why This Matters

Typed schemas make APIs easier to test, document, and integrate.

FastAPI uses these models to generate interactive docs automatically.

## Interview Explanation

> I added typed Pydantic schemas for API requests and responses, giving the service validation, documentation, and a stable contract for future frontend integration.
