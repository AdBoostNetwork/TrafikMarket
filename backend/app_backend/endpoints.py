from fastapi import APIRouter

from .app_database.profile_db import get_profile_info_db
from .app_database.ref_link_db import get_ref_link_db
from .app_database.opened_announ_db import get_announ_page_db
from .logger import get_logger


logger = get_logger(__name__)

endpoints = APIRouter()


@endpoints.get("/my_profile", tags=["Профиль"], summary="Получение данных профиля")
async def get_profile(user_id: int):
    try:
        return await get_profile_info_db(user_id)
    except Exception as e:
        logger.error(f"Ошибка при получении данных профиля | Пользователь: {user_id} | Ошибка: {str(e)}")
        return {"error": str(e)}


@endpoints.get("/ref_link", tags=["Реферальная ссылка"], summary="Получение реферальной ссылки пользователя")
async def get_ref_link(user_id: int):
    try:
        return await get_ref_link_db(user_id)
    except Exception as e:
        logger.error(f"Ошибка при получении реферальной ссылки пользователя {user_id} | {str(e)}")
        return {"error": str(e)}


@endpoints.get("/get_announ_info", tags=["Страница объявления"], summary="Получение данных объявления")
async def get_announ_info(announ_id: int):
    try:
        return await get_announ_page_db(announ_id)
    except Exception as e:
        logger.error(f"Ошибка получения данных объявления | announ_id = {announ_id} | error = {str(e)}")
        return {"error": str(e)}