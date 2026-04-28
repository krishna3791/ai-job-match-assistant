# AI Job Match Assistant

Portfolio project for moving from data engineering into AI engineering.

GitHub: https://github.com/krishna3791/ai-job-match-assistant

This first version works without paid AI APIs. It compares a resume with a job description using a simple skill-matching engine, then returns:

- Match score
- Readiness level
- Resume and job skills detected
- Skills found in both resume and job description
- Skills missing from the resume
- Missing skills grouped by category
- Resume improvement suggestions
- Personalized learning plan

Later versions will add:

- LLM-based analysis
- FastAPI backend
- SQLite storage
- RAG and vector search
- Frontend UI
- Deployment

## Quick Start

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Run the text report:

```powershell
python scripts/analyze_match.py data/sample_resume.txt data/sample_job_description.txt
```

Run JSON output:

```powershell
python scripts/analyze_match.py data/sample_resume.txt data/sample_job_description.txt --format json
```

Run tests:

```powershell
python -m pytest
```

Run the API server:

```powershell
python -m uvicorn app.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Show safe configuration metadata:

```powershell
python scripts/analyze_match.py data/sample_resume.txt data/sample_job_description.txt --show-config
```

For local secrets, copy `.env.example` to `.env` and edit `.env`. Never commit real API keys.

If `python` is not available on Windows, install Python 3.11+ from https://www.python.org/downloads/windows/ and enable "Add python.exe to PATH" during installation.

## Project Structure

```text
ai-job-match-assistant/
  README.md
  .gitignore
  .env.example
  requirements.txt
  app/
    api.py
    __init__.py
    cli.py
    config.py
    matcher.py
    schemas.py
    services.py
  data/
    sample_resume.txt
    sample_job_description.txt
  tests/
    test_api.py
    test_cli.py
    test_config.py
    test_matcher.py
    test_services.py
  scripts/
    analyze_match.py
```

## Resume Bullet Draft

Built an AI Job Match Assistant to compare resumes against job descriptions, identify skill gaps, generate match scores, and recommend targeted resume improvements. Designed the project as a production-style AI engineering portfolio app with planned LLM, RAG, API, database, evaluation, and deployment layers.
