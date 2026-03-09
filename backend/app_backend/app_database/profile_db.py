from sqlalchemy import text

from .db_engine import new_session
from ..app_classes import Transaction, MyProfile
from ..logger import get_logger


logger = get_logger(__name__)


async def get_user_transactions(session, user_id: int):
    logger.info("Запрос транзакций пользователя | user_id: %s", user_id)

    query = text("""
                 SELECT t.tr_type, t.summ, t.transaction_time 
                 FROM transactions t
                 WHERE t.user_id = :user_id
                 ORDER BY t.transaction_time DESC
                 """)

    result = await session.execute(query, {"user_id": user_id})
    rows = result.mappings().all()

    transactions_list = []
    if rows:
        transactions_list = [
            Transaction(
                trn_type=str(transaction["tr_type"]),
                trn_summ=str(transaction["summ"]),
                trn_date=str(transaction["transaction_time"]),
            )
            for transaction in rows
        ]

    return transactions_list


async def get_profile_info_db(user_id: int):
    logger.info("Запрос данных профиля | user_id: %s", user_id)

    query = text("""
                 SELECT a.name, a.user_id, a.current_balance, a.frozen_balance, a.success_count, a.good_marks, a.bad_marks, a.deals_summ,
                        (SELECT COUNT(*)
                         FROM deals d
                         WHERE d.seller_id = :user_id OR d.buyer_id = :user_id) AS deals_count
                 FROM accounts a
                 WHERE a.user_id = :user_id
                 """)

    async with new_session() as session:
        result = await session.execute(query, {"user_id": user_id})
        data = result.mappings().first()

        transactions_list = await get_user_transactions(session, user_id)

        success_deals_percent = int(data["success_count"] * 100 / data["deals_count"]) if data["deals_count"] else 0

        free_balance = float(data["current_balance"]) - float(data["frozen_balance"])
        free_balance_rub = free_balance * 80

        marks_count = int(data["good_marks"] + data["bad_marks"])

        if marks_count == 0:
            rating = 0.0
        else:
            rating = round((data["good_marks"] / marks_count) * 5, 1)

        profile_info = MyProfile(
            name=data["name"],
            deals_count=data["deals_count"],
            success_deals_percent=success_deals_percent,
            free_balance=free_balance,
            free_balance_rub=free_balance_rub,
            rating=rating,
            deals_summ=data["deals_summ"],
            avatar_filename=f'{str(data["user_id"])}.jpg',
            deps_list=transactions_list,
        )

        return profile_info