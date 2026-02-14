from fastapi import APIRouter
import html

from ..logger import get_logger


logger = get_logger(__name__)

announs_page = APIRouter()


@announs_page.get("/get_announs_list")
async def get_announs_list():
    ...