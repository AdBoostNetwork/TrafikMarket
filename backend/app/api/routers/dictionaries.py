from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.dictionaries import WallpaperResponse
from app.core.errors import RepositoryError
from app.db.dependencies import get_session
from app.logger import get_logger
from app.repositories.dictionaries import DictionariesRepository
from app.services.dictionaries import DictionariesService

logger = get_logger(__name__)

router = APIRouter(prefix="/dictionaries", tags=["Справочники"])


@router.get("/wallpapers", response_model=list[WallpaperResponse], summary="Получение списка обоев")
async def get_wallpapers(session: AsyncSession = Depends(get_session)) -> list[WallpaperResponse]:
    try:
        repo = DictionariesRepository(session)
        service = DictionariesService(repo)
        return await service.get_wallpapers()
    except RepositoryError as e:
        logger.error("get_wallpapers db_error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="db_error")
    except Exception as e:
        logger.error("get_wallpapers error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="internal_error")
