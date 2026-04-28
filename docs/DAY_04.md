# Day 4: Automated Tests

## What We Built

Today we added automated tests with `pytest`.

Tests help us prove that the project works without manually checking every result each time we change code.

## Why Tests Matter

As this project grows, we will add:

- LLM calls
- API endpoints
- Database storage
- RAG and embeddings
- Frontend integration

Without tests, every change becomes risky. With tests, we can quickly check whether the core behavior still works.

## New Dependency

We added this package to `requirements.txt`:

```text
pytest==8.3.4
```

`pytest` is a popular Python testing framework.

## New Folder: `tests/`

We created:

```text
tests/
  test_matcher.py
  test_cli.py
```

The `tests` folder is where automated tests live.

## What We Tested

### Skill Detection

We tested that the app detects skills like:

- Python
- SQL
- Airflow
- RAG

The test also confirms that uppercase text still works.

### Match Analysis

We tested that the app returns:

- Correct score
- Correct readiness level
- Correct matched skills
- Correct missing skills
- Correct missing skill category

### Empty Job Skill Case

We tested a job description that has no recognized skills.

This matters because real user input can be messy. Good software handles weak input without crashing.

### CLI Payload Shape

We tested that the JSON-friendly output includes the fields future APIs and frontends will need.

## Command To Run

Inside the activated virtual environment:

```powershell
python -m pytest
```

If the tests pass, you should see output showing all tests passed.

## Interview Explanation

You can explain Day 4 like this:

> I added automated tests with pytest to validate the skill extraction, match scoring, readiness labels, missing skill grouping, and API-friendly output payload. This gives the project a safety net before adding LLM calls, RAG, and database features.

## Next Step

Next we will improve the app configuration and prepare for a real LLM provider without hardcoding secrets.
