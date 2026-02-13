from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from ..app_config import DbConfig
from ..app_classes import SellerInfo, ChannelSchema, AdSchema, TrafficSchema, AccSchema
from ..logger import get_logger


logger = get_logger(__name__)

engine = create_async_engine(
    f'postgresql+asyncpg://{DbConfig.admin}:{DbConfig.password}@{DbConfig.host}:{DbConfig.port}/{DbConfig.db_name}')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


async def get_seller_info_db(session, seller_id: int):
    logger.info("Получение данных продавца | seller_id: %s", seller_id)

    query = text(
        """SELECT a.name, a.success_count,
            (SELECT COUNT(*) FROM deals d WHERE d.seller_id = :seller_id) AS deals_count
           FROM accounts a WHERE a.user_id = :seller_id""")

    result = await session.execute(query, {"seller_id": seller_id})
    row = result.mappings().first()

    if row is None:
        raise Exception(f"seller_not_found seller_id={seller_id}")

    success_count = int(row["success_count"])
    deals_count = int(row["deals_count"])

    success_deals_percent = int(success_count * 100 / deals_count) if deals_count else 0

    return SellerInfo(
        name=row["name"],
        deals_count=deals_count,
        success_deals_percent=success_deals_percent,
    )


async def get_announ_imgs_db(session, announ_id: int):
    logger.info("Получение картинок объявления | Announ id: %s", announ_id)

    query = text("SELECT img_filename FROM imgs WHERE img_announ_id = :announ_id ORDER BY img_id")

    result = await session.execute(query, {"announ_id": announ_id})
    rows = result.scalars().all()

    return list(rows) if rows else []



async def get_account_announ_db(session, announ_id: int):
    logger.info("Получение объявления (Аккаунты) | Announ id: %s", announ_id)

    query = text(
        """
        SELECT a.seller_id,
               a.title,
               a.price,
               a.short_text,
               a.long_text,

               ac.country,
               ac.log_type,
               ac.idle_time,
               ac.acc_type,
               ac.premium,
               ac.stars_count,
               ac.gifts,
               ac.tg_level
        FROM announs a
                 JOIN accs_announs ac
                      ON ac.acc_announ_id = a.announ_id
        WHERE a.announ_id = :announ_id;
        """
    )

    result = await session.execute(query, {"announ_id": announ_id})
    row = result.mappings().one_or_none()

    if row is None:
        logger.warning("Объявление (Аккаунты) не найдено | announ_id=%s", announ_id)
        raise Exception(f"account_announ_not_found announ_id={announ_id}")

    seller = await get_seller_info_db(session, int(row["seller_id"]))
    imgs = await get_announ_imgs_db(session, announ_id)

    return AccSchema(
        seller=seller,
        title=row["title"],
        price=int(row["price"]),
        short_text=row["short_text"],
        long_text=row["long_text"],
        imgs=imgs,
        country=row["country"],
        log_type=row["log_type"],
        idle_time=row["idle_time"],
        acc_type=row["acc_type"],
        premium=row["premium"],
        stars_count=row["stars_count"],
        gifts=bool(row["gifts"]),
        tg_level=int(row["tg_level"]),
    )


async def get_traffic_announ_db(session, announ_id: int):
    logger.info("Получение объявления (Трафик) | Announ id: %s", announ_id)

    query = text(
        """
        SELECT a.seller_id,
               a.title,
               a.price,
               a.short_text,
               a.long_text,

               t.topic,
               t.platform,
               t.traffic_type,
               t.audience_type,
               t.country
        FROM announs a
                 JOIN traffic t
                      ON t.trf_announ_id = a.announ_id
        WHERE a.announ_id = :announ_id;
        """
    )

    result = await session.execute(query, {"announ_id": announ_id})
    row = result.mappings().one_or_none()

    if row is None:
        logger.warning("Объявление (Трафик) не найдено | announ_id=%s", announ_id)
        raise Exception(f"traffic_announ_not_found announ_id={announ_id}")

    seller = await get_seller_info_db(session, int(row["seller_id"]))
    imgs = await get_announ_imgs_db(session, announ_id)

    return TrafficSchema(
        seller=seller,
        title=row["title"],
        price=int(row["price"]),
        short_text=row["short_text"],
        long_text=row["long_text"],
        imgs=imgs,
        topic=row["topic"],
        platform=row["platform"],
        traffic_type=row["traffic_type"],
        audience_type=row["audience_type"],
        country=row["country"],
    )


async def get_ad_announ_db(session, announ_id: int):
    logger.info("Получение объявления рекламы | Announ id: %s", announ_id)

    query = text(
        """
        SELECT a.seller_id,
               a.title,
               a.price,
               a.short_text,
               a.long_text,

               ad.topic,
               ad.country,
               ad.cover,
               ad.cpm,
               ad.er
        FROM announs a
                 JOIN ads ad
                      ON ad.ad_announ_id = a.announ_id
        WHERE a.announ_id = :announ_id;
        """
    )

    result = await session.execute(query, {"announ_id": announ_id})
    row = result.mappings().one_or_none()

    if row is None:
        logger.warning("Объявление (Реклама) не найдено | announ_id=%s", announ_id)
        raise Exception(f"ad_announ_not_found announ_id={announ_id}")

    seller = await get_seller_info_db(session, int(row["seller_id"]))
    imgs = await get_announ_imgs_db(session, announ_id)

    return AdSchema(
        seller=seller,
        title=row["title"],
        price=int(row["price"]),
        short_text=row["short_text"],
        long_text=row["long_text"],
        imgs=imgs,
        topic=row["topic"],
        country=row["country"],
        cover=int(row["cover"]),
        cpm=int(row["cpm"]),
        er=int(row["er"]),
    )


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


async def get_announ_info_db(session, announ_id: int, announ_type: str):

    if announ_type == "channel":
        return await get_channel_announ_db(session, announ_id)
    if announ_type == "ad":
        return await get_ad_announ_db(session, announ_id)
    if announ_type == "traffic":
        return await get_traffic_announ_db(session, announ_id)
    if announ_type == "account":
        return await get_account_announ_db(session, announ_id)

    raise Exception(f"unknown_announ_type type: {announ_type}")


async def get_announ_page_db(announ_id: int):
    logger.info("Получение данных страницы объявления | Announ id: %s", announ_id)

    async with new_session() as session:
        announ_type = await get_announ_type_db(session, announ_id)
        announ_info = await get_announ_info_db(session, announ_id, announ_type)

    return {
        "type": announ_type,
        "announ_info": announ_info,
    }