from sqlalchemy import text

from .db_engine import new_session
from ..app_classes import AnnounCreateSchema
from ..logger import get_logger


logger = get_logger(__name__)


async def post_announ_imgs_db(session, announ_id: int, imgs: list[str]):
    if not imgs:
        return

    query = text(
        """
        INSERT INTO imgs (img_announ_id, img_filename)
        VALUES (:announ_id, :img_filename);
        """
    )

    for img_filename in imgs:
        await session.execute(query, {"announ_id": announ_id, "img_filename": img_filename})


async def post_account_announ_db(session, announ_id: int, data: dict):
    logger.info("Создание данных объявления Аккаунта | announ_id = %s", announ_id)

    query = text(
        """
        INSERT INTO accs_announs
            (acc_announ_id, country, log_type, idle_time, acc_type, premium, stars_count, gifts, tg_level)
        VALUES
            (:announ_id, :country, :log_type, :idle_time, :acc_type, :premium, :stars_count, :gifts, :tg_level);
        """
    )

    await session.execute(
        query,
        {
            "announ_id": announ_id,
            "country": data["country"],
            "log_type": data["log_type"],
            "idle_time": data["idle_time"],
            "acc_type": data["acc_type"],
            "premium": data["premium"],
            "stars_count": data["stars_count"],
            "gifts": data["gifts"],
            "tg_level": data["tg_level"],
        },
    )


async def post_traffic_announ_db(session, announ_id: int, data: dict):
    logger.info("Создание данных объявления Трафика | announ_id = %s", announ_id)

    query = text(
        """
        INSERT INTO traffic
            (trf_announ_id, topic, platform, traffic_type, audience_type, country)
        VALUES
            (:announ_id, :topic, :platform, :traffic_type, :audience_type, :country);
        """
    )

    await session.execute(
        query,
        {
            "announ_id": announ_id,
            "topic": data["topic"],
            "platform": data["platform"],
            "traffic_type": data["traffic_type"],
            "audience_type": data["audience_type"],
            "country": data["country"],
        },
    )


async def post_ad_announ_db(session, announ_id: int, data: dict):
    logger.info("Создание данных объявления Рекламы | announ_id = %s", announ_id)

    query = text(
        """
        INSERT INTO ads
            (ad_announ_id, topic, country, cover, cpm, er)
        VALUES
            (:announ_id, :topic, :country, :cover, :cpm, :er);
        """
    )

    await session.execute(
        query,
        {
            "announ_id": announ_id,
            "topic": data["topic"],
            "country": data["country"],
            "cover": data["cover"],
            "cpm": data["cpm"],
            "er": data["er"],
        },
    )


async def post_channel_announ_db(session, announ_id: int, data: dict):
    logger.info("Создание данных объявления Канала | announ_id = %s", announ_id)

    query = text(
        """
        INSERT INTO channels
            (chn_announ_id, topic, chn_type, country, subs_count, cover_count, profit, entry_requests)
        VALUES
            (:announ_id, :topic, :chn_type, :country, :subs_count, :cover_count, :profit, :entry_requests);
        """
    )

    await session.execute(
        query,
        {
            "announ_id": announ_id,
            "topic": data["topic"],
            "chn_type": data["chn_type"],
            "country": data["country"],
            "subs_count": data["subs_count"],
            "cover_count": data["cover_count"],
            "profit": data["profit"],
            "entry_requests": data["entry_requests"],
        },
    )


async def post_common_info_db(session, announ_type: str, announ_info: dict):
    query = text(
        """
        INSERT INTO announs (seller_id, type, title, price, short_text, long_text, status)
        VALUES (:seller_id, :type, :title, :price, :short_text, :long_text, :status) RETURNING announ_id;
        """
    )

    result = await session.execute(
        query,
        {
            "seller_id": announ_info["seller_id"],
            "type": announ_type,
            "title": announ_info["title"],
            "price": announ_info["price"],
            "short_text": announ_info["short_text"],
            "long_text": announ_info["long_text"],
            "status": announ_info["status"],
        },
    )

    announ_id = result.scalar_one_or_none()

    if announ_id is None:
        raise Exception("announ_create_error")

    logger.info("Базовые данные объявления успешно записаны | announ_id = %s", announ_id)
    return int(announ_id)


async def post_announ_db(data: AnnounCreateSchema):
    logger.info("Создание объявления")

    announ_type = data.type
    announ_info = data.announ_info

    if not announ_type:
        raise Exception("type_not_found")

    if not announ_info:
        raise Exception("announ_info_not_found")

    async with new_session() as session:
        announ_id = await post_common_info_db(session, announ_type, announ_info)

        if announ_type == "channel":
            await post_channel_announ_db(session, announ_id, announ_info)
        elif announ_type == "ad":
            await post_ad_announ_db(session, announ_id, announ_info)
        elif announ_type == "traffic":
            await post_traffic_announ_db(session, announ_id, announ_info)
        elif announ_type == "account":
            await post_account_announ_db(session, announ_id, announ_info)
        else:
            raise Exception("unknown_announ_type")

        imgs = announ_info.get("imgs")
        await post_announ_imgs_db(session, announ_id, imgs)

        await session.commit()

        return {"success": True, "announ_id": announ_id}