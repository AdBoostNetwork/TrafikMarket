from sqlalchemy.ext.asyncio import AsyncSession

from updater.scheduler.logger import get_logger
from updater.rabbitmq_schemas import MaxdashUpdateTask
from updater.scheduler.repositories.maxdash_repository import (
    get_max_channels,
    get_max_chns_nets,
    get_max_ads,
    get_max_net_ads,
)
from updater.scheduler.services.utils import build_single_tasks, build_network_tasks

logger = get_logger(__name__)


async def build_maxdash_tasks(session: AsyncSession) -> list[MaxdashUpdateTask]:
    logger.info("Формирование задач maxdash")

    max_channels = await get_max_channels(session)
    max_chns_nets = await get_max_chns_nets(session)
    max_ads = await get_max_ads(session)
    max_net_ads = await get_max_net_ads(session)

    tasks: list[MaxdashUpdateTask] = [
        *build_single_tasks(max_channels, MaxdashUpdateTask),
        *build_network_tasks(max_chns_nets, MaxdashUpdateTask),
        *build_single_tasks(max_ads, MaxdashUpdateTask),
        *build_network_tasks(max_net_ads, MaxdashUpdateTask),
    ]

    logger.info("Сформировано задач maxdash: %d", len(tasks))
    return tasks
