from datetime import datetime

from sqlalchemy import text, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError, RepositoryError
from app.logger import get_logger

logger = get_logger(__name__)

_SQL_TRANSACTIONS = text("""
    SELECT
        'io'   AS kind,
        id,
        created_at,
        amount,
        type,
        NULL   AS direction,
        NULL   AS announ_type,
        NULL   AS referral_name
    FROM transactions_io
    WHERE user_id = :user_id

    UNION ALL

    SELECT
        'deal' AS kind,
        id,
        created_at,
        amount,
        NULL   AS type,
        'buy'  AS direction,
        announ_type,
        NULL   AS referral_name
    FROM transactions_deals
    WHERE user_from = :user_id
      AND type = 'deal'

    UNION ALL

    SELECT
        'deal' AS kind,
        id,
        created_at,
        amount,
        NULL   AS type,
        'sell' AS direction,
        announ_type,
        NULL   AS referral_name
    FROM transactions_deals
    WHERE user_to = :user_id
      AND type = 'deal'

    UNION ALL

    SELECT
        'ref'  AS kind,
        tr.id,
        tr.created_at,
        tr.amount,
        NULL   AS type,
        NULL   AS direction,
        NULL   AS announ_type,
        u.name AS referral_name
    FROM transactions_refs tr
    JOIN users u ON u.user_id = tr.user_from
    WHERE tr.user_to = :user_id

    ORDER BY created_at DESC, id DESC
    LIMIT :limit
""")

_SQL_TRANSACTIONS_WITH_CURSOR = text("""
    SELECT
        'io'   AS kind,
        id,
        created_at,
        amount,
        type,
        NULL   AS direction,
        NULL   AS announ_type,
        NULL   AS referral_name
    FROM transactions_io
    WHERE user_id = :user_id
      AND (created_at, id) < (:cursor_ts, :cursor_id)

    UNION ALL

    SELECT
        'deal' AS kind,
        id,
        created_at,
        amount,
        NULL   AS type,
        'buy'  AS direction,
        announ_type,
        NULL   AS referral_name
    FROM transactions_deals
    WHERE user_from = :user_id
      AND type = 'deal'
      AND (created_at, id) < (:cursor_ts, :cursor_id)

    UNION ALL

    SELECT
        'deal' AS kind,
        id,
        created_at,
        amount,
        NULL   AS type,
        'sell' AS direction,
        announ_type,
        NULL   AS referral_name
    FROM transactions_deals
    WHERE user_to = :user_id
      AND type = 'deal'
      AND (created_at, id) < (:cursor_ts, :cursor_id)

    UNION ALL

    SELECT
        'ref'  AS kind,
        tr.id,
        tr.created_at,
        tr.amount,
        NULL   AS type,
        NULL   AS direction,
        NULL   AS announ_type,
        u.name AS referral_name
    FROM transactions_refs tr
    JOIN users u ON u.user_id = tr.user_from
    WHERE tr.user_to = :user_id
      AND (tr.created_at, tr.id) < (:cursor_ts, :cursor_id)

    ORDER BY created_at DESC, id DESC
    LIMIT :limit
""")


class ProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_balance(self, user_id: int) -> RowMapping:
        logger.info("Запрос баланса | user_id=%s", user_id)
        try:
            result = await self._session.execute(
                text("SELECT current_balance, frozen_balance FROM users WHERE user_id = :user_id"),
                {"user_id": user_id},
            )
            row = result.mappings().one_or_none()
        except Exception as e:
            logger.error("Ошибка запроса баланса | user_id=%s | error=%s", user_id, str(e))
            raise RepositoryError(f"get_balance: {e}") from e

        if row is None:
            logger.warning("Пользователь не найден | user_id=%s", user_id)
            raise NotFoundError(f"user_not_found user_id={user_id}")

        return row

    async def get_wallpaper(self, user_id: int) -> RowMapping:
        logger.info("Запрос обоев пользователя | user_id=%s", user_id)
        try:
            result = await self._session.execute(
                text("""
                    SELECT u.wallpaper_id, w.img_key
                    FROM users u
                    LEFT JOIN wallpapers w ON w.id = u.wallpaper_id
                    WHERE u.user_id = :user_id
                """),
                {"user_id": user_id},
            )
            row = result.mappings().one_or_none()
        except Exception as e:
            logger.error("Ошибка запроса обоев пользователя | user_id=%s | error=%s", user_id, str(e))
            raise RepositoryError(f"get_wallpaper: {e}") from e

        if row is None:
            logger.warning("Пользователь не найден | user_id=%s", user_id)
            raise NotFoundError(f"user_not_found user_id={user_id}")

        return row

    async def get_transactions(
        self,
        user_id: int,
        limit: int,
        cursor_ts: datetime | None,
        cursor_id: int | None,
    ) -> list[RowMapping]:
        logger.info("Запрос транзакций | user_id=%s | cursor_ts=%s | cursor_id=%s", user_id, cursor_ts, cursor_id)
        if cursor_ts is not None:
            sql = _SQL_TRANSACTIONS_WITH_CURSOR
            params = {"user_id": user_id, "limit": limit, "cursor_ts": cursor_ts, "cursor_id": cursor_id}
        else:
            sql = _SQL_TRANSACTIONS
            params = {"user_id": user_id, "limit": limit}
        try:
            result = await self._session.execute(sql, params)
            return list(result.mappings().all())
        except Exception as e:
            logger.error("Ошибка запроса транзакций | user_id=%s | error=%s", user_id, str(e))
            raise RepositoryError(f"get_transactions: {e}") from e

    async def update_wallpaper(self, user_id: int, wallpaper_id: int) -> None:
        logger.info("Обновление обоев пользователя | user_id=%s | wallpaper_id=%s", user_id, wallpaper_id)
        try:
            await self._session.execute(
                text("UPDATE users SET wallpaper_id = :wallpaper_id WHERE user_id = :user_id"),
                {"user_id": user_id, "wallpaper_id": wallpaper_id},
            )
            await self._session.commit()
        except Exception as e:
            logger.error("Ошибка обновления обоев | user_id=%s | error=%s", user_id, str(e))
            raise RepositoryError(f"update_wallpaper: {e}") from e
