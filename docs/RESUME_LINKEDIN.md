# Resume And LinkedIn Content

## Resume Bullet Options

- Built a FastAPI-based AI Job Match Assistant that compares resumes against job descriptions, identifies skill gaps, generates match scores, and returns structured learning recommendations.
- Designed a provider abstraction supporting a deterministic mock analyzer and an OpenAI structured-output analyzer path for future LLM-powered resume/job analysis.
- Implemented SQLite persistence, analysis history endpoints, local vector search over stored job descriptions, and automated pytest coverage for CLI, API, database, provider, and evaluation workflows.
- Created a production-style Python project with virtual environment setup, typed Pydantic schemas, configuration management, API documentation, and GitHub documentation.

## LinkedIn Project Post

I built an AI Job Match Assistant as part of my transition from Data Engineering into AI Engineering.

The project compares a resume against a job description and returns a structured analysis with match score, matched skills, missing skills, skill-gap categories, resume suggestions, and a learning plan.

What I implemented:

- Python CLI
- FastAPI backend
- Pydantic request/response schemas
- SQLite analysis history
- Provider abstraction for mock and OpenAI analyzers
- Local vector search for similar job descriptions
- Automated pytest coverage
- Safe `.env` configuration

The goal of this project was not to build a startup product. It was to demonstrate how my data engineering background can extend into AI application engineering: APIs, data storage, retrieval, testing, and LLM-ready system design.

GitHub: https://github.com/krishna3791/ai-job-match-assistant
