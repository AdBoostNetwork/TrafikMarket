from fastapi import APIRouter

from .app_database.profile_db import get_profile_info_db
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