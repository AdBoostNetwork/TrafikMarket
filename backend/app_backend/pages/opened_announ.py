from fastapi import APIRouter
import html

from ..app_database.opened_announ_db import get_announ_page_db
from ..logger import get_logger


logger = get_logger(__name__)

opened_announ_page = APIRouter()


@opened_announ_page.get("/get_announ_info", tags=["Страница объявления"], summary="Получение данных объявления")
async def get_announ_info(announ_id: int):
    logger.info("Запрос данных объявления | announ_id=%s", announ_id)

    try:
        data = await get_announ_page_db(announ_id)
        return data

    except Exception as e:
        err = html.escape(str(e))
        logger.error("Ошибка получения данных объявления | announ_id=%s | error=%s", announ_id, err)
        return {"error": err}