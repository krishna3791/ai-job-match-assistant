# Day 8: FastAPI App

## What We Built

Today we added a FastAPI application in `app/api.py`.

FastAPI lets us expose the resume/job analysis as HTTP endpoints, which is the first step toward a frontend or deployed service.

## Command

```powershell
python -m uvicorn app.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Interview Explanation

> I exposed the analysis logic through a FastAPI service so the project can be used by a frontend, automation workflow, or external client.
