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

        free_balance = float(data["current_balance"]) - float(data["frozen_balance"])
        free_balance_rub = free_balance * 80

        marks_count = int(data["good_marks"] + data["bad_marks"])

        if marks_count == 0:
            rating = 0.0
        else:
            rating = round((data["good_marks"] / marks_count) * 5, 1)

        profile_info = MyProfile(
            name=data["name"],
            deals_count=data["deals_count"],
            success_deals_percent=success_deals_percent,
            free_balance=free_balance,
            free_balance_rub=free_balance_rub,
            rating=rating,
            deals_summ=0,
            avatar_filename=f'{str(data["user_id"])}.jpg',
            deps_list=deps_list,
        )

        logger.info("Данные профиля пользователя %s успешно получены", user_id)
        return profile_info

    except Exception as e:
        short_error = html.escape(str(e))

        logger.error("Ошибка при получении данных профиля | Пользователь: %s | Ошибка: %s", user_id, short_error)
        return {"error": short_error}