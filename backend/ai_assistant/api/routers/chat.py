import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from ai_assistant.agent.loop import stream_chat
from ai_assistant.api.schemas.chat import ChatRequest
from ai_assistant.core.errors import LLMError
from ai_assistant.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["Chat"])


@router.post("/chat", summary="Чат с ассистентом (SSE-стрим)")
async def chat(data: ChatRequest, request: Request) -> StreamingResponse:
    client = request.app.state.llm_client
    system_prompt = request.app.state.system_prompt
    logger.info("В чат отправлено сообщение | %s", repr(data))

    async def event_stream():
        try:
            async for delta in stream_chat(client, system_prompt, data.message):
                yield f"data: {json.dumps({'delta': delta}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"
        except LLMError as e:
            logger.error("chat llm_error | user_id=%s | error=%s", data.user_id, str(e))
            yield f"data: {json.dumps({'error': 'llm_error'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
