from sqlalchemy import text, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError, RepositoryError
from app.logger import get_logger

logger = get_logger(__name__)


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
