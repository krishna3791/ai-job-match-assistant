# Day 16: OpenAI Provider Shape

## What We Built

Today we made the `OpenAIAnalyzer` ready to call OpenAI through the Responses API.

It uses structured outputs so the model can return data in the same shape as the rest of the app.

## Why This Matters

Structured outputs are better than asking for plain text because APIs and frontends need predictable fields.

Reference: https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses&lang=python

## Interview Explanation

> I added an OpenAI provider path using structured outputs so LLM responses can be validated and converted into the same internal result model as the mock analyzer.
