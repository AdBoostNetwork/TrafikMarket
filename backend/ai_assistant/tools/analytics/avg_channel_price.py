from pydantic import BaseModel, Field
from sqlalchemy import text

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.tools.base import Tool
from ai_assistant.tools.topics import get_topics

logger = get_logger(__name__)


class SegmentDataSchema(BaseModel):
    announs_count: int
    avg_price_usdt: float | None
    avg_price_rub: float | None
    price_per_sub_usdt: float | None
    price_per_sub_rub: float | None


class ToolAnswerSchema(BaseModel):
    found: bool
    topic: str
    telegram_single: SegmentDataSchema
    telegram_net: SegmentDataSchema
    max_single: SegmentDataSchema
    max_net: SegmentDataSchema


_SQL_RESOLVE_TOPIC = text("SELECT id, topic_name FROM topics WHERE topic_name ILIKE :topic")
_SQL_RATE = text("SELECT ruble_usdt_rate FROM rate")

_SQL_SINGLE_TEMPLATE = """
    SELECT count(*) AS count,
           avg(price) AS avg_price,
           avg(price / NULLIF(subs_count, 0)) AS price_per_sub
    FROM {table} c
    JOIN announs a ON a.announ_id = c.chn_announ_id
    WHERE a.status = 'active' AND c.topic = :topic_id
"""

_SQL_NET_TEMPLATE = """
    SELECT count(DISTINCT n.net_announ_id) AS count,
           avg(n.price) AS avg_price,
           avg(n.price / NULLIF(n.subs_count, 0)) AS price_per_sub
    FROM {table} n
    JOIN announs a ON a.announ_id = n.net_announ_id
    JOIN {topics_table} t ON t.net_announ_id = n.net_announ_id
    WHERE a.status = 'active' AND t.topic_id = :topic_id
"""

_SQL_SINGLE_TG = text(_SQL_SINGLE_TEMPLATE.format(table="tg_channels"))
_SQL_SINGLE_MAX = text(_SQL_SINGLE_TEMPLATE.format(table="max_channels"))
_SQL_NET_TG = text(_SQL_NET_TEMPLATE.format(table="tg_chns_nets", topics_table="tg_chns_nets_topics"))
_SQL_NET_MAX = text(_SQL_NET_TEMPLATE.format(table="max_chns_nets", topics_table="max_chns_nets_topics"))


class _Params(BaseModel):
    topic: str = Field(description="Название тематики канала")


def _to_float(value) -> float | None:
    return float(value) if value is not None else None


def _to_rub(value_usdt: float | None, rate: float | None) -> float | None:
    if value_usdt is None or rate is None:
        return None
    return value_usdt * rate


def _segment_data(row, rate: float | None) -> SegmentDataSchema:
    avg_price_usdt = _to_float(row["avg_price"])
    price_per_sub_usdt = _to_float(row["price_per_sub"])
    return SegmentDataSchema(
        announs_count=int(row["count"]),
        avg_price_usdt=avg_price_usdt,
        avg_price_rub=_to_rub(avg_price_usdt, rate),
        price_per_sub_usdt=price_per_sub_usdt,
        price_per_sub_rub=_to_rub(price_per_sub_usdt, rate),
    )


def _empty_segment() -> SegmentDataSchema:
    return SegmentDataSchema(
        announs_count=0, avg_price_usdt=None, avg_price_rub=None,
        price_per_sub_usdt=None, price_per_sub_rub=None,
    )


@register
class AvgChannelPrice(Tool):
    name = "avg_channel_price"
    description = (
        "Средняя цена одиночного канала и сети каналов в заданной тематике, отдельно для Telegram и MAX: "
        "число объявлений, средняя цена и цена за подписчика — в USDT и рублях (курс из БД), по активным "
        "объявлениям. У сети цена — за весь лот целиком (своей цены у канала внутри сети в БД нет), "
        "поэтому сегменты одиночных и сетей сравнивай по цене за подписчика, не по абсолютной цене."
    )
    Params = _Params

    def tool_spec(self) -> dict:
        spec = super().tool_spec()
        spec["function"]["parameters"]["properties"]["topic"]["enum"] = get_topics()
        return spec

    async def execute(self, ctx: ToolContext, params: _Params) -> dict:
        resolved = await ctx.db.execute(_SQL_RESOLVE_TOPIC, {"topic": params.topic})
        topic_row = resolved.mappings().one_or_none()
        if topic_row is None:
            logger.info("тема не найдена | topic=%s | user_id=%s", params.topic, ctx.user_id)
            empty = _empty_segment()
            return ToolAnswerSchema(
                found=False, topic=params.topic,
                telegram_single=empty, telegram_net=empty, max_single=empty, max_net=empty,
            ).model_dump()

        topic_id = topic_row["id"]
        topic_name = topic_row["topic_name"]

        rate_result = await ctx.db.execute(_SQL_RATE)
        rate = _to_float(rate_result.scalar_one_or_none())

        tg_single = await ctx.db.execute(_SQL_SINGLE_TG, {"topic_id": topic_id})
        telegram_single = _segment_data(tg_single.mappings().one(), rate)

        tg_net = await ctx.db.execute(_SQL_NET_TG, {"topic_id": topic_id})
        telegram_net = _segment_data(tg_net.mappings().one(), rate)

        max_single_result = await ctx.db.execute(_SQL_SINGLE_MAX, {"topic_id": topic_id})
        max_single = _segment_data(max_single_result.mappings().one(), rate)

        max_net_result = await ctx.db.execute(_SQL_NET_MAX, {"topic_id": topic_id})
        max_net = _segment_data(max_net_result.mappings().one(), rate)

        logger.info(
            "средняя цена канала посчитана | topic=%s | user_id=%s | rate=%s | "
            "tg_single=%s | tg_net=%s | max_single=%s | max_net=%s",
            topic_name, ctx.user_id, rate,
            telegram_single.announs_count, telegram_net.announs_count,
            max_single.announs_count, max_net.announs_count,
        )
        return ToolAnswerSchema(
            found=True, topic=topic_name,
            telegram_single=telegram_single, telegram_net=telegram_net,
            max_single=max_single, max_net=max_net,
        ).model_dump()
