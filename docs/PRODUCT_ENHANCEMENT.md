# Product Enhancement: Local Resume Review App

## What Changed

The project now has a cleaner local web interface at:

```text
http://127.0.0.1:8000/
```

The interface supports:

- Resume upload
- Job description input
- Background analysis
- Match percentage
- ATS score
- Missing skills
- Resume suggestions
- Resume preview
- Rewrite draft download

## Supported Upload Formats

- `.txt`
- `.docx`
- `.pdf`

## Rewrite Safety

The rewrite workflow is intentionally conservative.

It does not invent:

- Employers
- Dates
- Certifications
- Metrics
- Tools
- Responsibilities
- Years of experience

For `.docx`, the app preserves the original document and appends a targeted rewrite draft section. This avoids destroying the original formatting while still giving a useful resume-improvement artifact.

## Future Improvement

A more advanced version can use a full document transformation pipeline to rewrite specific bullets while preserving exact paragraph/run formatting. That should be handled carefully and reviewed before use.
