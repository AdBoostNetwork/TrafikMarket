import json
import time
from collections.abc import AsyncIterator

from ai_assistant.agent.context import ToolContext
from ai_assistant.agent.registry import Registry
from ai_assistant.llm.client import LLMClient, LLMMessage
from ai_assistant.logger import get_logger
from ai_assistant.memory.repository import (
    add_message,
    get_facts,
    get_or_create_current_dialog,
    get_recent_messages,
)

logger = get_logger(__name__)

MAX_ROUNDS = 6
PAUSE_SECONDS = 3600      # час без сообщений → новый разговор
HISTORY_LIMIT = 20        # сколько последних сообщений отдаём модели

_EMPTY_ANSWER = "Не удалось сформулировать ответ, попробуйте переспросить."
_NO_FINAL_ANSWER = "Не смог собрать ответ, переформулируйте вопрос."


async def stream_chat(
    client: LLMClient,
    system_prompt: str,
    message: str,
    ctx: ToolContext,
    registry: Registry,
) -> AsyncIterator[str]:
    """Один ход разговора: контекст из истории, цикл tool-calling, сохранение обеих реплик."""
    dialog_id = await get_or_create_current_dialog(ctx.ai_db, ctx.user_id, PAUSE_SECONDS)
    history = await get_recent_messages(ctx.ai_db, dialog_id, HISTORY_LIMIT)

    facts = await get_facts(ctx.ai_db, ctx.user_id)
    system_content = system_prompt
    if facts:
        facts_block = "\n".join(f"[{f.id}] {f.content}" for f in facts)
        system_content = f"{system_prompt}\n\n## Что ты знаешь о пользователе\n{facts_block}"

    messages = [LLMMessage(role="system", content=system_content)]
    messages.extend(LLMMessage(role=m.role, content=m.content) for m in history)
    messages.append(LLMMessage(role="user", content=message))

    final = _NO_FINAL_ANSWER
    for round_number in range(1, MAX_ROUNDS + 1):
        resp = await client.complete(messages, tools=registry.specs())

        if not resp.tool_calls:
            final = resp.text or _EMPTY_ANSWER
            break

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
    else:
        logger.error("исчерпан лимит кругов tool-calling | user_id=%s | max_rounds=%s", ctx.user_id, MAX_ROUNDS)

    await add_message(ctx.ai_db, dialog_id, "user", message)
    await add_message(ctx.ai_db, dialog_id, "assistant", final)
    await ctx.ai_db.commit()
    logger.info(
        "ответ пользователю | user_id=%s | dialog_id=%s | chars=%s",
        ctx.user_id, dialog_id, len(final),
    )
    yield final
