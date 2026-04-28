# Day 19: Mock Fallback Strategy

## What We Built

Today we kept `MODEL_PROVIDER=mock` as the default.

That means the project runs without an API key or paid model.

## Why This Matters

Good AI applications should have a cheap, deterministic local path for development and testing.

## Interview Explanation

> I kept a deterministic mock provider as the default so tests and local development do not depend on external AI services.
