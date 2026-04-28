# Day 12: Save Analysis Results

## What We Built

Today we added `app/repository.py`.

This file saves and reads analysis records from SQLite.

## What Gets Stored

Each analysis stores:

- Provider
- Model provider
- Model name
- Score
- Readiness level
- Resume text
- Job description text
- Full JSON result

## Interview Explanation

> I added a repository layer to separate database operations from API logic, making the application easier to test and maintain.
