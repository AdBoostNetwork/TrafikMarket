from sqlalchemy import text

from backend.app_backend.app_classes import SellerInfo, ClosedAnnoun
from backend.db_engine import new_session
from backend.logger import get_logger


logger = get_logger(__name__)


async def delete_announ_db(announ_id: int, user_id: int):
    query = text("DELETE FROM announs WHERE announ_id = :announ_id AND seller_id = :user_id RETURNING announ_id")

    async with new_session() as session:
        result = await session.execute(query, {"announ_id": announ_id, "user_id": user_id})
        deleted_id = result.scalar_one_or_none()

        if deleted_id is None:
            raise Exception("not_allowed")

        await session.commit()
        return {"success": True}


async def get_seller_info_db(session, seller_id: int):
    logger.info("Получение данных продавца | seller_id: %s", seller_id)

    query = text(
        """
        SELECT a.name,
               a.success_count,
               a.good_marks,
               a.bad_marks,
               (SELECT COUNT(*)
                FROM deals d
                WHERE d.seller_id = :seller_id) AS deals_count
        FROM accounts a
        WHERE a.user_id = :seller_id
        """
    )

    result = await session.execute(query, {"seller_id": seller_id})
    row = result.mappings().first()

    if row is None:
        raise Exception(f"seller_not_found seller_id={seller_id}")

    success_count = int(row["success_count"])
    deals_count = int(row["deals_count"])
    success_deals_percent = int(success_count * 100 / deals_count) if deals_count else 0

    marks_count = int(row["good_marks"]) + int(row["bad_marks"])
    rating = 0.0 if marks_count == 0 else round((float(row["good_marks"]) / marks_count) * 5, 1)

    return SellerInfo(
        name=row["name"],
        deals_count=deals_count,
        success_deals_percent=success_deals_percent,
        rating=rating,
    )


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


async def get_user_announs_db(user_id: int):
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
                topic=""
            )
            announs_list.append(announ)

    return announs_list