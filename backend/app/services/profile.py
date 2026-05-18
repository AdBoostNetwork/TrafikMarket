from app.api.schemas.common import SuccessResponse
from app.api.schemas.profile import BalanceResponse, WallpaperCurrentResponse, WallpaperUpdateRequest
from app.logger import get_logger
from app.repositories.profile import ProfileRepository

logger = get_logger(__name__)


class ProfileService:
    def __init__(self, repo: ProfileRepository) -> None:
        self._repo = repo

    async def get_balance(self, user_id: int) -> BalanceResponse:
        logger.info("Получение баланса | user_id=%s", user_id)
        row = await self._repo.get_balance(user_id)
        free_balance = float(row["current_balance"]) - float(row["frozen_balance"])
        return BalanceResponse(free_balance=free_balance)

    async def get_wallpaper(self, user_id: int) -> WallpaperCurrentResponse:
        logger.info("Получение обоев пользователя | user_id=%s", user_id)
        row = await self._repo.get_wallpaper(user_id)
        return WallpaperCurrentResponse(wallpaper_id=row["wallpaper_id"], img_key=row["img_key"])

    async def update_wallpaper(self, user_id: int, data: WallpaperUpdateRequest) -> SuccessResponse:
        logger.info("Изменение обоев пользователя | user_id=%s | wallpaper_id=%s", user_id, data.wallpaper_id)
        await self._repo.update_wallpaper(user_id, data.wallpaper_id)
        return SuccessResponse()
