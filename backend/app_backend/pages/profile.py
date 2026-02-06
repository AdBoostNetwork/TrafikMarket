from fastapi import APIRouter

from ..app_classes import MyProfile
from ..database import get_profile_info_db

profile_page = APIRouter()


@profile_page.get("/my_profile", tags=["Профиль"], summary="Получение данных профиля")
def get_profile(user_id: int):
    data = get_profile_info_db(user_id)

    profile_info = MyProfile(
        name=data["name"],
        deals_count=data["deals_count"],
        success_deals=data["success_deals"],
        balance=data["balance"],
        deps_list=data["deps_list"],
    )

    return profile_info