from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from.endpoints import endpoints
from .pages.announs import announs_page
from .pages.announ_creator import announ_creator
from backend.config import AppConfig
from .logger import get_logger


logger = get_logger(__name__)


def app_run():
    try:
        logger.info("Запуск FastAPI app")
        uvicorn.run(app, host=AppConfig.host, port=AppConfig.port)

    except Exception as e:
        logger.error(f"Ошибка при запуске FastAPI app: {str(e)}")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints)
app.include_router(announs_page)
app.include_router(announ_creator)