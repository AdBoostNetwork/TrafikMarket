import os
from dataclasses import dataclass

@dataclass(frozen=True)
class AISettings:
    ai_host: str
    ai_port: int
    ai_database_url: str
    main_database_url: str
    openrouter_api_key: str
    openrouter_url: str
    llm_model: str


def load_ai_settings() -> AISettings:
    return AISettings(
        ai_host = os.environ["AI_HOST"],
        ai_port = int(os.environ["AI_PORT"]),
        ai_database_url = os.environ["AI_DATABASE_URL"],
        main_database_url = os.environ["MAIN_DATABASE_URL"],
        openrouter_api_key = os.environ["OPENROUTER_API_KEY"],
        openrouter_url = os.environ["OPENROUTER_URL"],
        llm_model = os.environ["LLM_MODEL"],
    )