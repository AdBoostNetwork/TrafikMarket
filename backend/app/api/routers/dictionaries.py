from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.dictionaries import DictionaryItemResponse, WallpaperResponse
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


@router.get("/countries", response_model=list[DictionaryItemResponse], summary="Получение списка стран")
async def get_countries(session: AsyncSession = Depends(get_session)) -> list[DictionaryItemResponse]:
    try:
        repo = DictionariesRepository(session)
        service = DictionariesService(repo)
        return await service.get_countries()
    except RepositoryError as e:
        logger.error("get_countries db_error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="db_error")
    except Exception as e:
        logger.error("get_countries error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="internal_error")


@router.get("/topics", response_model=list[DictionaryItemResponse], summary="Получение списка тематик")
async def get_topics(session: AsyncSession = Depends(get_session)) -> list[DictionaryItemResponse]:
    try:
        repo = DictionariesRepository(session)
        service = DictionariesService(repo)
        return await service.get_topics()
    except RepositoryError as e:
        logger.error("get_topics db_error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="db_error")
    except Exception as e:
        logger.error("get_topics error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="internal_error")


@router.get("/platforms", response_model=list[DictionaryItemResponse], summary="Получение списка платформ")
async def get_platforms(session: AsyncSession = Depends(get_session)) -> list[DictionaryItemResponse]:
    try:
        repo = DictionariesRepository(session)
        service = DictionariesService(repo)
        return await service.get_platforms()
    except RepositoryError as e:
        logger.error("get_platforms db_error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="db_error")
    except Exception as e:
        logger.error("get_platforms error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="internal_error")


@router.get("/traffic-types", response_model=list[DictionaryItemResponse], summary="Получение списка типов трафика")
async def get_traffic_types(session: AsyncSession = Depends(get_session)) -> list[DictionaryItemResponse]:
    try:
        repo = DictionariesRepository(session)
        service = DictionariesService(repo)
        return await service.get_traffic_types()
    except RepositoryError as e:
        logger.error("get_traffic_types db_error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="db_error")
    except Exception as e:
        logger.error("get_traffic_types error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="internal_error")


@router.get("/audience-types", response_model=list[DictionaryItemResponse], summary="Получение списка типов аудитории")
async def get_audience_types(session: AsyncSession = Depends(get_session)) -> list[DictionaryItemResponse]:
    try:
        repo = DictionariesRepository(session)
        service = DictionariesService(repo)
        return await service.get_audience_types()
    except RepositoryError as e:
        logger.error("get_audience_types db_error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="db_error")
    except Exception as e:
        logger.error("get_audience_types error | error=%s", str(e))
        raise HTTPException(status_code=500, detail="internal_error")
