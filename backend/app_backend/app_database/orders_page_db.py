from ..app_classes import AnnounCreateSchema
from ..logger import get_logger


logger = get_logger(__name__)


async def get_active_orders_db(user_id: int):
    logger.info(f"Получение активных заказов пользователя | user_id: %s", user_id)


async def get_closed_orders_db(user_id: int):
    logger.info(f"Получение завершенных заказов пользователя | user_id: %s", user_id)


async def edit_announ_db(announ_id: int, data: AnnounCreateSchema):
    ...