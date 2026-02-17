from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from .main_bot_config import db_info
from backend.classes import UserCreateSchema


engine = create_async_engine(
    f'postgresql+asyncpg://{db_info.admin}:{db_info.password}@{db_info.host}:{db_info.port}/{db_info.db_name}')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def is_new_user_db(user_id: int):
    query = text(
        """
        SELECT avatar_filename
        FROM accounts
        WHERE user_id = :user_id
        """
    )

    async with new_session() as session:
        result = await session.execute(query, {"user_id": user_id})
        row = result.mappings().one_or_none()

        if row is None:
            return False, None

        return True, row["avatar_filename"]


async def save_new_user_db(user_data: UserCreateSchema):
    query = text(
        """
        INSERT INTO accounts (user_id, name, username, avatar_filename, ref_link, referrer_id)
        VALUES (:user_id, :name, :username, :avatar_filename, :ref_link, :referrer_id)
        """
    )

    try:
        async with new_session() as session:
            await session.execute(
                query,
                {
                    "user_id": user_data.user_id,
                    "name": user_data.name,
                    "username": user_data.tg_username,
                    "avatar_filename": user_data.avatar_id,
                    "ref_link": user_data.ref_link,
                    "referrer_id": user_data.referi_if,
                },
            )
            await session.commit()
            return True

    except Exception as e:
        print(str(e))
        return False