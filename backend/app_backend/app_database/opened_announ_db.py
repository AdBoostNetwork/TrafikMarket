from sqlalchemy import text

from backend.db_engine import new_session
from backend.app_backend.app_classes import ChannelSchema, AdSchema, TrafficSchema, AnnounPageSchema, Chart, ChartPoint
from .helpers_db import get_seller_info_db
from backend.logger import get_logger


logger = get_logger(__name__)


async def get_announ_imgs_db(session, announ_id: int):
    logger.info("Получение картинок объявления | Announ id: %s", announ_id)

    query = text("SELECT img_filename FROM imgs WHERE img_announ_id = :announ_id ORDER BY img_id")

    result = await session.execute(query, {"announ_id": announ_id})
    rows = result.scalars().all()

    return list(rows) if rows else []


async def get_traffic_announ_db(session, announ_id: int):
    logger.info("Получение объявления (Трафик) | Announ id: %s", announ_id)

    query = text(
        """
        SELECT a.article,
               a.seller_id,
               a.title,
               a.long_text,
                
               t.price,
               t.min_leads,
               t.max_leads,
               tp.topic_name AS topic,
               p.platform_name AS platform,
               tt.traffic_type_name AS traffic_type,
               at.type_name AS audience_type,
               ctr.country_name AS country
        FROM announs a
                 JOIN traffic t
                      ON t.trf_announ_id = a.announ_id
                 LEFT JOIN topics tp
                      ON tp.id = t.topic
                 LEFT JOIN platforms p
                      ON p.id = t.platform
                 LEFT JOIN traffic_types tt
                      ON tt.id = t.traffic_type
                 LEFT JOIN audience_types at
                      ON at.id = t.audience_type
                 LEFT JOIN countries ctr
                      ON ctr.id = t.country
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
        article = int(row["article"]),
        seller=seller,
        title=row["title"],
        price=int(row["price"]),
        min_leads=int(row["min_leads"]),
        max_leads=int(row["max_leads"]),
        description=row["long_text"],
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
        SELECT a.article,
               a.seller_id,
               a.title,
               a.long_text,
                
               ad.channel_link,
               t.topic_name AS topic,
               ctr.country_name AS country,
               ad.subs_count,
               ad.cover,
               ad.cpm,
               ad.er
        FROM announs a
                 JOIN ads ad
                      ON ad.ad_announ_id = a.announ_id
                 LEFT JOIN topics t
                      ON t.id = ad.topic
                 LEFT JOIN countries ctr
                      ON ctr.id = ad.country
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
        article = int(row["article"]),
        seller=seller,
        channel_link=row["channel_link"],
        title=row["title"],
        prices={"1": 2},
        description=row["long_text"],
        imgs=imgs,
        topic=row["topic"],
        country=row["country"],
        subs_count=row["subs_count"],
        cover_count=int(row["cover"]),
        cpm=int(row["cpm"]),
        er=int(row["er"]),
    )


async def get_channel_announ_db(session, announ_id: int):
    logger.info("Получение объявления канала | Announ id: %s", announ_id)

    query = text(
        """
        SELECT a.article,
               a.seller_id,
               a.title,
               a.long_text,
            
               c.channel_link, 
               t.topic_name AS topic,
               c.chn_type,
               ctr.country_name AS country,
               c.subs_count,
               c.cover_count,
               c.profit,
               c.on_requests,
               c.price,
               c.author,
               c.red_label,
               c.black_label
        FROM announs a
                 JOIN channels c
                      ON c.chn_announ_id = a.announ_id
                 LEFT JOIN topics t
                      ON t.id = c.topic
                 LEFT JOIN countries ctr
                      ON ctr.id = c.country
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

    return ChannelSchema(
        article=row["article"],
        seller=seller,
        channel_link=row["channel_link"],
        title=row["title"],
        price=float(row["price"]),
        description=row["long_text"],
        imgs=imgs,
        topic=row["topic"],
        chn_type=row["chn_type"],
        country=row["country"],
        subs_count=int(row["subs_count"]),
        cover_count=float(row["cover_count"]),
        profit=float(row["profit"]),
        on_requests=bool(row["on_requests"]),
        author=bool(row["author"]),
        red_label=bool(row["red_label"]),
        black_label=bool(row["black_label"]),
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

    raise Exception(f"unknown_announ_type type: {announ_type}")


async def get_announ_page_db(announ_id: int):
    logger.info("Получение данных страницы объявления | Announ id: %s", announ_id)

    try:
        async with new_session() as session:
            announ_type = await get_announ_type_db(session, announ_id)
            announ_info = await get_announ_info_db(session, announ_id, announ_type)

    except Exception as e:
        logger.error(f"Ошибка при получении данных объявления | announ_id: {announ_id} | error: {str(e)}")
        raise ValueError("Ошибка при получении данных объявления")

    return AnnounPageSchema(
        type=announ_type,
        announ_info=announ_info,
    )


async def get_price_chart_points_db(announ_id: int):
    logger.info(f"Запрос истории цены | announ_id: {announ_id}")

    query = text(
        """
        SELECT price_date, price
        FROM announ_price_history
        WHERE announ_id = :announ_id
        ORDER BY price_date DESC
        """
    )

    try:
        async with new_session() as session:
            result = await session.execute(query, {"announ_id": announ_id})
            rows = result.mappings().all()
    except Exception as e:
        logger.error(f"Ошибка при получении истории цены | announ_id: {announ_id} | error: {str(e)}")
        raise ValueError("Ошибка при получении истории цены")

    points = [
        ChartPoint(
            period=str(point["price_date"]),
            value=float(point["price"]),
        )
        for point in rows
    ]

    return points


async def get_current_price_db(announ_id: int):
    logger.info(f"Запрос текущей цены | announ_id: {announ_id}")

    query = text(
        """
        SELECT COALESCE(c.price, t.price) AS price
        FROM announs a
                 LEFT JOIN channels c
                      ON c.chn_announ_id = a.announ_id
                 LEFT JOIN traffic t
                      ON t.trf_announ_id = a.announ_id
        WHERE a.announ_id = :announ_id
        """
    )

    try:
        async with new_session() as session:
            result = await session.execute(query, {"announ_id": announ_id})
            price = result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Ошибка при получении текущей цены | announ_id: {announ_id} | error: {str(e)}")
        raise ValueError("Ошибка при получении текущей цены")

    return float(price) if price is not None else None


async def get_price_chart_db(announ_id: int):
    points = await get_price_chart_points_db(announ_id)

    if not points:
        raise ValueError("нет данных")

    def format_delta(delta):
        formatted = f"{delta:+.2f}".rstrip("0").rstrip(".")
        return "0" if formatted in ("+0", "-0") else formatted

    current_value = await get_current_price_db(announ_id)
    yesterday_price = points[0].value
    yesterday_delta = format_delta(yesterday_price - points[1].value) if len(points) > 1 else None
    week_delta = format_delta(yesterday_price - points[7].value) if len(points) > 7 else None
    month_delta = format_delta(yesterday_price - points[30].value) if len(points) > 30 else None

    return Chart(
        title="price",
        points=points,
        current_value=current_value,
        yesterday_delta=yesterday_delta,
        week_delta=week_delta,
        month_delta=month_delta,
    )
