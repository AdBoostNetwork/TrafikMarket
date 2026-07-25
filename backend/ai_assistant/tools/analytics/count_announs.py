from pydantic import BaseModel, Field
from sqlalchemy import text

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.tools.base import Tool
from ai_assistant.tools.topics import get_topics

logger = get_logger(__name__)


class GroupCount(BaseModel):
    total: int
    telegram_single: int
    telegram_net: int
    max_single: int
    max_net: int


class CountAnswerSchema(BaseModel):
    topic: str | None
    found: bool
    total: int
    channels: GroupCount
    ads: GroupCount
    stories: GroupCount
    traffic: int


_SQL_RESOLVE_TOPIC = text("SELECT id, topic_name FROM topics WHERE topic_name ILIKE :topic")

_SQL_COUNT_ALL = text(
    "SELECT ty.type_name, count(*) AS cnt FROM announs a JOIN announ_types ty ON ty.id = a.type "
    "WHERE a.status = 'active' GROUP BY ty.type_name"
)

_SQL_COUNT_TOPIC = text("""
    WITH announ_topic AS (
      SELECT chn_announ_id AS announ_id, topic     AS topic_id FROM tg_channels
      UNION ALL SELECT chn_announ_id, topic     FROM max_channels
      UNION ALL SELECT ad_id,        topic     FROM tg_ads
      UNION ALL SELECT ad_id,        topic     FROM max_ads
      UNION ALL SELECT story_id,     topic     FROM stories
      UNION ALL SELECT traffic_id,   topic     FROM traffic
      UNION ALL SELECT net_announ_id, topic_id FROM tg_chns_nets_topics
      UNION ALL SELECT net_announ_id, topic_id FROM max_chns_nets_topics
      UNION ALL SELECT ad_id,        topic_id FROM tg_net_ads_topics
      UNION ALL SELECT ad_id,        topic_id FROM max_net_ads_topics
      UNION ALL SELECT story_id,     topic_id FROM stories_nets_topics
    )
    SELECT ty.type_name, count(DISTINCT at.announ_id) AS cnt
    FROM announ_topic at
    JOIN announs a       ON a.announ_id = at.announ_id
    JOIN announ_types ty ON ty.id = a.type
    WHERE a.status = 'active' AND at.topic_id = :topic_id
    GROUP BY ty.type_name
""")


class _Params(BaseModel):
    topic: str | None = Field(default=None, description="Тематика; не указывай для счёта по всей платформе")


def _group(counts: dict, ts_key: str, tn_key: str, ms_key: str | None, mn_key: str | None) -> GroupCount:
    ts, tn = counts.get(ts_key, 0), counts.get(tn_key, 0)
    ms = counts.get(ms_key, 0) if ms_key else 0
    mn = counts.get(mn_key, 0) if mn_key else 0
    return GroupCount(total=ts + tn + ms + mn, telegram_single=ts, telegram_net=tn, max_single=ms, max_net=mn)


@register
class CountAnnouns(Tool):
    name = "count_announs"
    description = (
        "Считает количество активных объявлений платформы по группам (каналы, реклама, сторис, трафик) "
        "с разбивкой Telegram/MAX и одиночные/сети. Без темы — по всей платформе, с темой — только внутри неё. "
        "У сторис MAX-типов в БД нет, эти слоты всегда 0."
    )
    Params = _Params

    def tool_spec(self) -> dict:
        spec = super().tool_spec()
        spec["function"]["parameters"]["properties"]["topic"] = {
            "type": "string",
            "enum": get_topics(),
            "description": "Тематика; не указывай для счёта по всей платформе",
        }
        return spec

    async def execute(self, ctx: ToolContext, params: _Params) -> dict:
        found = True
        if params.topic is None:
            result = await ctx.db.execute(_SQL_COUNT_ALL)
            counts = {row["type_name"]: int(row["cnt"]) for row in result.mappings().all()}
            topic_name = None
        else:
            resolved = await ctx.db.execute(_SQL_RESOLVE_TOPIC, {"topic": params.topic})
            topic_row = resolved.mappings().one_or_none()
            if topic_row is None:
                logger.info("тема не найдена | topic=%s | user_id=%s", params.topic, ctx.user_id)
                found, counts, topic_name = False, {}, params.topic
            else:
                topic_name = topic_row["topic_name"]
                result = await ctx.db.execute(_SQL_COUNT_TOPIC, {"topic_id": topic_row["id"]})
                counts = {row["type_name"]: int(row["cnt"]) for row in result.mappings().all()}
        channels = _group(counts, "tg_channel", "tg_chns_net", "max_channel", "max_chns_net")
        ads = _group(counts, "tg_ad", "tg_net_ad", "max_ad", "max_net_ad")
        stories = _group(counts, "story", "stories_net", None, None)
        traffic = counts.get("traffic", 0)
        total = channels.total + ads.total + stories.total + traffic
        if found:
            logger.info(
                "счётчик объявлений посчитан | topic=%s | user_id=%s | total=%s",
                topic_name if topic_name else "вся платформа", ctx.user_id, total,
            )
        return CountAnswerSchema(
            topic=topic_name, found=found, total=total,
            channels=channels, ads=ads, stories=stories, traffic=traffic,
        ).model_dump()
