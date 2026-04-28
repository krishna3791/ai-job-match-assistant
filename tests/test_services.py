import pytest

from app.config import AppConfig
from app.services import MockSkillAnalyzer, OpenAIAnalyzer, get_analyzer


def test_get_analyzer_returns_mock_provider() -> None:
    config = AppConfig(
        app_env="test",
        model_provider="mock",
        model_name="mock-skill-matcher",
        openai_api_key=None,
    )

    analyzer = get_analyzer(config)

    assert isinstance(analyzer, MockSkillAnalyzer)
    assert analyzer.provider_name == "mock"


def test_get_analyzer_returns_openai_provider() -> None:
    config = AppConfig(
        app_env="test",
        model_provider="openai",
        model_name="gpt-test",
        openai_api_key="test-key",
    )

    analyzer = get_analyzer(config)

    assert isinstance(analyzer, OpenAIAnalyzer)
    assert analyzer.provider_name == "openai"


def test_openai_provider_requires_api_key() -> None:
    analyzer = OpenAIAnalyzer(
        config=AppConfig(
            app_env="test",
            model_provider="openai",
            model_name="gpt-test",
            openai_api_key=None,
        )
    )

    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        analyzer.analyze("resume", "job")


def test_openai_provider_uses_structured_response(monkeypatch: pytest.MonkeyPatch) -> None:
    class ParsedOutput:
        score = 75
        readiness_level = "good match with a few gaps"
        resume_skills = ["python"]
        job_skills = ["python", "llm"]
        matched_skills = ["python"]
        missing_skills = ["llm"]
        missing_skills_by_category = {"ai_engineering": ["llm"]}
        suggestions = ["Add LLM project experience."]
        learning_plan = ["Build a small hands-on feature that uses llm."]

    class FakeResponse:
        output_parsed = ParsedOutput()

    class FakeResponses:
        def parse(self, **kwargs: object) -> FakeResponse:
            assert kwargs["model"] == "gpt-test"
            assert "text_format" in kwargs
            return FakeResponse()

    class FakeClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-key"
            self.responses = FakeResponses()

    import types
    import sys

    fake_openai = types.SimpleNamespace(OpenAI=FakeClient)
    monkeypatch.setitem(sys.modules, "openai", fake_openai)

    analyzer = OpenAIAnalyzer(
        config=AppConfig(
            app_env="test",
            model_provider="openai",
            model_name="gpt-test",
            openai_api_key="test-key",
        )
    )

    result = analyzer.analyze("resume", "job")

    assert result.score == 75
    assert result.missing_skills == ["llm"]


def test_get_analyzer_rejects_unknown_provider() -> None:
    config = AppConfig(
        app_env="test",
        model_provider="unknown",
        model_name="none",
        openai_api_key=None,
    )

    with pytest.raises(ValueError, match="Unsupported MODEL_PROVIDER"):
        get_analyzer(config)
