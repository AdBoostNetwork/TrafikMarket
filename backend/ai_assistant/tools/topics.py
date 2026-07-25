from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ai_assistant.logger import get_logger

logger = get_logger(__name__)

_topics: list[str] = []


async def load_topics(session: AsyncSession) -> None:
    global _topics
    result = await session.execute(text("SELECT topic_name FROM topics ORDER BY id"))
    _topics = list(result.scalars().all())
    logger.info("тематики загружены | count=%s", len(_topics))


def get_topics() -> list[str]:
    return list(_topics)
