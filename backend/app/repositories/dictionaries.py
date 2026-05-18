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

    async def get_countries(self) -> Sequence[RowMapping]:
        logger.info("Запрос стран")
        try:
            result = await self._session.execute(
                text("SELECT id, country_name AS name FROM countries ORDER BY id")
            )
            return result.mappings().all()
        except Exception as e:
            logger.error("Ошибка запроса стран | error=%s", str(e))
            raise RepositoryError(f"get_countries: {e}") from e

    async def get_topics(self) -> Sequence[RowMapping]:
        logger.info("Запрос тематик")
        try:
            result = await self._session.execute(
                text("SELECT id, topic_name AS name FROM topics ORDER BY id")
            )
            return result.mappings().all()
        except Exception as e:
            logger.error("Ошибка запроса тематик | error=%s", str(e))
            raise RepositoryError(f"get_topics: {e}") from e

    async def get_platforms(self) -> Sequence[RowMapping]:
        logger.info("Запрос платформ")
        try:
            result = await self._session.execute(
                text("SELECT id, platform_name AS name FROM platforms ORDER BY id")
            )
            return result.mappings().all()
        except Exception as e:
            logger.error("Ошибка запроса платформ | error=%s", str(e))
            raise RepositoryError(f"get_platforms: {e}") from e

    async def get_traffic_types(self) -> Sequence[RowMapping]:
        logger.info("Запрос типов трафика")
        try:
            result = await self._session.execute(
                text("SELECT id, traffic_type_name AS name FROM traffic_types ORDER BY id")
            )
            return result.mappings().all()
        except Exception as e:
            logger.error("Ошибка запроса типов трафика | error=%s", str(e))
            raise RepositoryError(f"get_traffic_types: {e}") from e

    async def get_audience_types(self) -> Sequence[RowMapping]:
        logger.info("Запрос типов аудитории")
        try:
            result = await self._session.execute(
                text("SELECT id, type_name AS name FROM audience_types ORDER BY id")
            )
            return result.mappings().all()
        except Exception as e:
            logger.error("Ошибка запроса типов аудитории | error=%s", str(e))
            raise RepositoryError(f"get_audience_types: {e}") from e
