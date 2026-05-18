from app.api.schemas.dictionaries import WallpaperResponse
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
