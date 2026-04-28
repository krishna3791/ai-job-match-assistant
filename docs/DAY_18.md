# Day 18: Structured LLM Output

## What We Built

Today we added `LLMAnalysisOutput` in `app/schemas.py`.

This schema represents the exact fields the LLM should return.

## Why This Matters

Without structure, LLM output can be inconsistent.

With structure, the application can safely consume:

- Score
- Skills
- Missing gaps
- Suggestions
- Learning plan

## Interview Explanation

> I used a typed schema for LLM output so generated analysis can be validated before entering the application flow.
