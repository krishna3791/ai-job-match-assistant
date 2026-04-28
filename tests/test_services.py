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


def test_get_analyzer_rejects_unknown_provider() -> None:
    config = AppConfig(
        app_env="test",
        model_provider="unknown",
        model_name="none",
        openai_api_key=None,
    )

    with pytest.raises(ValueError, match="Unsupported MODEL_PROVIDER"):
        get_analyzer(config)
