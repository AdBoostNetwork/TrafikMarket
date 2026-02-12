from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from ..app_config import DbConfig
from ..app_classes import ChannelSchema
from ..logger import get_logger


logger = get_logger(__name__)

engine = create_async_engine(
    f'postgresql+asyncpg://{DbConfig.admin}:{DbConfig.password}@{DbConfig.host}:{DbConfig.port}/{DbConfig.db_name}')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


async def get_channel_announ_db(session, announ_id: int):
    logger.info("Получение объявления канала | Announ id: %s", announ_id)

    query = text(
        """
        SELECT a.seller_id,
               a.title,
               a.price,
               a.short_text,
               a.long_text,

               c.topic,
               c.chn_type,
               c.country,
               c.subs_count,
               c.cover_count,
               c.profit
        FROM announs a
                 JOIN channels c
                      ON c.chn_announ_id = a.announ_id
        WHERE a.announ_id = :announ_id;
        """
    )

    result = await session.execute(query, {"announ_id": announ_id})
    row = result.mappings().one_or_none()

    if row is None:
        logger.warning("Объявление канала не найдено | announ_id=%s", announ_id)
        raise Exception(f"channel_announ_not_found announ_id={announ_id}")

    seller = await get_seller_info_db(session, int(row["seller_id"]))
    imgs = await get_announ_imgs_db(session, announ_id)

    cover_count = float(row["cover_count"])
    profit = float(row["profit"])

    return ChannelSchema(
        seller=seller,
        title=row["title"],
        price=int(row["price"]),
        short_text=row["short_text"],
        long_text=row["long_text"],
        imgs=imgs,
        topic=row["topic"],
        chn_type=row["chn_type"],
        country=row["country"],
        subs_count=int(row["subs_count"]),
        cover_count=cover_count,
        profit=profit,
    )


async def get_announ_type_db(session, announ_id: int):
    logger.info("Получение типа объявления | Announ id: %s", announ_id)

    query = text("SELECT type FROM announs WHERE announ_id = :announ_id")

    result = await session.execute(query, {"announ_id": announ_id})

    announ_type = result.scalar_one_or_none()

    if announ_type is None:
        logger.warning("Тип объявления не найден | announ_id=%s", announ_id)
        raise Exception("announ not found")

    return announ_type


async def get_announ_info_db(session, announ_id: int, announ_type: int):

    if announ_type == "channel":
        return await get_channel_announ_db(session, announ_id)
    if announ_type == "ad":
        return await get_ad_announ_db(session, announ_id)
    if announ_type == "traffic":
        return await get_traffic_announ_db(session, announ_id)
    if announ_type == "account":
        return await get_account_announ_db(session, announ_id)

    raise Exception({"error": "unknown announ type"})


async def get_announ_page_db(announ_id: int):
    logger.info("Получение данных страницы объявления | Announ id: %s", announ_id)

    async with new_session() as session:
        announ_type = await get_announ_type_db(session, announ_id)
        announ_info = await get_announ_info_db(session, announ_id, announ_type)
