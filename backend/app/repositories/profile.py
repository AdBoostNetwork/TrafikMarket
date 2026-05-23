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
