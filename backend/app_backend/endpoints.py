from fastapi import APIRouter, HTTPException

from .app_database.profile_db import get_profile_info_db
from .app_database.ref_link_db import get_ref_link_db
from .app_database.opened_announ_db import get_announ_page_db
from .app_database.announ_creator_db import post_announ_db
from .app_database.orders_page_db import get_active_orders_db, get_closed_orders_db, edit_announ_db
from app_database.other_user_db import get_user_info_db
from .app_database.helpers_db import delete_announ_db, get_user_announs_db
from backend.tgstat_module import ChartsData, get_last_posts, get_channel, get_ad
from backend.topics_reciever import build_topic_config
from .app_classes import AnnounCreateSchema
from .logger import get_logger


logger = get_logger(__name__)

endpoints = APIRouter()


@endpoints.get("/my_profile", tags=["Страница профиля"], summary="Получение данных профиля")
async def get_profile(user_id: int):
    try:
        return await get_profile_info_db(user_id)
    except Exception as e:
        logger.error(f"Ошибка при получении данных профиля | Пользователь: {user_id} | Ошибка: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/ref_link", tags=["Страница реферальной ссылки"], summary="Получение реферальной ссылки пользователя")
async def get_ref_link(user_id: int):
    try:
        return await get_ref_link_db(user_id)
    except Exception as e:
        logger.error(f"Ошибка при получении реферальной ссылки пользователя {user_id} | {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/get_announ_info", tags=["Страница объявления"], summary="Получение данных объявления")
async def get_announ_info(announ_id: int):
    try:
        return await get_announ_page_db(announ_id)
    except Exception as e:
        logger.error(f"Ошибка получения данных объявления | announ_id = {announ_id} | error = {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/tgstat_charts", tags=["Страница объявления"], summary="Получение графиков с TgStat")
def get_tgstat_charts(channel_link: str):
    try:
        charts_data = ChartsData(channel_link)
        return charts_data.get_charts_data()
    except Exception as e:
        logger.error(f"Ошибка получения графиков с TgStat | channel_link = {channel_link} | error = {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/tgstat_posts", tags=["Страница объявления"], summary="Получение постов канала с TgStat")
def get_tgstat_posts(channel_link: str):
    try:
        return get_last_posts(channel_link, posts_count=10)
    except Exception as e:
        logger.error(f"Ошибка получения постов канала с TgStat | channel_link = {channel_link} | error = {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/tgstat_channel", tags=["Страница создания объявления"], summary="Получение информации о канале с TgStat")
def get_tgstat_channel(channel_link: str):
    try:
        return get_channel(channel_link)
    except Exception as e:
        logger.error(f"Ошибка получения информации канала с TgStat | channel_link = {channel_link} | error = {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/tgstat_add", tags=["Страница создания объявления"], summary="Получение информации о канале для рекламы с TgStat")
def get_tgstat_ad(channel_link: str):
    try:
        return get_ad(channel_link)
    except Exception as e:
        logger.error(f"Ошибка получения информации канала для рекламы с TgStat | channel_link = {channel_link} | error = {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.post("/create_announ", tags=["Страница создания объявления"], summary="Создание объявления")
async def create_announ(announ_data: AnnounCreateSchema):
    try:
        return post_announ_db(announ_data)
    except Exception as e:
        logger.error(f"Ошибка при создании объявления: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/topics", tags=["Страница объявлений"], summary="Загрузка списка топиков")
async def get_topics():
    try:
        return await build_topic_config()
    except Exception as e:
        logger.error("Ошибка при загрузке топиков")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/user_announs", tags=["Страница заказов", "Страница другого пользователя"], summary="Получение объявлений пользователя")
async def get_my_announs(user_id: int):
    try:
        return await get_user_announs_db(user_id)
    except Exception as e:
        logger.error(f"Ошибка при загрузке объявлений пользователя | user_id = {user_id} | error = {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/active_orders", tags=["Страница заказов"], summary="Получение активных заказов пользователя")
async def get_active_orders(user_id: int):
    try:
        return await get_active_orders_db(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/closed_orders", tags=["Страница заказов"], summary="Получение завершенных заказов пользователя")
async def get_closed_orders(user_id: int):
    try:
        return await get_closed_orders_db(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.delete("/announ", tags=["Страница заказов"], summary="Удаление объявления")
async def delete_announ(announ_id: int, user_id: int):
    try:
        return await delete_announ_db(announ_id, user_id)
    except Exception as e:
        logger.error(f"Ошибка при удалении объявления | announ_id = {announ_id} | error = {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.put("/announ", tags=["Страница редактирования объявления"], summary="Редактирование объявления")
async def edit_announ(announ_id: int, announ_data: AnnounCreateSchema):
    try:
        return await edit_announ_db(announ_id, announ_data)
    except Exception as e:
        logger.error(f"Ошибка при редактировании объявления | announ_id = {announ_id} | error = {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@endpoints.get("/other_user", tags=["Станица другого пользователя"], summary="Получение информации о пользователе")
async def get_other_user_info(user_id: int):
    try:
        return await get_user_info_db(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))