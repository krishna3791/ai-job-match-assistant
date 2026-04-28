# Day 3: Virtual Environment and Cleaner CLI

## What We Built

Today we made the project easier to run and closer to a real Python application.

We added:

- Virtual environment setup instructions
- A proper CLI module in `app/cli.py`
- A text report format for humans
- A JSON output format for automation and future APIs

## Why A Virtual Environment Matters

A virtual environment is a private Python setup for one project.

Without a virtual environment, every package you install goes into your global Python installation. That becomes messy when different projects need different package versions.

With a virtual environment, this project gets its own packages inside:

```text
.venv/
```

We do not commit `.venv` to GitHub because it can be rebuilt from `requirements.txt`.

## Commands For Cursor Terminal

Open the project in Cursor, then open a terminal and run:

```powershell
python -m venv .venv
```

This creates the virtual environment.

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation works, your terminal prompt should show:

```text
(.venv)
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install project requirements:

```powershell
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then try activation again:

```powershell
.\.venv\Scripts\Activate.ps1
```

If `python` is not recognized, Cursor may know about Python but your terminal PATH may not. In Cursor, press `Ctrl + Shift + P`, choose `Python: Select Interpreter`, and select your Python version.

Run the app:

```powershell
python scripts\analyze_match.py data\sample_resume.txt data\sample_job_description.txt
```

Run JSON output:

```powershell
python scripts\analyze_match.py data\sample_resume.txt data\sample_job_description.txt --format json
```

## New File: `app/cli.py`

The CLI file handles command-line behavior:

- Read user arguments
- Read input files
- Call the matcher
- Print text or JSON output

This is cleaner than putting all logic inside `scripts/analyze_match.py`.

## Why Keep `scripts/analyze_match.py`

The script is still useful because it gives beginners a simple command to run.

But now the script only points to the real CLI code:

```text
scripts/analyze_match.py -> app/cli.py -> app/matcher.py
```

That structure is easier to grow when we add APIs, tests, and LLM calls.

## Text Output vs JSON Output

Text output is easier for humans to read.

JSON output is better for software systems.

In AI engineering, both matter:

- Humans need readable summaries
- APIs and frontends need structured data

## Interview Explanation

You can explain Day 3 like this:

> I refactored the project into a cleaner application structure. The command-line script delegates to a CLI module, which calls the core matching logic. The app supports both human-readable text output and JSON output for future API/frontend integration. I also documented virtual environment setup so the project can be reproduced cleanly.

## Next Step

Next we will add tests so the project proves its matching logic works before we introduce LLM behavior.
