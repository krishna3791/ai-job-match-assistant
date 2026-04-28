# AI Job Match Assistant

Portfolio project for moving from data engineering into AI engineering.

This first version works without paid AI APIs. It compares a resume with a job description using a simple skill-matching engine, then returns:

- Match score
- Skills found in both resume and job description
- Skills missing from the resume
- Resume improvement suggestions

Later versions will add:

- LLM-based analysis
- FastAPI backend
- SQLite storage
- RAG and vector search
- Frontend UI
- Deployment

## Quick Start

```powershell
python scripts/analyze_match.py data/sample_resume.txt data/sample_job_description.txt
```

If `python` is not available on Windows, install Python 3.11+ from https://www.python.org/downloads/windows/ and enable "Add python.exe to PATH" during installation.

## Project Structure

```text
ai-job-match-assistant/
  README.md
  .gitignore
  .env.example
  requirements.txt
  app/
    __init__.py
    matcher.py
  data/
    sample_resume.txt
    sample_job_description.txt
  scripts/
    analyze_match.py
```

## Resume Bullet Draft

Built an AI Job Match Assistant to compare resumes against job descriptions, identify skill gaps, generate match scores, and recommend targeted resume improvements. Designed the project as a production-style AI engineering portfolio app with planned LLM, RAG, API, database, evaluation, and deployment layers.
