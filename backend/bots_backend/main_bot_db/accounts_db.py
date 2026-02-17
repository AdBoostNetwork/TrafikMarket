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
        WHERE user_id = :user_id;
        """
    )

    async with new_session() as session:
        result = await session.execute(query, {"user_id": user_id})
        row = result.mappings().one_or_none()

        if row is None:
            return False, None

        return True, int(row["avatar_filename"])


def save_new_user_db(user_id, name, tg_username, avatar_id) -> bool:
    """
    Сохраняет новый акк в БД, возвращает False в смлучае ошибки, True если все норм
    :param user_id:
    :param name:
    :param tg_username:
    :param avatar_id:
    :return:
    """
    return True
