from pydantic import BaseModel, Field

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.memory.repository import delete_fact
from ai_assistant.tools.base import Tool

logger = get_logger(__name__)


class _Params(BaseModel):
    fact_id: int = Field(description="ID факта из блока «Что ты знаешь о пользователе»")


@register
class ForgetFact(Tool):
    name = "forget_fact"
    description = "Удалить факт о пользователе по его ID, когда факт больше не верен."
    Params = _Params

    async def execute(self, ctx: ToolContext, params: _Params) -> dict:
        ok = await delete_fact(ctx.ai_db, ctx.user_id, params.fact_id)
        logger.info("факт забыт | user_id=%s | fact_id=%s | ok=%s", ctx.user_id, params.fact_id, ok)
        return {"forgotten": ok}
