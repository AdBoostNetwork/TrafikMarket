from pydantic import BaseModel


class BalanceResponse(BaseModel):
    """Свободный баланс пользователя"""
    free_balance: float


class WallpaperCurrentResponse(BaseModel):
    """Текущие обои пользователя"""
    wallpaper_id: int | None
    img_key: str | None


class WallpaperUpdateRequest(BaseModel):
    """Запрос на изменение обоев пользователя"""
    wallpaper_id: int
