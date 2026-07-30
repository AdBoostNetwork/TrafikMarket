import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.loop import stream_chat
from ai_assistant.agent.registry import registry
from ai_assistant.api.schemas.chat import ChatRequest
from ai_assistant.core.errors import LLMError
from ai_assistant.db.dependencies import get_ai_session, get_main_session
from ai_assistant.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["Chat"])


@router.post("/chat", summary="Запрос в чат ассистента")
async def chat(
    data: ChatRequest,
    request: Request,
    session: AsyncSession = Depends(get_main_session),
    ai_session: AsyncSession = Depends(get_ai_session),
) -> StreamingResponse:
    client = request.app.state.llm_client
    system_prompt = request.app.state.system_prompt
    ctx = ToolContext(user_id=data.user_id, db=session, ai_db=ai_session)
    logger.info("В чат отправлено сообщение | %s", repr(data))

    async def event_stream():
        try:
            async for delta in stream_chat(client, system_prompt, data.message, ctx, registry):
                yield f"data: {json.dumps({'delta': delta}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"
        except LLMError as e:
            logger.error("chat llm_error | user_id=%s | error=%s", data.user_id, str(e))
            yield f"data: {json.dumps({'error': 'llm_error'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
