from __future__ import annotations

from pydantic import BaseModel, Field


class LLMAnalysisOutput(BaseModel):
    score: int = Field(..., ge=0, le=100)
    readiness_level: str
    resume_skills: list[str]
    job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    missing_skills_by_category: dict[str, list[str]]
    suggestions: list[str]
    learning_plan: list[str]


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    job_description_text: str = Field(..., min_length=1)


class AnalyzeResponse(BaseModel):
    id: int | None = None
    score: int
    readiness_level: str
    resume_skills: list[str]
    job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    missing_skills_by_category: dict[str, list[str]]
    suggestions: list[str]
    learning_plan: list[str]
    provider: str


class AnalysisHistoryItem(BaseModel):
    id: int
    created_at: str
    provider: str
    model_provider: str
    model_name: str
    score: int
    readiness_level: str


class AnalysisDetailResponse(BaseModel):
    id: int
    created_at: str
    provider: str
    model_provider: str
    model_name: str
    score: int
    readiness_level: str
    resume_text: str
    job_description_text: str
    result: dict[str, object]


class HealthResponse(BaseModel):
    status: str
    app_env: str
    model_provider: str
    model_name: str
    has_openai_api_key: bool
