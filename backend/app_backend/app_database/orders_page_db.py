from sqlalchemy import text

from backend.db_engine import new_session
from ..app_classes import ClosedAnnoun, AnnounCreateSchema
from .helpers_db import get_seller_info_db
from ..logger import get_logger


logger = get_logger(__name__)


async def get_user_announs_data_db(session, user_id: int):
    logger.info("Получение данных объявлений пользователя | user_id: %s", user_id)

    query = text(
        """
        SELECT an.announ_id,
               an.title,
               an.short_text AS description,
               CASE
                   WHEN an.type = 'channel' THEN ch.price
                   WHEN an.type = 'traffic' THEN tr.price
               END AS price
        FROM announs an
                 LEFT JOIN channels ch
                           ON ch.chn_announ_id = an.announ_id
                          AND an.type = 'channel'
                 LEFT JOIN traffic tr
                           ON tr.trf_announ_id = an.announ_id
                          AND an.type = 'traffic'
        WHERE an.seller_id = :user_id
        ORDER BY an.announ_id DESC;
        """
    )

    result = await session.execute(query, {"user_id": user_id})
    return result.mappings().all()


async def get_my_announs_db(user_id: int):
    logger.info("Получение объявлений пользователя | user_id: %s", user_id)

    async with new_session() as session:
        seller = await get_seller_info_db(session, user_id)
        rows = await get_user_announs_data_db(session, user_id)
        announs_list = []

        for row in rows:
            announ = ClosedAnnoun(
                announ_id=int(row["announ_id"]),
                seller=seller,
                title=row["title"],
                price=float(row["price"]),
                description=row["description"],
            )
            announs_list.append(announ)

    return announs_list


async def get_active_orders_db(user_id: int):
    logger.info(f"Получение активных заказов пользователя | user_id: %s", user_id)


async def get_closed_orders_db(user_id: int):
    logger.info(f"Получение завершенных заказов пользователя | user_id: %s", user_id)


async def edit_announ_db(announ_id: int, data: AnnounCreateSchema):
    ...