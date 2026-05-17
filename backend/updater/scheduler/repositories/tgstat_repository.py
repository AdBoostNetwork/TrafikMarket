from collections.abc import Sequence

from sqlalchemy import text, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from updater.scheduler.logger import get_logger
from updater.scheduler.core.errors import RepositoryError

logger = get_logger(__name__)


async def get_tg_channels(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка tg_channels для tgstat")
    query = text(
        """
        SELECT a.announ_id, tc.link
        FROM announs a
        JOIN tg_channels tc ON tc.chn_announ_id = a.announ_id
        WHERE a.tgstat_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки tg_channels | %s", str(e))
        raise RepositoryError(f"get_tg_channels: {e}") from e


async def get_tg_chns_nets(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка tg_chns_nets для tgstat")
    query = text(
        """
        SELECT a.announ_id, tcl.id AS link_id, tcl.link AS url
        FROM announs a
        JOIN tg_chns_nets_links tcl ON tcl.net_announ_id = a.announ_id
        WHERE a.tgstat_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки tg_chns_nets | %s", str(e))
        raise RepositoryError(f"get_tg_chns_nets: {e}") from e


async def get_tg_ads(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка tg_ads для tgstat")
    query = text(
        """
        SELECT a.announ_id, ta.link
        FROM announs a
        JOIN tg_ads ta ON ta.ad_id = a.announ_id
        WHERE a.tgstat_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки tg_ads | %s", str(e))
        raise RepositoryError(f"get_tg_ads: {e}") from e


async def get_tg_net_ads(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка tg_net_ads для tgstat")
    query = text(
        """
        SELECT a.announ_id, tnal.id AS link_id, tnal.link AS url
        FROM announs a
        JOIN tg_net_ads_links tnal ON tnal.ad_id = a.announ_id
        WHERE a.tgstat_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки tg_net_ads | %s", str(e))
        raise RepositoryError(f"get_tg_net_ads: {e}") from e


async def get_stories(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка stories для tgstat")
    query = text(
        """
        SELECT a.announ_id, s.link
        FROM announs a
        JOIN stories s ON s.story_id = a.announ_id
        WHERE a.tgstat_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки stories | %s", str(e))
        raise RepositoryError(f"get_stories: {e}") from e


async def get_stories_nets(session: AsyncSession) -> Sequence[RowMapping]:
    logger.info("Выборка stories_nets для tgstat")
    query = text(
        """
        SELECT a.announ_id, snl.id AS link_id, snl.link AS url
        FROM announs a
        JOIN stories_nets_links snl ON snl.story_id = a.announ_id
        WHERE a.tgstat_announ = true AND a.status = 'active'
        """
    )
    try:
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error("Ошибка выборки stories_nets | %s", str(e))
        raise RepositoryError(f"get_stories_nets: {e}") from e
