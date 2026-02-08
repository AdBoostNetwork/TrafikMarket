#Точка входа в сайт. Запуск fastapi

from fastapi import FastAPI
import uvicorn
import html

from .pages.profile import profile_page
from .app_config import AppConfig
from .logger import get_logger


logger = get_logger(__name__)


def app_run():
    try:
        logger.info("Запуск FastAPI app")
        uvicorn.run(app, host=AppConfig.host, port=AppConfig.port)

    except Exception as e:
        short_error = html.escape(str(e))
        logger.error("Ошибка при запуске FastAPI app: %s", short_error)



app = FastAPI()

app.include_router(profile_page)