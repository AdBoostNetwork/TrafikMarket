#Файл с функциями БД

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from .app_config import DbConfig
from .logger import get_logger


logger = get_logger(__name__)

engine = create_async_engine(
    f'postgresql+asyncpg://{DbConfig.admin}:{DbConfig.password}@{DbConfig.host}:{DbConfig.port}/{DbConfig.db_name}',
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session

async def get_profile_info_db(user_id: int):
    logger.info("Запрос данных профиля | user_id: %s", user_id)

    query = text("""
                 SELECT a.name,
                        a.avatar_filename,
                        a.current_balance,
                        a.success_count,
                        (SELECT COUNT(*)
                         FROM deals d
                         WHERE d.seller_id = :user_id
                            OR d.buyer_id = :user_id) AS deals_count
                 FROM accounts a
                 WHERE a.user_id = :user_id
                 """)

    async with new_session() as session:
        result = await session.execute(query, {"user_id": user_id})
        data = result.mappings().first()

        return data