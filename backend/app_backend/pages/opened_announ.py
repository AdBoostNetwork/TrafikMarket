from fastapi import APIRouter
import html

from ..app_classes import AnnounPageSchema
from ..logger import get_logger


logger = get_logger(__name__)

opened_announ_page = APIRouter()


@opened_announ_page.get("/get_announ_info", tags=["Страница объявления"], summary="Получение данных объявления")
async def get_announ_info(announ_id: int):
    ...