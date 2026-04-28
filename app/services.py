from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.config import AppConfig, load_config
from app.matcher import MatchResult, analyze_match
from app.schemas import LLMAnalysisOutput


class JobMatchAnalyzer(Protocol):
    provider_name: str

    def analyze(self, resume_text: str, job_description_text: str) -> MatchResult:
        """Analyze a resume against a job description."""


@dataclass(frozen=True)
class MockSkillAnalyzer:
    provider_name: str = "mock"

    def analyze(self, resume_text: str, job_description_text: str) -> MatchResult:
        return analyze_match(resume_text, job_description_text)


@dataclass(frozen=True)
class OpenAIAnalyzer:
    config: AppConfig
    provider_name: str = "openai"

    def analyze(self, resume_text: str, job_description_text: str) -> MatchResult:
        if not self.config.has_openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when MODEL_PROVIDER=openai.")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Install the openai package before using MODEL_PROVIDER=openai."
            ) from exc

        client = OpenAI(api_key=self.config.openai_api_key)
        response = client.responses.parse(
            model=self.config.model_name,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI career assistant. Compare a resume and job "
                        "description. Return only structured analysis using the schema."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Resume:\n"
                        f"{resume_text}\n\n"
                        "Job description:\n"
                        f"{job_description_text}"
                    ),
                },
            ],
            text_format=LLMAnalysisOutput,
        )
        parsed = response.output_parsed

        return MatchResult(
            score=parsed.score,
            readiness_level=parsed.readiness_level,
            resume_skills=parsed.resume_skills,
            job_skills=parsed.job_skills,
            matched_skills=parsed.matched_skills,
            missing_skills=parsed.missing_skills,
            missing_skills_by_category=parsed.missing_skills_by_category,
            suggestions=parsed.suggestions,
            learning_plan=parsed.learning_plan,
        )


def get_analyzer(config: AppConfig | None = None) -> JobMatchAnalyzer:
    config = config or load_config()

    if config.model_provider == "mock":
        return MockSkillAnalyzer()

    if config.model_provider == "openai":
        return OpenAIAnalyzer(config=config)

    raise ValueError(f"Unsupported MODEL_PROVIDER: {config.model_provider}")
