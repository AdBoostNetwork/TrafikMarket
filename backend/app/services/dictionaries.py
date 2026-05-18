from app.api.schemas.dictionaries import DictionaryItemResponse, WallpaperResponse
from app.logger import get_logger
from app.repositories.dictionaries import DictionariesRepository

logger = get_logger(__name__)


class DictionariesService:
    def __init__(self, repo: DictionariesRepository) -> None:
        self._repo = repo

    @staticmethod
    def _map_items(rows) -> list[DictionaryItemResponse]:
        return [DictionaryItemResponse(id=row["id"], name=row["name"]) for row in rows]

    async def get_wallpapers(self) -> list[WallpaperResponse]:
        logger.info("Получение обоев")
        rows = await self._repo.get_wallpapers()
        return [WallpaperResponse(id=row["id"], wallpaper_name=row["wallpaper_name"], img_key=row["img_key"]) for row in rows]

    async def get_countries(self) -> list[DictionaryItemResponse]:
        logger.info("Получение стран")
        return self._map_items(await self._repo.get_countries())

    async def get_topics(self) -> list[DictionaryItemResponse]:
        logger.info("Получение тематик")
        return self._map_items(await self._repo.get_topics())

    async def get_platforms(self) -> list[DictionaryItemResponse]:
        logger.info("Получение платформ")
        return self._map_items(await self._repo.get_platforms())

    async def get_traffic_types(self) -> list[DictionaryItemResponse]:
        logger.info("Получение типов трафика")
        return self._map_items(await self._repo.get_traffic_types())

    async def get_audience_types(self) -> list[DictionaryItemResponse]:
        logger.info("Получение типов аудитории")
        return self._map_items(await self._repo.get_audience_types())
