# Day 17: LLM Prompt Design

## What We Built

Today we added the first LLM prompt inside the OpenAI provider.

The prompt tells the model to compare:

- Resume text
- Job description text

and return structured career analysis.

## Why This Matters

Prompting in production code should be specific, constrained, and connected to a schema.

## Interview Explanation

> I designed the LLM prompt to compare resume and job description text while requiring a structured response instead of free-form text.
