# Day 1: Project Setup and First Working Version

## What We Built

We created the first version of an AI Job Match Assistant.

Right now it does not call a paid AI model. Instead, it uses a simple skill-matching engine so we can confirm the project works end to end before adding LLMs.

## Why This Matters

In real AI engineering, the model is only one part of the system. A useful AI product also needs:

- Clean inputs
- Clear business logic
- Reliable code structure
- Repeatable execution
- Good error handling
- Later, APIs, databases, evaluation, and deployment

Starting with a simple working version helps us avoid building everything around an API key before we understand the application flow.

## Files Created

### `README.md`

Explains what the project is, how to run it, and what we will add later.

### `.gitignore`

Tells Git which files not to track, such as virtual environments, cache files, and secret `.env` files.

### `.env.example`

Shows which environment variables the project expects later. This file is safe to commit because it does not contain real secrets.

### `requirements.txt`

Lists Python packages for the project. Day 1 does not need external packages yet.

### `app/matcher.py`

Contains the core matching logic:

- Normalize text
- Detect known skills
- Compare resume skills against job description skills
- Calculate match score
- Suggest improvements

### `scripts/analyze_match.py`

Command-line script that reads two text files:

- Resume file
- Job description file

Then it prints the result as JSON.

### `data/sample_resume.txt`

Sample resume text for testing.

### `data/sample_job_description.txt`

Sample AI job description for testing.

## Important Concepts

### Resume Text

The resume is treated as plain text. Later, we can add support for PDF and DOCX resumes.

### Job Description Text

The job description is also plain text. Later, we can store many job descriptions and compare them.

### Skill Matching

The first version checks whether known skill words appear in the resume and job description.

Example:

If the job description mentions `Python`, `SQL`, and `RAG`, but the resume only mentions `Python` and `SQL`, then `RAG` becomes a missing skill.

### Match Score

The score is:

```text
matched job skills / total detected job skills * 100
```

This is not perfect yet, but it gives us a simple baseline.

### JSON Output

The script prints JSON because APIs and frontend apps can easily consume structured data.

## Command We Ran

```powershell
python scripts/analyze_match.py data/sample_resume.txt data/sample_job_description.txt
```

In this Codex session, Python was not on your system PATH, so we ran the script with Codex's bundled Python.

## Your Local Python Fix

Your terminal did not recognize:

```powershell
python --version
py --version
```

That means Python is probably not installed correctly or not added to PATH.

To fix it:

1. Download Python 3.11+ from https://www.python.org/downloads/windows/
2. During installation, check **Add python.exe to PATH**.
3. Reopen Cursor or PowerShell.
4. Run:

```powershell
python --version
```

You should see something like:

```text
Python 3.11.x
```

## What We Learned

Today we learned that an AI project should start with a working application flow:

1. Input resume
2. Input job description
3. Analyze both
4. Return structured output

Tomorrow we will make this cleaner and more useful by adding better output formatting and preparing for real LLM analysis.
