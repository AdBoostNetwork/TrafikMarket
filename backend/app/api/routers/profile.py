from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.common import SuccessResponse
from app.api.schemas.profile import BalanceResponse, WallpaperCurrentResponse, WallpaperUpdateRequest
from app.core.errors import NotFoundError, RepositoryError
from app.db.dependencies import get_session
from app.logger import get_logger
from app.repositories.profile import ProfileRepository
from app.services.profile import ProfileService

logger = get_logger(__name__)

router = APIRouter(prefix="/profile", tags=["Профиль"])


@router.get("/balance", response_model=BalanceResponse, summary="Получение баланса пользователя")
async def get_balance(user_id: int, session: AsyncSession = Depends(get_session)) -> BalanceResponse:
    try:
        repo = ProfileRepository(session)
        service = ProfileService(repo)
        return await service.get_balance(user_id)
    except NotFoundError as e:
        logger.error("get_balance not_found | user_id=%s | error=%s", user_id, str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        logger.error("get_balance db_error | user_id=%s | error=%s", user_id, str(e))
        raise HTTPException(status_code=500, detail="db_error")
    except Exception as e:
        logger.error("get_balance error | user_id=%s | error=%s", user_id, str(e))
        raise HTTPException(status_code=500, detail="internal_error")


@router.get("/wallpaper", response_model=WallpaperCurrentResponse, summary="Получение текущих обоев пользователя")
async def get_wallpaper(user_id: int, session: AsyncSession = Depends(get_session)) -> WallpaperCurrentResponse:
    try:
        repo = ProfileRepository(session)
        service = ProfileService(repo)
        return await service.get_wallpaper(user_id)
    except NotFoundError as e:
        logger.error("get_wallpaper not_found | user_id=%s | error=%s", user_id, str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        logger.error("get_wallpaper db_error | user_id=%s | error=%s", user_id, str(e))
        raise HTTPException(status_code=500, detail="db_error")
    except Exception as e:
        logger.error("get_wallpaper error | user_id=%s | error=%s", user_id, str(e))
        raise HTTPException(status_code=500, detail="internal_error")


@router.put("/wallpaper", response_model=SuccessResponse, summary="Изменение текущих обоев пользователя")
async def update_wallpaper(user_id: int, data: WallpaperUpdateRequest, session: AsyncSession = Depends(get_session)) -> SuccessResponse:
    try:
        repo = ProfileRepository(session)
        service = ProfileService(repo)
        return await service.update_wallpaper(user_id, data)
    except RepositoryError as e:
        logger.error("update_wallpaper db_error | user_id=%s | error=%s", user_id, str(e))
        raise HTTPException(status_code=500, detail="db_error")
    except Exception as e:
        logger.error("update_wallpaper error | user_id=%s | error=%s", user_id, str(e))
        raise HTTPException(status_code=500, detail="internal_error")
