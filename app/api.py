from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.config import load_config
from app.matcher import MatchResult
from app.schemas import AnalyzeRequest, AnalyzeResponse, HealthResponse
from app.services import get_analyzer


app = FastAPI(
    title="AI Job Match Assistant",
    description="Compare resumes against job descriptions and return skill-gap analysis.",
    version="0.1.0",
)


def match_result_to_response(result: MatchResult, provider: str) -> AnalyzeResponse:
    return AnalyzeResponse(
        score=result.score,
        readiness_level=result.readiness_level,
        resume_skills=result.resume_skills,
        job_skills=result.job_skills,
        matched_skills=result.matched_skills,
        missing_skills=result.missing_skills,
        missing_skills_by_category=result.missing_skills_by_category,
        suggestions=result.suggestions,
        learning_plan=result.learning_plan,
        provider=provider,
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    config = load_config()
    return HealthResponse(
        status="ok",
        app_env=config.app_env,
        model_provider=config.model_provider,
        model_name=config.model_name,
        has_openai_api_key=config.has_openai_api_key,
    )


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    try:
        analyzer = get_analyzer()
        result = analyzer.analyze(
            resume_text=request.resume_text,
            job_description_text=request.job_description_text,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc

    return match_result_to_response(result, provider=analyzer.provider_name)
