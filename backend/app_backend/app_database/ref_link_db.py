from sqlalchemy import text

from backend.helpers.db_engine import new_session
from ..app_classes import RefSchema, RefAnswerSchema
from ..logger import get_logger


logger = get_logger(__name__)


async def get_refs_list_db(user_id, session):
    logger.info("Запрос списка рефералов пользователя | user_id: %s", user_id)

    query = text("""
    SELECT accounts.name, accounts.user_id, accounts.vip_status, accounts.deals_summ
    FROM accounts
    WHERE referrer_id = :user_id;
    """)

    result = await session.execute(query, {"user_id": user_id})
    rows = result.mappings().all()

    refs_list = []
    for row in rows:
        deals_summ = float(row["deals_summ"])
        refs_list.append(
            RefSchema(
                name=row["name"],
                avatar_filename=f"{row['user_id']}.png",
                vip_status=row["vip_status"],
                deals_summ=deals_summ,
                profit=deals_summ * 0.04,
            )
        )

    return refs_list


async def get_ref_link_db(user_id: int):
    logger.info("Запрос реферальной ссылки пользователя | user_id: %s", user_id)

    query = text("SELECT accounts.ref_link FROM accounts WHERE accounts.user_id = :user_id")

    async with new_session() as session:
        result = await session.execute(query, {"user_id": user_id})

        ref_link = result.scalar_one_or_none()
        if ref_link is None:
            raise Exception("ref_link not found")

        refs_list = await get_refs_list_db(user_id, session)

        ref_answer = RefAnswerSchema(
            ref_link=ref_link,
            refs_list=refs_list
        )

        return ref_answer