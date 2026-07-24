import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    ai_host: str
    ai_port: int
    ai_database_url: str
    main_database_url: str


@dataclass(frozen=True)
class AISettings:
    openrouter_api_key: str
    openrouter_url: str
    llm_model: str
    temperature: float
    max_tokens: int


def load_app_settings() -> AppSettings:
    return AppSettings(
        ai_host = os.environ["AI_HOST"],
        ai_port = int(os.environ["AI_PORT"]),
        ai_database_url = os.environ["AI_DATABASE_URL"],
        main_database_url = os.environ["MAIN_DATABASE_URL"],
    )


def load_ai_settings() -> AISettings:
    return AISettings(
        openrouter_api_key = os.environ["OPENROUTER_API_KEY"],
        openrouter_url = os.environ["OPENROUTER_URL"],
        llm_model = os.environ["LLM_MODEL"],
        temperature = float(os.environ["LLM_TEMPERATURE"]),
        max_tokens = int(os.environ["LLM_MAX_TOKENS"]),
    )
