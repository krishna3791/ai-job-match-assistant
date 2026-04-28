# Day 7: Provider Routing

## What We Built

Today we connected configuration to analyzer selection.

The app reads:

```text
MODEL_PROVIDER=mock
```

and chooses the correct analyzer.

## Why This Matters

This is how real systems support multiple environments:

- Local development can use `mock`
- Production can use `openai`
- Tests can use deterministic behavior

## Interview Explanation

> I added provider routing from config so the application can choose the right analyzer based on environment settings, while keeping local development deterministic and cost-free.
