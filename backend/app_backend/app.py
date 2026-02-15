#Точка входа в сайт. Запуск fastapi

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import html

from .pages.profile import profile_page
from .pages.ref_link import ref_link_page
from .pages.opened_announ import opened_announ_page
from .pages.announs import announs_page
from .pages.announ_creator import announ_creator
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_page)
app.include_router(ref_link_page)
app.include_router(opened_announ_page)
app.include_router(announs_page)
app.include_router(announ_creator)