from collections.abc import Sequence

from sqlalchemy import text, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from updater.scheduler.logger import get_logger
from updater.scheduler.core.errors import RepositoryError

logger = get_logger(__name__)


async def get_max_channels(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка max_channels для maxdash")
    query = text(
        """
        SELECT a.announ_id, mc.link
        FROM announs a
        JOIN max_channels mc ON mc.chn_announ_id = a.announ_id
        WHERE a.maxdash_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки max_channels | %s", str(e))
        raise RepositoryError(f"get_max_channels: {e}") from e


async def get_max_chns_nets(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка max_chns_nets для maxdash")
    query = text(
        """
        SELECT a.announ_id, mcnl.id AS link_id, mcnl.link AS url
        FROM announs a
        JOIN max_chns_nets_links mcnl ON mcnl.net_announ_id = a.announ_id
        WHERE a.maxdash_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки max_chns_nets | %s", str(e))
        raise RepositoryError(f"get_max_chns_nets: {e}") from e


async def get_max_ads(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка max_ads для maxdash")
    query = text(
        """
        SELECT a.announ_id, ma.link
        FROM announs a
        JOIN max_ads ma ON ma.ad_id = a.announ_id
        WHERE a.maxdash_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки max_ads | %s", str(e))
        raise RepositoryError(f"get_max_ads: {e}") from e


async def get_max_net_ads(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка max_net_ads для maxdash")
    query = text(
        """
        SELECT a.announ_id, mnal.id AS link_id, mnal.link AS url
        FROM announs a
        JOIN max_net_ads_links mnal ON mnal.ad_id = a.announ_id
        WHERE a.maxdash_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки max_net_ads | %s", str(e))
        raise RepositoryError(f"get_max_net_ads: {e}") from e
