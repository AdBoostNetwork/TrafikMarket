from fastapi import APIRouter
import html

from ..app_database.ref_link_db import get_ref_link_db
from ..logger import get_logger


logger = get_logger(__name__)

ref_link_page = APIRouter()

@ref_link_page.get("/ref_link", tags=["Реферальная ссылка"], summary="Получение реферальной ссылки пользователя")
async def get_ref_link(user_id: int):
    try:
        ref_link = await get_ref_link_db(user_id)
        logger.info("Ссылка пользователя %s успешно получена | %s", user_id, ref_link)

        return {"success": ref_link}

    except Exception as e:
        short_error = html.escape(str(e))
        logger.error("Ошибка при получении реферальной ссылки пользователя %s | %s", user_id, short_error)

        return {"error": short_error}