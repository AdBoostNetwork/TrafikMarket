from pydantic import BaseModel, Field
from sqlalchemy import text

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.tools.base import Tool
from ai_assistant.tools.topics import get_topics

logger = get_logger(__name__)


class FormatComparisonSchema(BaseModel):
    format: str
    placements: int
    avg_price_usdt: float | None
    avg_price_rub: float | None
    requests_count: int


class ToolAnswerSchema(BaseModel):
    found: bool
    topic: str
    segment: str
    formats: list[FormatComparisonSchema]


_SQL_RESOLVE_TOPIC = text("SELECT id, topic_name FROM topics WHERE topic_name ILIKE :topic")
_SQL_RATE = text("SELECT ruble_usdt_rate FROM rate")

# цена и число размещений — из прайсов формата, популярность — из откликов на этот формат;
# тема отклика берётся через объявление, поэтому нужна карта announ_id → topic_id
_SQL_TEMPLATE = """
    WITH prices AS ({segment_prices}),
    announ_topic AS ({segment_topics}),
    reqs AS (SELECT r.format FROM {requests_table} r
             JOIN announ_topic at ON at.announ_id = r.announ_id WHERE at.topic_id = :topic_id),
    price_stats AS (
      SELECT format, count(*) AS placements, avg(price) AS avg_price FROM prices GROUP BY format
    ),
    req_stats AS (SELECT format, count(*) AS req_count FROM reqs GROUP BY format)
    SELECT ps.format, ps.placements, ps.avg_price, COALESCE(rs.req_count, 0) AS req_count
    FROM price_stats ps LEFT JOIN req_stats rs ON rs.format = ps.format
    ORDER BY ps.placements DESC, ps.format
"""

_ADS_PRICES = """
      SELECT p.format, p.price FROM tg_ads a JOIN announs an ON an.announ_id = a.ad_id
        JOIN tg_ads_prices p ON p.ad_id = a.ad_id WHERE an.status = 'active' AND a.topic = :topic_id
      UNION ALL SELECT p.format, p.price FROM max_ads a JOIN announs an ON an.announ_id = a.ad_id
        JOIN max_ads_prices p ON p.ad_id = a.ad_id WHERE an.status = 'active' AND a.topic = :topic_id
      UNION ALL SELECT p.format, p.price FROM tg_net_ads a JOIN announs an ON an.announ_id = a.ad_id
        JOIN tg_net_ads_prices p ON p.ad_id = a.ad_id JOIN tg_net_ads_topics t ON t.ad_id = a.ad_id
        WHERE an.status = 'active' AND t.topic_id = :topic_id
      UNION ALL SELECT p.format, p.price FROM max_net_ads a JOIN announs an ON an.announ_id = a.ad_id
        JOIN max_net_ads_prices p ON p.ad_id = a.ad_id JOIN max_net_ads_topics t ON t.ad_id = a.ad_id
        WHERE an.status = 'active' AND t.topic_id = :topic_id
"""

_ADS_TOPICS = """
      SELECT ad_id AS announ_id, topic AS topic_id FROM tg_ads
      UNION ALL SELECT ad_id, topic FROM max_ads
      UNION ALL SELECT ad_id, topic_id FROM tg_net_ads_topics
      UNION ALL SELECT ad_id, topic_id FROM max_net_ads_topics
"""

_STORIES_PRICES = """
      SELECT p.format, p.price FROM stories a JOIN announs an ON an.announ_id = a.story_id
        JOIN stories_prices p ON p.story_id = a.story_id
        WHERE an.status = 'active' AND a.topic = :topic_id
      UNION ALL SELECT p.format, p.price FROM stories_nets a
        JOIN announs an ON an.announ_id = a.story_id
        JOIN stories_nets_prices p ON p.story_id = a.story_id
        JOIN stories_nets_topics t ON t.story_id = a.story_id
        WHERE an.status = 'active' AND t.topic_id = :topic_id
"""

_STORIES_TOPICS = """
      SELECT story_id AS announ_id, topic AS topic_id FROM stories
      UNION ALL SELECT story_id, topic_id FROM stories_nets_topics
"""

# сегмент выбирает готовый запрос, а не подставляется в строку
_SQL_BY_SEGMENT = {
    "реклама": text(_SQL_TEMPLATE.format(
        segment_prices=_ADS_PRICES, segment_topics=_ADS_TOPICS, requests_table="ad_requests",
    )),
    "сторис": text(_SQL_TEMPLATE.format(
        segment_prices=_STORIES_PRICES, segment_topics=_STORIES_TOPICS,
        requests_table="stories_requests",
    )),
}


class _Params(BaseModel):
    topic: str = Field(description="Название тематики")
    segment: str = Field(description="Сегмент рынка: реклама или сторис")


def _to_float(value) -> float | None:
    return float(value) if value is not None else None


def _to_rub(value_usdt: float | None, rate: float | None) -> float | None:
    if value_usdt is None or rate is None:
        return None
    return value_usdt * rate


@register
class FormatComparison(Tool):
    name = "format_comparison"
    description = (
        "Сравнение форматов размещения в тематике по сегменту рынка (реклама или сторис): по "
        "каждому формату средняя цена, число размещений с этим форматом и сколько раз формат "
        "запрашивали в откликах (популярность), в USDT и рублях (курс из БД), по активным "
        "объявлениям. Форматы есть только у рекламы и сторис, у каналов и трафика их нет. "
        "Популярность считается по откликам, поэтому пока откликов нет, она равна нулю у всех "
        "форматов — сравнивай в этом случае по цене и числу размещений."
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
                found=False, topic=params.topic, segment=params.segment, formats=[],
            ).model_dump()

        topic_id = topic_row["id"]
        topic_name = topic_row["topic_name"]

        rate_result = await ctx.db.execute(_SQL_RATE)
        rate = _to_float(rate_result.scalar_one_or_none())

        result = await ctx.db.execute(_SQL_BY_SEGMENT[params.segment], {"topic_id": topic_id})
        formats = []
        for row in result.mappings().all():
            avg_usdt = _to_float(row["avg_price"])
            formats.append(FormatComparisonSchema(
                format=row["format"],
                placements=int(row["placements"]),
                avg_price_usdt=avg_usdt,
                avg_price_rub=_to_rub(avg_usdt, rate),
                requests_count=int(row["req_count"]),
            ))

        logger.info(
            "сравнение форматов посчитано | topic=%s | segment=%s | user_id=%s | formats=%s",
            topic_name, params.segment, ctx.user_id, len(formats),
        )
        return ToolAnswerSchema(
            found=len(formats) > 0, topic=topic_name, segment=params.segment, formats=formats,
        ).model_dump()
