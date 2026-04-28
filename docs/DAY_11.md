# Day 11: SQLite Database

## What We Built

Today we added SQLite support in `app/database.py`.

SQLite is a lightweight database that stores data in a local `.db` file.

## Why This Matters

Before this, the app returned an analysis but forgot it immediately.

Now the app has a place to store analysis history, which makes it behave more like a real backend system.

## Interview Explanation

> I added SQLite persistence so each resume/job analysis can be stored locally with score, provider metadata, source text, and structured result JSON.
