from pydantic import BaseModel, Field
from sqlalchemy import text

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.tools.base import Tool
from ai_assistant.tools.topics import get_topics

logger = get_logger(__name__)


class GeoPriceSchema(BaseModel):
    country: str
    count: int
    avg_price_usdt: float | None
    avg_price_rub: float | None


class ToolAnswerSchema(BaseModel):
    found: bool
    topic: str
    segment: str
    countries: list[GeoPriceSchema]


_SQL_RESOLVE_TOPIC = text("SELECT id, topic_name FROM topics WHERE topic_name ILIKE :topic")
_SQL_RATE = text("SELECT ruble_usdt_rate FROM rate")

_SQL_GEO_TEMPLATE = """
    WITH geo AS ({segment_geo})
    SELECT country, count(*) AS cnt, avg(price) AS avg_price
    FROM geo GROUP BY country ORDER BY avg(price) ASC
"""

# наборы пар «страна, цена»: страна у одиночных — прямой столбец, у сетей — через junction;
# MAX здесь нет вовсе — страны у него в БД не заведено
_GEO_CHANNELS = """
    SELECT co.country_name AS country, c.price FROM tg_channels c
      JOIN announs a ON a.announ_id = c.chn_announ_id JOIN countries co ON co.id = c.country
      WHERE a.status = 'active' AND c.topic = :topic_id
    UNION ALL SELECT co.country_name, n.price FROM tg_chns_nets n
      JOIN announs a ON a.announ_id = n.net_announ_id
      JOIN tg_chns_nets_topics t ON t.net_announ_id = n.net_announ_id
      JOIN tg_chns_nets_countries cc ON cc.net_announ_id = n.net_announ_id
      JOIN countries co ON co.id = cc.country_id
      WHERE a.status = 'active' AND t.topic_id = :topic_id
"""

_GEO_ADS = """
    SELECT co.country_name AS country, p.price FROM tg_ads a
      JOIN announs an ON an.announ_id = a.ad_id JOIN tg_ads_prices p ON p.ad_id = a.ad_id
      JOIN countries co ON co.id = a.country
      WHERE an.status = 'active' AND a.topic = :topic_id
    UNION ALL SELECT co.country_name, p.price FROM tg_net_ads a
      JOIN announs an ON an.announ_id = a.ad_id JOIN tg_net_ads_prices p ON p.ad_id = a.ad_id
      JOIN tg_net_ads_topics t ON t.ad_id = a.ad_id
      JOIN tg_net_ads_countries cc ON cc.ad_id = a.ad_id
      JOIN countries co ON co.id = cc.country_id
      WHERE an.status = 'active' AND t.topic_id = :topic_id
"""

_GEO_STORIES = """
    SELECT co.country_name AS country, p.price FROM stories a
      JOIN announs an ON an.announ_id = a.story_id JOIN stories_prices p ON p.story_id = a.story_id
      JOIN countries co ON co.id = a.country
      WHERE an.status = 'active' AND a.topic = :topic_id
    UNION ALL SELECT co.country_name, p.price FROM stories_nets a
      JOIN announs an ON an.announ_id = a.story_id
      JOIN stories_nets_prices p ON p.story_id = a.story_id
      JOIN stories_nets_topics t ON t.story_id = a.story_id
      JOIN stories_nets_countries cc ON cc.story_id = a.story_id
      JOIN countries co ON co.id = cc.country_id
      WHERE an.status = 'active' AND t.topic_id = :topic_id
"""

_GEO_TRAFFIC = """
    SELECT co.country_name AS country, t.price FROM traffic t
      JOIN announs a ON a.announ_id = t.traffic_id JOIN countries co ON co.id = t.country
      WHERE a.status = 'active' AND t.topic = :topic_id
"""

# сегмент выбирает готовый запрос, а не подставляется в строку
_SQL_BY_SEGMENT = {
    "каналы": text(_SQL_GEO_TEMPLATE.format(segment_geo=_GEO_CHANNELS)),
    "реклама": text(_SQL_GEO_TEMPLATE.format(segment_geo=_GEO_ADS)),
    "сторис": text(_SQL_GEO_TEMPLATE.format(segment_geo=_GEO_STORIES)),
    "трафик": text(_SQL_GEO_TEMPLATE.format(segment_geo=_GEO_TRAFFIC)),
}


class _Params(BaseModel):
    topic: str = Field(description="Название тематики")
    segment: str = Field(description="Сегмент рынка: каналы, реклама, сторис или трафик")


def _to_float(value) -> float | None:
    return float(value) if value is not None else None


def _to_rub(value_usdt: float | None, rate: float | None) -> float | None:
    if value_usdt is None or rate is None:
        return None
    return value_usdt * rate


@register
class PriceByGeo(Tool):
    name = "price_by_geo"
    description = (
        "Сравнение средней цены одной тематики между странами по одному сегменту рынка "
        "(каналы / реклама / сторис / трафик): по каждой стране, где есть предложения, — средняя "
        "цена и число объявлений, в USDT и рублях (курс из БД), по активным объявлениям, от "
        "дешёвых стран к дорогим. Страна в данных есть только у Telegram и трафика, MAX в это "
        "сравнение не входит — страны у него нет."
    )
    Params = _Params

    def tool_spec(self) -> dict:
        spec = super().tool_spec()
        properties = spec["function"]["parameters"]["properties"]
        properties["topic"]["enum"] = get_topics()
        properties["segment"]["enum"] = list(_SQL_BY_SEGMENT)
        return spec

    async def execute(self, ctx: ToolContext, params: _Params) -> dict:
        resolved = await ctx.db.execute(_SQL_RESOLVE_TOPIC, {"topic": params.topic})
        topic_row = resolved.mappings().one_or_none()
        if topic_row is None:
            logger.info("тема не найдена | topic=%s | user_id=%s", params.topic, ctx.user_id)
            return ToolAnswerSchema(
                found=False, topic=params.topic, segment=params.segment, countries=[],
            ).model_dump()

        topic_id = topic_row["id"]
        topic_name = topic_row["topic_name"]

        rate_result = await ctx.db.execute(_SQL_RATE)
        rate = _to_float(rate_result.scalar_one_or_none())

        result = await ctx.db.execute(_SQL_BY_SEGMENT[params.segment], {"topic_id": topic_id})
        countries = []
        for row in result.mappings().all():
            avg_usdt = _to_float(row["avg_price"])
            countries.append(GeoPriceSchema(
                country=row["country"],
                count=int(row["cnt"]),
                avg_price_usdt=avg_usdt,
                avg_price_rub=_to_rub(avg_usdt, rate),
            ))

        logger.info(
            "сравнение цен по гео посчитано | topic=%s | segment=%s | user_id=%s | countries=%s",
            topic_name, params.segment, ctx.user_id, len(countries),
        )
        return ToolAnswerSchema(
            found=len(countries) > 0, topic=topic_name, segment=params.segment, countries=countries,
        ).model_dump()
