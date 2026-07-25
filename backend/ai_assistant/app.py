from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from ai_assistant.api.routers import chat
from ai_assistant.core.config import load_app_settings, load_ai_settings
from ai_assistant.db.dependencies import init_main_session_factory, get_main_session_factory
from ai_assistant.llm.client import make_llm_client
from ai_assistant.logger import get_logger
from ai_assistant.tools.loader import load_tools
from ai_assistant.tools.topics import load_topics

logger = get_logger(__name__)


def load_system_prompt() -> str:
    path = Path(__file__).parent / "prompts" / "system.md"
    return path.read_text(encoding="utf-8")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _app.state.app_settings = load_app_settings()
    _app.state.ai_settings = load_ai_settings()
    init_main_session_factory(_app.state.app_settings.main_database_url)
    async with get_main_session_factory()() as session:
        await load_topics(session)
    load_tools()
    _app.state.llm_client = make_llm_client(_app.state.ai_settings)
    _app.state.system_prompt = load_system_prompt()
    logger.info("Traff AI успешно запущен")
    yield
    await _app.state.llm_client.aclose()
    logger.info("Traff AI остановлен")


app = FastAPI(title="TraffMarket AI Assistant", version="1.0.0", lifespan=lifespan)
app.include_router(chat.router)


@app.get("/health", tags=["Health"], summary="Проверка состояния сервиса")
async def health() -> dict:
    return {"status": "ok"}
