from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.config import AppConfig, load_config
from app.matcher import MatchResult, analyze_match


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

        raise NotImplementedError(
            "OpenAI analysis is not implemented yet. Use MODEL_PROVIDER=mock for now."
        )


def get_analyzer(config: AppConfig | None = None) -> JobMatchAnalyzer:
    config = config or load_config()

    if config.model_provider == "mock":
        return MockSkillAnalyzer()

    if config.model_provider == "openai":
        return OpenAIAnalyzer(config=config)

    raise ValueError(f"Unsupported MODEL_PROVIDER: {config.model_provider}")
