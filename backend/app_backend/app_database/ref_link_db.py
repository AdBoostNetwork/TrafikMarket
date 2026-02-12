from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from ..app_config import DbConfig
from ..logger import get_logger


logger = get_logger(__name__)

engine = create_async_engine(
    f'postgresql+asyncpg://{DbConfig.admin}:{DbConfig.password}@{DbConfig.host}:{DbConfig.port}/{DbConfig.db_name}')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


async def get_ref_link_db(user_id: int):
    logger.info("Запрос реферальной ссылки пользователя | user_id: %s", user_id)

    query = text("SELECT accounts.ref_link FROM accounts WHERE accounts.user_id = :user_id")

    async with new_session() as session:
        result = await session.execute(query, {"user_id": user_id})

        ref_link = result.scalar_one_or_none()
        if ref_link is None:
            raise Exception("ref_link not found")

        return ref_link