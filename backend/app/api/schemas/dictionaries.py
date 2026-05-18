from pydantic import BaseModel


class WallpaperResponse(BaseModel):
    """Объект обоев интерфейса mini app"""
    wallpaper_name: str
    img_key: str


class DictionaryItemResponse(BaseModel):
    """Элемент справочника (страна, тематика, платформа, тип трафика, тип аудитории)"""
    id: int
    name: str
