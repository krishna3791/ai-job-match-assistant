# Day 5: Configuration and `.env` Files

## What We Built

Today we added safe configuration handling.

The project can now read settings from:

- Environment variables
- A local `.env` file
- Default values when no config is provided

## Why This Matters

When we add a real LLM provider, we will need API keys.

API keys must never be hardcoded in Python files and must never be committed to GitHub.

Instead, we use a local `.env` file.

## Important Files

### `.env.example`

This file is safe to commit.

It shows other developers which settings the project expects:

```text
APP_ENV=development
MODEL_PROVIDER=mock
MODEL_NAME=mock-skill-matcher
OPENAI_API_KEY=
```

### `.env`

This file is private and local.

It is ignored by Git because `.gitignore` already includes:

```text
.env
```

That means real secrets stay on your machine and do not go to GitHub.

### `app/config.py`

This file loads configuration safely.

It also exposes `has_openai_api_key`, which tells the app whether a key exists without printing the actual key.

## Command To Check Config

Run:

```powershell
python scripts\analyze_match.py data\sample_resume.txt data\sample_job_description.txt --show-config
```

Expected output:

```json
{
  "app_env": "development",
  "model_provider": "mock",
  "model_name": "mock-skill-matcher",
  "has_openai_api_key": false
}
```

Notice that the API key itself is not printed.

## Why We Use `mock`

For now, `MODEL_PROVIDER=mock` means the app uses our deterministic skill matcher instead of a paid AI API.

This lets us keep building and testing without spending money or debugging API issues too early.

Later, we will support:

```text
MODEL_PROVIDER=openai
```

## Interview Explanation

You can explain Day 5 like this:

> I added configuration management using environment variables and local `.env` files, keeping API keys out of source code and GitHub. The app can report safe config metadata without exposing secrets, which prepares the project for OpenAI or other LLM providers.

## Next Step

Next we will add the first LLM-ready interface so the app can support both a mock analyzer and a real AI analyzer later.
