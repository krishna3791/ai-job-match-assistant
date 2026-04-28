# Day 6: LLM-Ready Analyzer Interface

## What We Built

Today we added `app/services.py`.

This file defines a common analyzer interface and two providers:

- `MockSkillAnalyzer`
- `OpenAIAnalyzer`

The mock analyzer uses the current deterministic skill matcher. The OpenAI analyzer is a placeholder that we will implement later.

## Why This Matters

AI applications should not spread model-specific code across the whole project.

The rest of the app can now call:

```text
analyzer.analyze(resume_text, job_description_text)
```

That means the CLI and API do not need to care whether the analyzer is mock, OpenAI, Azure OpenAI, or another provider.

## Interview Explanation

> I introduced a provider interface so the app can switch between a deterministic mock analyzer and a future LLM analyzer without changing the CLI or API layers.
