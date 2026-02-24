from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from .main_bot_config import db_info
from backend.classes import UserCreateSchema
from backend.logger import get_logger


logger = get_logger(__name__)

engine = create_async_engine(
    f'postgresql+asyncpg://{db_info.admin}:{db_info.password}@{db_info.host}:{db_info.port}/{db_info.db_name}')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def is_new_user_db(user_id: int):
    logger.info(f"Проверка существования пользователя | user_id: {user_id}")

    query = text(
        """
        SELECT name, avatar_filename
        FROM accounts
        WHERE user_id = :user_id
        """
    )

    async with new_session() as session:
        result = await session.execute(query, {"user_id": user_id})
        row = result.mappings().one_or_none()

        if row is None:
            logger.info(f"Пользователя нет в БД | user_id: {user_id}")
            return True, None, None

        logger.info(f"Пользователь есть в бд | user_id: {user_id}, name: {row.name}")
        return False, row["name"], row["avatar_filename"]


async def save_new_user_db(user_data: UserCreateSchema):
    logger.info(f"Сохранение нового пользователя в БД | user_id: {user_data.user_id}")

    query = text(
        """
        INSERT INTO accounts (user_id, name, reg_date, avatar_filename, ref_link, referrer_id)
        VALUES (:user_id, :name, :reg_date, :avatar_filename, :ref_link, :referrer_id)
        """
    )

    try:
        async with new_session() as session:
            await session.execute(
                query,
                {
                    "user_id": user_data.user_id,
                    "name": user_data.name,
                    "reg_date": user_data.registration_date,
                    "avatar_filename": user_data.avatar_id,
                    "ref_link": user_data.ref_link,
                    "referrer_id": user_data.referi_id,
                },
            )
            await session.commit()
            logger.info(f"Пользователь успешно сохранен в БД | user_id: {user_data.user_id}")
            return True

    except Exception as e:
        logger.exception(f"Ошибка при сохранении нового пользотвателя в БД | user_id: {user_data.user_id} | Ошибка: {str(e)}")
        return False


async def change_avatar_id_db(user_id: int, new_avatar_id: int):
    logger.info(f"Смена аватарки пользователя | user_id: {user_id}")

    query = text(
        """
        UPDATE accounts
        SET avatar_filename = :avatar_filename
        WHERE user_id = :user_id
        """
    )
    try:
        async with new_session() as session:

            await session.execute(query,{"user_id": user_id, "avatar_filename": new_avatar_id})
            await session.commit()
            logger.info(f"Аватарка успешно обновлена | user_id: {user_id}")
            return True

    except Exception as e:
        logger.exception(f"Ошибка при смене аватарки пользователя | user_id: {user_id} | Ошибка: {str(e)}")
        return False


async def change_name_db(user_id: int, new_name: str):
    logger.info(f"Смена имени пользователя | user_id: {user_id}")

    query = text(
        """
        UPDATE accounts
        SET name = :name
        WHERE user_id = :user_id
        """
    )

    try:
        async with new_session() as session:
            await session.execute(query, {"user_id": user_id, "name": new_name})
            await session.commit()
            logger.info(f"Имя успешно обновлено | user_id: {user_id}")
            return True

    except Exception as e:
        logger.exception(f"Ошибка при смене имени пользователя | user_id: {user_id} | Ошибка: {str(e)}")
        return False