from config import DB_CONFIG
from classes import Appeal
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text


async def get_session():
    async with new_session() as session:
        yield session


engine = create_async_engine(f"postgresql+asyncpg://{DB_CONFIG.admin}:{DB_CONFIG.password}@{DB_CONFIG.host}:{DB_CONFIG.port}/{DB_CONFIG.db_name}")

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_appeal_buy_id(user_from_id):
    query = text("SELECT user_from_id, last_msg, chat, status FROM appeals WHERE user_from_id = :user_from_id")

    async with new_session() as session:
        result = await session.execute(query, {"user_from_id": user_from_id})

        appeal = result.mappings().first()

        return Appeal(
            appeal["user_from_id"],
            appeal["last_msg"],
            appeal["chat"],
            appeal["status"]
        )