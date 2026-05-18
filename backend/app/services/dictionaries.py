from app.api.schemas.dictionaries import DictionaryItemResponse, WallpaperResponse
from app.logger import get_logger
from app.repositories.dictionaries import DictionariesRepository

logger = get_logger(__name__)


class DictionariesService:
    def __init__(self, repo: DictionariesRepository) -> None:
        self._repo = repo

    async def get_wallpapers(self) -> list[WallpaperResponse]:
        logger.info("Получение обоев")
        rows = await self._repo.get_wallpapers()
        return [WallpaperResponse(wallpaper_name=row["wallpaper_name"], img_key=row["img_key"]) for row in rows]

    async def get_countries(self) -> list[DictionaryItemResponse]:
        logger.info("Получение стран")
        rows = await self._repo.get_countries()
        return [DictionaryItemResponse(id=row["id"], name=row["name"]) for row in rows]

    async def get_topics(self) -> list[DictionaryItemResponse]:
        logger.info("Получение тематик")
        rows = await self._repo.get_topics()
        return [DictionaryItemResponse(id=row["id"], name=row["name"]) for row in rows]

    async def get_platforms(self) -> list[DictionaryItemResponse]:
        logger.info("Получение платформ")
        rows = await self._repo.get_platforms()
        return [DictionaryItemResponse(id=row["id"], name=row["name"]) for row in rows]

    async def get_traffic_types(self) -> list[DictionaryItemResponse]:
        logger.info("Получение типов трафика")
        rows = await self._repo.get_traffic_types()
        return [DictionaryItemResponse(id=row["id"], name=row["name"]) for row in rows]

    async def get_audience_types(self) -> list[DictionaryItemResponse]:
        logger.info("Получение типов аудитории")
        rows = await self._repo.get_audience_types()
        return [DictionaryItemResponse(id=row["id"], name=row["name"]) for row in rows]
