from fastapi import APIRouter
import html

from ..app_classes import MyProfile, Transaction
from ..app_database.profile_db import get_profile_info_db
from ..logger import get_logger


logger = get_logger(__name__)

profile_page = APIRouter()


@profile_page.get("/my_profile", tags=["Профиль"], summary="Получение данных профиля")
async def get_profile(user_id: int):
    try:
        return await get_profile_info_db(user_id)

    except Exception as e:
        short_error = html.escape(str(e))

        logger.error("Ошибка при получении данных профиля | Пользователь: %s | Ошибка: %s", user_id, short_error)
        return {"error": short_error}