from pydantic import BaseModel, Field

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import register
from ai_assistant.logger import get_logger
from ai_assistant.memory.repository import update_fact
from ai_assistant.tools.base import Tool

logger = get_logger(__name__)


class _Params(BaseModel):
    fact_id: int = Field(description="ID факта из блока «Что ты знаешь о пользователе»")
    content: str = Field(description="Новая формулировка факта одним предложением")


@register
class UpdateFact(Tool):
    name = "update_fact"
    description = "Обновить существующий факт о пользователе по его ID, когда узнал новое или факт устарел."
    Params = _Params

    async def execute(self, ctx: ToolContext, params: _Params) -> dict:
        ok = await update_fact(ctx.ai_db, ctx.user_id, params.fact_id, params.content)
        logger.info("факт обновлён | user_id=%s | fact_id=%s | ok=%s", ctx.user_id, params.fact_id, ok)
        return {"updated": ok}
