from sqlalchemy import text

from backend.helpers.db_engine import new_session
from backend.app_backend.app_classes import TopicsConfig
from backend.logger import get_logger


logger = get_logger(__name__)


async def get_topics(session):
    logger.info("Загрузка списка тематик из БД")
    query = text("SELECT topic_name FROM topics ORDER BY topic_name")
    result = await session.execute(query)
    return list(result.scalars().all())
        

async def get_countries(session):
    logger.info("Загрузка списка стран из БД")
    query = text("SELECT country_name FROM countries ORDER BY country_name")
    result = await session.execute(query)
    return list(result.scalars().all())


async def get_audience_types(session):
    logger.info("Загрузка списка типов аудитории из БД")
    query = text("SELECT type_name FROM audience_types ORDER BY type_name")
    result = await session.execute(query)
    return list(result.scalars().all())


async def get_platforms(session):
    logger.info("Загрузка списка платформ из БД")
    query = text("SELECT platform_name FROM platforms ORDER BY platform_name")
    result = await session.execute(query)
    return list(result.scalars().all())


async def build_topic_config():

    async with new_session() as session:
        topics = await get_topics(session)
        countries = await get_countries(session)
        audience_types = await get_audience_types(session)
        platforms = await get_platforms(session)

        return TopicsConfig(
            topics=topics,
            countries=countries,
            audience_types=audience_types,
            platforms=platforms,
        )