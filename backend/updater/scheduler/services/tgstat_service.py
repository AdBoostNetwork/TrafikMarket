from sqlalchemy.ext.asyncio import AsyncSession

from updater.scheduler.logger import get_logger
from updater.rabbitmq_schemas import TgstatUpdateTask
from updater.scheduler.repositories.tgstat_repository import (
    get_tg_channels,
    get_tg_chns_nets,
    get_tg_ads,
    get_tg_net_ads,
    get_stories,
    get_stories_nets,
)
from updater.scheduler.services.utils import build_single_tasks, build_network_tasks

logger = get_logger(__name__)


async def build_tgstat_tasks(session: AsyncSession) -> list[TgstatUpdateTask]:
    logger.info("Формирование задач tgstat")

    tg_channels = await get_tg_channels(session)
    tg_chns_nets = await get_tg_chns_nets(session)
    tg_ads = await get_tg_ads(session)
    tg_net_ads = await get_tg_net_ads(session)
    stories = await get_stories(session)
    stories_nets = await get_stories_nets(session)

    tasks: list[TgstatUpdateTask] = [
        *build_single_tasks(tg_channels, TgstatUpdateTask),
        *build_network_tasks(tg_chns_nets, TgstatUpdateTask),
        *build_single_tasks(tg_ads, TgstatUpdateTask),
        *build_network_tasks(tg_net_ads, TgstatUpdateTask),
        *build_single_tasks(stories, TgstatUpdateTask),
        *build_network_tasks(stories_nets, TgstatUpdateTask),
    ]

    logger.info("Сформировано задач tgstat: %d", len(tasks))
    return tasks
