from pydantic import BaseModel


class WallpaperResponse(BaseModel):
    wallpaper_name: str
    img_key: str
