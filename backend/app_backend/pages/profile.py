from fastapi import APIRouter
import html

from ..app_classes import MyProfile
from ..database import get_profile_info_db
from ..logger import get_logger


logger = get_logger(__name__)

profile_page = APIRouter()


@profile_page.get("/my_profile", tags=["Профиль"], summary="Получение данных профиля")
async def get_profile(user_id: int):
    try:
        data = await get_profile_info_db(user_id)

        profile_info = MyProfile(
            name=data["name"],
            deals_count=data["deals_count"],
            success_deals=data["success_count"],
            balance=data["current_balance"],
       #     deps_list=data["deps_list"],
        )

        logger.info("Данные профиля пользователя %s успешно получены", user_id)
        return profile_info

    except Exception as e:
        short_error = html.escape(str(e))

        logger.error("Ошибка при получении данных профиля | Пользователь: %s | Ошибка: %s", user_id, short_error)
        return {"error": short_error}