from pydantic import BaseModel, Field
from sqlalchemy import text

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.tools.base import Tool
from ai_assistant.tools.dictionaries import get_dictionary
from ai_assistant.tools.topics import get_topics

logger = get_logger(__name__)


class ToolAnswerSchema(BaseModel):
    found: bool
    topic: str | None
    platform: str | None
    traffic_type: str | None
    audience: str | None
    count: int
    avg_price_per_sub_usdt: float | None
    avg_price_per_sub_rub: float | None


_SQL_RATE = text("SELECT ruble_usdt_rate FROM rate")

_SQL_BASE = """
    SELECT count(*) AS cnt, avg(t.price) AS avg_price
    FROM traffic t
    JOIN announs a ON a.announ_id = t.traffic_id
    JOIN topics tp ON tp.id = t.topic
    JOIN platforms pl ON pl.id = t.platform
    JOIN traffic_types tt ON tt.id = t.type
    JOIN audience_types au ON au.id = t.auditory
    WHERE a.status = 'active'
"""

# условия фильтров: имя параметра → готовое условие с плейсхолдером
_CONDITIONS = {
    "topic": "AND tp.topic_name = :topic",
    "platform": "AND pl.platform_name = :platform",
    "traffic_type": "AND tt.traffic_type_name = :traffic_type",
    "audience": "AND au.type_name = :audience",
}


class _Params(BaseModel):
    topic: str | None = Field(default=None, description="Тематика")
    platform: str | None = Field(default=None, description="Платформа трафика")
    traffic_type: str | None = Field(default=None, description="Тип трафика")
    audience: str | None = Field(default=None, description="Тип аудитории")


def _to_float(value) -> float | None:
    return float(value) if value is not None else None


def _to_rub(value_usdt: float | None, rate: float | None) -> float | None:
    if value_usdt is None or rate is None:
        return None
    return value_usdt * rate


def _build_query(params: _Params) -> tuple[str, dict]:
    filters = {key: value for key, value in params.model_dump().items() if value is not None}
    sql = _SQL_BASE + "".join(f"\n    {_CONDITIONS[key]}" for key in filters)
    return sql, filters


@register
class AvgTrafficPrice(Tool):
    name = "avg_traffic_price"
    description = (
        "Средняя цена за подписчика по объявлениям трафика в заданных фильтрах — тематика, "
        "платформа, тип трафика, тип аудитории (любой фильтр необязателен, без фильтров — весь "
        "активный трафик платформы). В USDT и рублях (курс из БД), по активным объявлениям."
    )
    Params = _Params

    def tool_spec(self) -> dict:
        spec = super().tool_spec()
        properties = spec["function"]["parameters"]["properties"]
        properties["topic"]["enum"] = get_topics()
        properties["platform"]["enum"] = get_dictionary("platform")
        properties["traffic_type"]["enum"] = get_dictionary("traffic_type")
        properties["audience"]["enum"] = get_dictionary("audience")
        return spec

    async def execute(self, ctx: ToolContext, params: _Params) -> dict:
        sql, filters = _build_query(params)
        result = await ctx.db.execute(text(sql), filters)
        row = result.mappings().one()

        rate_result = await ctx.db.execute(_SQL_RATE)
        rate = _to_float(rate_result.scalar_one_or_none())

        count = int(row["cnt"])
        avg_usdt = _to_float(row["avg_price"])

        logger.info(
            "средняя цена подписчика в трафике посчитана | user_id=%s | count=%s | filters=%s",
            ctx.user_id, count, filters if filters else "без фильтров",
        )
        return ToolAnswerSchema(
            found=count > 0,
            topic=params.topic,
            platform=params.platform,
            traffic_type=params.traffic_type,
            audience=params.audience,
            count=count,
            avg_price_per_sub_usdt=avg_usdt,
            avg_price_per_sub_rub=_to_rub(avg_usdt, rate),
        ).model_dump()
