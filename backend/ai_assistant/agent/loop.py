import json
import time
from collections.abc import AsyncIterator

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import Registry
from ai_assistant.llm.client import LLMClient, LLMMessage
from ai_assistant.logger import get_logger

logger = get_logger(__name__)

MAX_ROUNDS = 6

_EMPTY_ANSWER = "Не удалось сформулировать ответ, попробуйте переспросить."
_NO_FINAL_ANSWER = "Не смог собрать ответ, переформулируйте вопрос."


async def stream_chat(
    client: LLMClient,
    system_prompt: str,
    message: str,
    ctx: ToolContext,
    registry: Registry,
) -> AsyncIterator[str]:
    """Цикл tool-calling: модель просит инструменты, мы их исполняем, финальный текст отдаём целиком."""
    messages = [
        LLMMessage(role="system", content=system_prompt),
        LLMMessage(role="user", content=message),
    ]

    for round_number in range(1, MAX_ROUNDS + 1):
        resp = await client.complete(messages, tools=registry.specs())

        if not resp.tool_calls:
            final = resp.text or _EMPTY_ANSWER
            logger.info("ответ пользователю | user_id=%s | chars=%s", ctx.user_id, len(final))
            yield final
            return

        messages.append(LLMMessage(role="assistant", content=resp.text, tool_calls=resp.tool_calls))

        for call in resp.tool_calls:
            logger.info(
                "вызов инструмента | round=%s | name=%s | user_id=%s | args=%s",
                round_number, call.name, ctx.user_id, call.arguments,
            )
            start = time.monotonic()
            try:
                result = await registry.dispatch(call.name, ctx, call.arguments)
                latency_ms = int((time.monotonic() - start) * 1000)
                logger.info(
                    "инструмент выполнен | name=%s | user_id=%s | latency_ms=%s",
                    call.name, ctx.user_id, latency_ms,
                )
            except Exception as e:
                latency_ms = int((time.monotonic() - start) * 1000)
                logger.error(
                    "инструмент завершился ошибкой | name=%s | user_id=%s | latency_ms=%s | error=%s",
                    call.name, ctx.user_id, latency_ms, str(e),
                )
                result = {"error": str(e)}
            messages.append(
                LLMMessage(
                    role="tool",
                    tool_call_id=call.id,
                    content=json.dumps(result, ensure_ascii=False),
                )
            )

    logger.error("исчерпан лимит кругов tool-calling | user_id=%s | max_rounds=%s", ctx.user_id, MAX_ROUNDS)
    logger.info("ответ пользователю | user_id=%s | chars=%s", ctx.user_id, len(_NO_FINAL_ANSWER))
    yield _NO_FINAL_ANSWER
