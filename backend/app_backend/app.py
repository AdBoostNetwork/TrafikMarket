#Точка входа в сайт. Запуск fastapi

from fastapi import FastAPI

from pages.profile import profile_page
from logger import get_logger


logger = get_logger(__name__)

app = FastAPI()

app.include_router(profile_page)