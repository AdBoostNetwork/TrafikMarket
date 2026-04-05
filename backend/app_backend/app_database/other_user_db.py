from sqlalchemy import text

from backend.db_engine import new_session
from ..app_classes import OtherProfile
from backend.logger import get_logger


logger = get_logger(__name__)


async def get_user_info_db(user_id: int):
    logger.info(f"Получение данных пользователя {user_id}")

    query = text("""
                 SELECT a.name, a.success_count, a.good_marks, a.bad_marks, a.deals_summ, a.reg_date, a.was_online,
                        (SELECT COUNT(*)
                         FROM deals d
                         WHERE d.seller_id = :user_id OR d.buyer_id = :user_id)
                         AS deals_count
                 FROM accounts a
                 WHERE a.user_id = :user_id
                 """)

    try:
        async with new_session() as session:
            result = await session.execute(query, {"user_id": user_id})
    except Exception as e:
        logger.error(f"Ошибка при получении данных пользователя | user_id = {user_id}| error: {str(e)}")
        raise ValueError(f"Ошибка при получении данных пользователя")

    data = result.mappings().first()

    success_deals_percent = int(data["success_count"] * 100 / data["deals_count"]) if data["deals_count"] else 0
    marks_count = int(data["good_marks"] + data["bad_marks"])

    if marks_count == 0:
        rating = 0.0
    else:
        rating = round((data["good_marks"] / marks_count) * 5, 1)

    profile = OtherProfile(
        name=data["name"],
        avatar_filename=f'{user_id}.jpg',
        rating=rating,
        deals_count=data["deals_count"],
        success_deals_percent=success_deals_percent,
        deals_summ=data["deals_summ"],
        registration_date=data["reg_date"],
        was_online=data["was_online"],
    )

    return profile