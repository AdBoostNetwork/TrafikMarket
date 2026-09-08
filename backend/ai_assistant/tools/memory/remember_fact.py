from pydantic import BaseModel, Field

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.memory.repository import add_fact
from ai_assistant.tools.base import Tool

logger = get_logger(__name__)


class _Params(BaseModel):
    content: str = Field(description="Факт о пользователе одним предложением")


@register
class RememberFact(Tool):
    name = "remember_fact"
    description = (
        "Сохранить новый устойчивый факт о пользователе (чем торгует, бюджет, тематики, "
        "предпочтения). Только устойчивое и полезное для будущих разговоров, не мелочи и не разовое."
    )
    Params = _Params

    async def execute(self, ctx: ToolContext, params: _Params) -> dict:
        fact_id = await add_fact(ctx.ai_db, ctx.user_id, params.content)
        logger.info("факт сохранён | user_id=%s | fact_id=%s", ctx.user_id, fact_id)
        return {"saved": True, "fact_id": fact_id}
