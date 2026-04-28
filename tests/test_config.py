from pathlib import Path

from app.config import load_config, parse_env_file


TMP_DIR = Path(__file__).parent / ".tmp"


def write_tmp_env(name: str, content: str = "") -> Path:
    TMP_DIR.mkdir(exist_ok=True)
    env_file = TMP_DIR / name
    env_file.write_text(content, encoding="utf-8")
    return env_file


def test_parse_env_file_reads_key_value_pairs() -> None:
    env_file = write_tmp_env(
        "parse.env",
        """
APP_ENV=test
MODEL_PROVIDER=openai
MODEL_NAME="gpt-test"
OPENAI_API_KEY='secret-key'
""",
    )

    values = parse_env_file(env_file)

    assert values == {
        "APP_ENV": "test",
        "MODEL_PROVIDER": "openai",
        "MODEL_NAME": "gpt-test",
        "OPENAI_API_KEY": "secret-key",
    }


def test_load_config_uses_defaults_when_env_file_is_missing() -> None:
    config = load_config(TMP_DIR / "missing.env")

    assert config.app_env == "development"
    assert config.model_provider == "mock"
    assert config.model_name == "mock-skill-matcher"
    assert config.openai_api_key is None
    assert config.has_openai_api_key is False


def test_load_config_detects_api_key_without_exposing_it() -> None:
    env_file = write_tmp_env("api-key.env", "OPENAI_API_KEY=test-key\n")

    config = load_config(env_file)

    assert config.openai_api_key == "test-key"
    assert config.has_openai_api_key is True
