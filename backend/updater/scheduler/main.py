import asyncio

from updater.scheduler.logger import get_logger
from updater.scheduler.runner import run_scheduler

logger = get_logger(__name__)


async def main() -> None:
    try:
        await run_scheduler()
    except asyncio.CancelledError:
        logger.info("updater-scheduler остановлен")


if __name__ == "__main__":
    logger.info("updater-scheduler запущен")
    asyncio.run(main())
