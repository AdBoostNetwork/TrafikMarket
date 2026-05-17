import asyncio
import os
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from updater.scheduler.logger import get_logger
from updater.scheduler.core.errors import RepositoryError, PublishError
from updater.scheduler.db.session import make_session
from updater.scheduler.messaging.rabbitmq_client import connect, publish_task, TGSTAT_QUEUE, MAXDASH_QUEUE
from updater.scheduler.services.maxdash_service import build_maxdash_tasks
from updater.scheduler.services.tgstat_service import build_tgstat_tasks

logger = get_logger(__name__)

TZ_UTC3 = timezone(timedelta(hours=3))


def _seconds_until_next_run(target_hour: int) -> float:
    now = datetime.now(tz=TZ_UTC3)
    next_run = now.replace(hour=target_hour, minute=0, second=0, microsecond=0)
    if next_run <= now:
        next_run += timedelta(days=1)
    return (next_run - now).total_seconds()


async def _run_once(session: AsyncSession, channel) -> None:
    tgstat_tasks = await build_tgstat_tasks(session)
    for task in tgstat_tasks:
        await publish_task(channel, task, TGSTAT_QUEUE)

    maxdash_tasks = await build_maxdash_tasks(session)
    for task in maxdash_tasks:
        await publish_task(channel, task, MAXDASH_QUEUE)

    logger.info(
        "Публикация завершена | tgstat: %d | maxdash: %d",
        len(tgstat_tasks),
        len(maxdash_tasks),
    )


async def run_scheduler() -> None:
    target_hour = int(os.environ["SCHEDULER_RUN_HOUR"])
    logger.info("Запуск планировщика | target_hour=%d UTC+3", target_hour)

    while True:
        seconds = _seconds_until_next_run(target_hour)
        logger.info("Следующий запуск через %.0f секунд", seconds)
        await asyncio.sleep(seconds)

        session_factory = make_session()
        connection = await connect()
        try:
            async with session_factory() as session:
                channel = await connection.channel()
                await _run_once(session, channel)
        except (RepositoryError, PublishError) as e:
            logger.error("Ошибка в цикле планировщика | %s", str(e))
        finally:
            await connection.close()
