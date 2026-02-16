from fastapi import APIRouter
import html

from ..app_classes import AnnounCreateSchema
from ..app_database.announ_creator_db import post_announ_db
from ..logger import get_logger


logger = get_logger(__name__)

announ_creator = APIRouter()


@announ_creator.post("/create_announ", tags=["Страница создания объявления"], summary="Создание объявления")
async def create_announ(announ_data: AnnounCreateSchema):
    logger.info("Запрос создания объявления")

    try:
        result = await post_announ_db(announ_data)
        return result

    except Exception as e:
        err = html.escape(str(e))
        logger.error("Ошибка создания объявления | error=%s", err)
        return {"error": err}