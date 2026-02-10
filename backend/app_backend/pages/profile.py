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
        data = await get_profile_info_db(user_id)

        deps_list = None
        if data.get("transactions"):
            deps_list = [
                Transaction(
                    trn_type=str(t["type"]),
                    trn_summ=str(t["summ"]),
                    trn_date=str(t["transaction_time"]),
                )
                for t in data["transactions"]
            ]

        success_deals_percent = int(data["success_count"] * 100 / data["deals_count"]) if data["deals_count"] else 0

        profile_info = MyProfile(
            name=data["name"],
            deals_count=data["deals_count"],
            success_deals_percent=success_deals_percent,
            balance=data["current_balance"],
            avatar_filename=data["avatar_filename"],
            deps_list=deps_list,
        )

        logger.info("Данные профиля пользователя %s успешно получены", user_id)
        return profile_info

    except Exception as e:
        short_error = html.escape(str(e))

        logger.error("Ошибка при получении данных профиля | Пользователь: %s | Ошибка: %s", user_id, short_error)
        return {"error": short_error}