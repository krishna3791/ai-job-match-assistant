from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"


@dataclass(frozen=True)
class AppConfig:
    app_env: str
    model_provider: str
    model_name: str
    openai_api_key: str | None

    @property
    def has_openai_api_key(self) -> bool:
        return bool(self.openai_api_key)


def parse_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key:
            values[key] = value

    return values


def get_config_value(
    key: str, env_values: dict[str, str], default: str | None = None
) -> str | None:
    return os.environ.get(key) or env_values.get(key) or default


def load_config(env_file: Path = DEFAULT_ENV_FILE) -> AppConfig:
    env_values = parse_env_file(env_file)

    return AppConfig(
        app_env=get_config_value("APP_ENV", env_values, "development") or "development",
        model_provider=get_config_value("MODEL_PROVIDER", env_values, "mock") or "mock",
        model_name=get_config_value("MODEL_NAME", env_values, "mock-skill-matcher")
        or "mock-skill-matcher",
        openai_api_key=get_config_value("OPENAI_API_KEY", env_values),
    )
