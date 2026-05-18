from collections.abc import Sequence

from sqlalchemy import text, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import RepositoryError
from app.logger import get_logger

logger = get_logger(__name__)


class DictionariesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_wallpapers(self) -> Sequence[RowMapping]:
        logger.info("Запрос обоев")
        try:
            result = await self._session.execute(
                text("SELECT wallpaper_name, img_key FROM wallpapers ORDER BY id")
            )
            return result.mappings().all()
        except Exception as e:
            logger.error("Ошибка запроса обоев | error=%s", str(e))
            raise RepositoryError(f"get_wallpapers: {e}") from e
