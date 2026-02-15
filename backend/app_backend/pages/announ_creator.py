from fastapi import APIRouter
import html

from ..logger import get_logger


logger = get_logger(__name__)

announ_creator = APIRouter()


@announ_creator.post("/create_announ")
async def create_announ():
    ...