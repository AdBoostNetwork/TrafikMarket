from sqlalchemy import text
from sqlalchemy.util import await_only

from backend.db_engine import new_session
from backend.app_backend.app_classes import TopicsConfig
from backend.logger import get_logger


logger = get_logger(__name__)


async def get_topics(session):
    query = text("SELECT topic FROM topics")


async def get_countries(session):
    query = text("SELECT country FROM countries")


async def get_audience_types(session):
    query = text("SELECT audience_type FROM audience_types")


async def get_platforms(session):
    query = text("SELECT platform FROM platforms")


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