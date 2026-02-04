from .config import DB_CONFIG
from .classes import Appeal
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
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

        if not appeal:
            return "appeal_not_found"

        return Appeal(
            appeal["user_from_id"],
            appeal["last_msg"],
            appeal["chat"],
            appeal["status"]
        )


async def change_appeal(user_from_id, status, last_msg, chat_append):
    query = text("UPDATE appeals SET status = :status, last_msg = :last_msg, chat = chat || E'\n' || :chat_append WHERE user_from_id = :user_from_id")

    async with new_session() as session:
        try:
            await session.execute(query,{"user_from_id": user_from_id, "status": status, "last_msg": last_msg, "chat_append": chat_append})
            await session.commit()

            return {"success": True}

        except Exception as e:
            await session.rollback()

            return {"success": False, "error": str(e)}


async def create_appeal(data: Appeal):
    query = text("INSERT INTO appeals (user_from_id, last_msg, chat, status) VALUES (:user_from_id, :last_msg, :chat, :status)")

    async with new_session() as session:
        try:
            await session.execute(query,{"user_from_id": data.user_from_id, "last_msg": data.last_msg, "chat": data.chat, "status": data.status})
            await session.commit()

            return {"success": True}

        except Exception as e:
            await session.rollback()

            return {"success": False, "error": str(e)}