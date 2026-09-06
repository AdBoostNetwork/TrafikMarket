from pydantic import BaseModel, Field
from sqlalchemy import text

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.tools.base import Tool
from ai_assistant.tools.topics import get_topics

logger = get_logger(__name__)


class FormatCpmSchema(BaseModel):
    format: str
    placements: int
    avg_cpm_usdt: float | None
    avg_cpm_rub: float | None


class ToolAnswerSchema(BaseModel):
    found: bool
    topic: str
    formats: list[FormatCpmSchema]


_SQL_RESOLVE_TOPIC = text("SELECT id, topic_name FROM topics WHERE topic_name ILIKE :topic")
_SQL_RATE = text("SELECT ruble_usdt_rate FROM rate")

_SQL_CPM_BY_FORMAT = text("""
    WITH cpm_rows AS (
      SELECT p.format, p.price / NULLIF(a.cover_count, 0) * 1000 AS cpm
      FROM stories a
      JOIN announs an ON an.announ_id = a.story_id
      JOIN stories_prices p ON p.story_id = a.story_id
      WHERE an.status = 'active' AND a.topic = :topic_id
      UNION ALL
      SELECT p.format, p.price / NULLIF(a.cover_count, 0) * 1000
      FROM stories_nets a
      JOIN announs an ON an.announ_id = a.story_id
      JOIN stories_nets_prices p ON p.story_id = a.story_id
      JOIN stories_nets_topics t ON t.story_id = a.story_id
      WHERE an.status = 'active' AND t.topic_id = :topic_id
    )
    SELECT format, count(*) AS placements, avg(cpm) AS avg_cpm
    FROM cpm_rows GROUP BY format ORDER BY format
""")


class _Params(BaseModel):
    topic: str = Field(description="Название тематики")


def _to_float(value) -> float | None:
    return float(value) if value is not None else None


def _to_rub(value_usdt: float | None, rate: float | None) -> float | None:
    if value_usdt is None or rate is None:
        return None
    return value_usdt * rate


def _format_cpm(row, rate: float | None) -> FormatCpmSchema:
    avg_cpm_usdt = _to_float(row["avg_cpm"])
    return FormatCpmSchema(
        format=row["format"],
        placements=int(row["placements"]),
        avg_cpm_usdt=avg_cpm_usdt,
        avg_cpm_rub=_to_rub(avg_cpm_usdt, rate),
    )


@register
class AvgStoryCpm(Tool):
    name = "avg_story_cpm"
    description = (
        "Средний CPM (цена за 1000 охвата) сторис в заданной тематике — по всем форматам темы "
        "(«сторис 24ч», «сторис 6ч» и т.п.), в USDT и рублях (курс из БД). Считается по активным "
        "объявлениям сторис: одиночные и сети, Telegram. Реклама-посты, каналы и трафик сюда не входят."
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
            return ToolAnswerSchema(found=False, topic=params.topic, formats=[]).model_dump()

        topic_id = topic_row["id"]
        topic_name = topic_row["topic_name"]

        rate_result = await ctx.db.execute(_SQL_RATE)
        rate = _to_float(rate_result.scalar_one_or_none())

        cpm_result = await ctx.db.execute(_SQL_CPM_BY_FORMAT, {"topic_id": topic_id})
        formats = [_format_cpm(row, rate) for row in cpm_result.mappings()]

        logger.info(
            "средний CPM сторис посчитан | topic=%s | user_id=%s | rate=%s | formats=%s",
            topic_name, ctx.user_id, rate, len(formats),
        )
        return ToolAnswerSchema(found=True, topic=topic_name, formats=formats).model_dump()
