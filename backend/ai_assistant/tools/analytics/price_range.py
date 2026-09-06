from pydantic import BaseModel, Field
from sqlalchemy import text

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.tools.base import Tool
from ai_assistant.tools.topics import get_topics

logger = get_logger(__name__)


class Money(BaseModel):
    usdt: float | None
    rub: float | None


class ToolAnswerSchema(BaseModel):
    found: bool
    topic: str
    segment: str
    count: int
    min: Money
    p25: Money
    median: Money
    p75: Money
    max: Money


_SQL_RESOLVE_TOPIC = text("SELECT id, topic_name FROM topics WHERE topic_name ILIKE :topic")
_SQL_RATE = text("SELECT ruble_usdt_rate FROM rate")

_SQL_STATS_TEMPLATE = """
    WITH prices AS ({segment_prices})
    SELECT count(*) AS cnt,
           min(price) AS mn,
           percentile_cont(0.25) WITHIN GROUP (ORDER BY price) AS p25,
           percentile_cont(0.5)  WITHIN GROUP (ORDER BY price) AS median,
           percentile_cont(0.75) WITHIN GROUP (ORDER BY price) AS p75,
           max(price) AS mx
    FROM prices
"""

# наборы цен: у сетей тема через junction, у рекламы и сторис цена — у каждого формата
_PRICES_CHANNELS = """
    SELECT c.price FROM tg_channels c JOIN announs a ON a.announ_id = c.chn_announ_id
      WHERE a.status = 'active' AND c.topic = :topic_id
    UNION ALL SELECT c.price FROM max_channels c JOIN announs a ON a.announ_id = c.chn_announ_id
      WHERE a.status = 'active' AND c.topic = :topic_id
    UNION ALL SELECT n.price FROM tg_chns_nets n JOIN announs a ON a.announ_id = n.net_announ_id
      JOIN tg_chns_nets_topics t ON t.net_announ_id = n.net_announ_id
      WHERE a.status = 'active' AND t.topic_id = :topic_id
    UNION ALL SELECT n.price FROM max_chns_nets n JOIN announs a ON a.announ_id = n.net_announ_id
      JOIN max_chns_nets_topics t ON t.net_announ_id = n.net_announ_id
      WHERE a.status = 'active' AND t.topic_id = :topic_id
"""

_PRICES_ADS = """
    SELECT p.price FROM tg_ads a JOIN announs an ON an.announ_id = a.ad_id
      JOIN tg_ads_prices p ON p.ad_id = a.ad_id WHERE an.status = 'active' AND a.topic = :topic_id
    UNION ALL SELECT p.price FROM max_ads a JOIN announs an ON an.announ_id = a.ad_id
      JOIN max_ads_prices p ON p.ad_id = a.ad_id WHERE an.status = 'active' AND a.topic = :topic_id
    UNION ALL SELECT p.price FROM tg_net_ads a JOIN announs an ON an.announ_id = a.ad_id
      JOIN tg_net_ads_prices p ON p.ad_id = a.ad_id JOIN tg_net_ads_topics t ON t.ad_id = a.ad_id
      WHERE an.status = 'active' AND t.topic_id = :topic_id
    UNION ALL SELECT p.price FROM max_net_ads a JOIN announs an ON an.announ_id = a.ad_id
      JOIN max_net_ads_prices p ON p.ad_id = a.ad_id JOIN max_net_ads_topics t ON t.ad_id = a.ad_id
      WHERE an.status = 'active' AND t.topic_id = :topic_id
"""

_PRICES_STORIES = """
    SELECT p.price FROM stories a JOIN announs an ON an.announ_id = a.story_id
      JOIN stories_prices p ON p.story_id = a.story_id WHERE an.status = 'active' AND a.topic = :topic_id
    UNION ALL SELECT p.price FROM stories_nets a JOIN announs an ON an.announ_id = a.story_id
      JOIN stories_nets_prices p ON p.story_id = a.story_id
      JOIN stories_nets_topics t ON t.story_id = a.story_id
      WHERE an.status = 'active' AND t.topic_id = :topic_id
"""

_PRICES_TRAFFIC = """
    SELECT t.price FROM traffic t JOIN announs a ON a.announ_id = t.traffic_id
      WHERE a.status = 'active' AND t.topic = :topic_id
"""

# сегмент выбирает готовый запрос, а не подставляется в строку
_SQL_BY_SEGMENT = {
    "каналы": text(_SQL_STATS_TEMPLATE.format(segment_prices=_PRICES_CHANNELS)),
    "реклама": text(_SQL_STATS_TEMPLATE.format(segment_prices=_PRICES_ADS)),
    "сторис": text(_SQL_STATS_TEMPLATE.format(segment_prices=_PRICES_STORIES)),
    "трафик": text(_SQL_STATS_TEMPLATE.format(segment_prices=_PRICES_TRAFFIC)),
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


def _money(value, rate: float | None) -> Money:
    return Money(usdt=_to_float(value), rub=_to_rub(_to_float(value), rate))


@register
class PriceRange(Tool):
    name = "price_range"
    description = (
        "Разброс цен в тематике по одному сегменту рынка (каналы / реклама / сторис / трафик): "
        "минимум, максимум, медиана и концентрация (25-й–75-й перцентиль, средняя половина цен) — "
        "в USDT и рублях (курс из БД), по активным объявлениям. Цены разных сегментов несопоставимы "
        "(канал стоит тысячи, формат рекламы — десятки, трафик — за подписчика), сегмент обязателен."
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
            empty = Money(usdt=None, rub=None)
            return ToolAnswerSchema(
                found=False, topic=params.topic, segment=params.segment, count=0,
                min=empty, p25=empty, median=empty, p75=empty, max=empty,
            ).model_dump()

        topic_id = topic_row["id"]
        topic_name = topic_row["topic_name"]

        rate_result = await ctx.db.execute(_SQL_RATE)
        rate = _to_float(rate_result.scalar_one_or_none())

        result = await ctx.db.execute(_SQL_BY_SEGMENT[params.segment], {"topic_id": topic_id})
        row = result.mappings().one()
        count = int(row["cnt"])

        logger.info(
            "диапазон цен посчитан | topic=%s | segment=%s | user_id=%s | count=%s",
            topic_name, params.segment, ctx.user_id, count,
        )
        return ToolAnswerSchema(
            found=count > 0, topic=topic_name, segment=params.segment, count=count,
            min=_money(row["mn"], rate), p25=_money(row["p25"], rate),
            median=_money(row["median"], rate), p75=_money(row["p75"], rate), max=_money(row["mx"], rate),
        ).model_dump()
