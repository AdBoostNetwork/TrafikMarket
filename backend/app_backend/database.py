#Файл с функциями БД

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app_config import DbConfig


engine = create_async_engine(
    f'postgresql+asyncpg://{DbConfig.admin}:{DbConfig.password}@{DbConfig.host}:{DbConfig.port}/{DbConfig.database}',
)


def get_profile_info_db(user_id: int):
    ...