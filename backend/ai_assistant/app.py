from contextlib import asynccontextmanager

from fastapi import FastAPI

from ai_assistant.core.config import load_ai_settings
from ai_assistant.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _app.state.settings = load_ai_settings()
    logger.info("ai-assistant startup")
    yield
    logger.info("ai-assistant shutdown")


app = FastAPI(title="TraffMarket AI Assistant", version="1.0.0", lifespan=lifespan)


@app.get("/health", tags=["Health"], summary="Проверка состояния сервиса")
async def health() -> dict:
    return {"status": "ok"}
