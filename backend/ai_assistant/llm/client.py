import json
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import cast

from openai import AsyncOpenAI, AsyncStream, OpenAIError
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from ai_assistant.core.config import AISettings
from ai_assistant.core.errors import LLMError
from ai_assistant.logger import get_logger

logger = get_logger(__name__)

_TIMEOUT_SECONDS = 60.0
_MAX_RETRIES = 3


@dataclass(frozen=True)
class ToolCall:
    """Запрос модели на вызов инструмента (id — метка вызова для сопоставления результата)."""
    id: str
    name: str
    arguments: dict


@dataclass(frozen=True)
class LLMMessage:
    """Сообщение для модели. Наш формат; перевод в формат провайдера — внутри клиента."""
    role: str                               # "system" | "user" | "assistant" | "tool"
    content: str | None = None
    tool_calls: list[ToolCall] | None = None    # для ассистентского сообщения с запросом инструментов
    tool_call_id: str | None = None             # для сообщения-результата инструмента


@dataclass(frozen=True)
class LLMUsage:
    prompt_tokens: int
    completion_tokens: int


@dataclass(frozen=True)
class LLMResponse:
    """Итог не-стрим вызова: либо tool_calls (пусто, если модель ответила текстом), либо text."""
    text: str | None
    tool_calls: list[ToolCall]
    finish_reason: str | None
    usage: LLMUsage | None


class LLMClient:
    """Единственная точка выхода в LLM. Типы провайдера наружу не отдаёт — только наши DTO."""

    def __init__(self, client: AsyncOpenAI, model: str, temperature: float, max_tokens: int) -> None:
        self._client = client
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    async def complete(self, messages: list[LLMMessage], tools: list[dict] | None = None) -> LLMResponse:
        """Не-стрим вызов для tool-раундов: вернёт список ToolCall либо финальный текст целиком."""
        params = self._base_params(messages, tools)
        start = time.monotonic()
        try:
            resp = cast(ChatCompletion, await self._client.chat.completions.create(**params))
        except OpenAIError as e:
            logger.error("llm complete ошибка | model=%s | error=%s", self._model, type(e).__name__)
            raise LLMError(f"complete: {type(e).__name__}") from e

        latency_ms = int((time.monotonic() - start) * 1000)
        choice = resp.choices[0]
        usage = self._parse_usage(resp.usage)
        logger.info(
            "llm complete | model=%s | latency_ms=%s | finish=%s | prompt=%s | completion=%s",
            self._model, latency_ms, choice.finish_reason,
            usage.prompt_tokens if usage else None,
            usage.completion_tokens if usage else None,
        )
        return LLMResponse(
            text=choice.message.content,
            tool_calls=self._parse_tool_calls(choice.message.tool_calls),
            finish_reason=choice.finish_reason,
            usage=usage,
        )

    async def stream_text(self, messages: list[LLMMessage], tools: list[dict] | None = None) -> AsyncIterator[str]:
        """Стрим для финального ответа: отдаёт текст кусочками (дельтами)."""
        params = self._base_params(messages, tools)
        params["stream"] = True
        params["stream_options"] = {"include_usage": True}
        usage = None
        try:
            stream = cast(AsyncStream[ChatCompletionChunk], await self._client.chat.completions.create(**params))
            async for chunk in stream:
                if chunk.usage is not None:
                    usage = chunk.usage
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if delta is not None and delta.content:
                        yield delta.content
        except OpenAIError as e:
            logger.error("llm stream ошибка | model=%s | error=%s", self._model, type(e).__name__)
            raise LLMError(f"stream_text: {type(e).__name__}") from e

        logger.info(
            "llm stream завершён | model=%s | prompt=%s | completion=%s",
            self._model,
            usage.prompt_tokens if usage else None,
            usage.completion_tokens if usage else None,
        )

    async def aclose(self) -> None:
        await self._client.close()

    def _base_params(self, messages: list[LLMMessage], tools: list[dict] | None) -> dict:
        params: dict = {
            "model": self._model,
            "messages": self._to_openai_messages(messages),
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
        }
        if tools:
            params["tools"] = tools
        return params

    @staticmethod
    def _to_openai_messages(messages: list[LLMMessage]) -> list[dict]:
        result: list[dict] = []
        for m in messages:
            if m.role == "assistant" and m.tool_calls:
                result.append({
                    "role": "assistant",
                    "content": m.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.name,
                                "arguments": json.dumps(tc.arguments, ensure_ascii=False),
                            },
                        }
                        for tc in m.tool_calls
                    ],
                })
            elif m.role == "tool":
                result.append({"role": "tool", "tool_call_id": m.tool_call_id, "content": m.content or ""})
            else:
                result.append({"role": m.role, "content": m.content or ""})
        return result

    @staticmethod
    def _parse_tool_calls(raw: list | None) -> list[ToolCall]:
        if not raw:
            return []
        calls: list[ToolCall] = []
        for tc in raw:
            try:
                arguments = json.loads(tc.function.arguments) if tc.function.arguments else {}
            except json.JSONDecodeError as e:
                logger.error("llm битые аргументы инструмента | name=%s | error=%s", tc.function.name, str(e))
                raise LLMError(f"tool_arguments: {tc.function.name}") from e
            calls.append(ToolCall(id=tc.id, name=tc.function.name, arguments=arguments))
        return calls

    @staticmethod
    def _parse_usage(usage) -> LLMUsage | None:
        if usage is None:
            return None
        return LLMUsage(prompt_tokens=usage.prompt_tokens, completion_tokens=usage.completion_tokens)


def make_llm_client(settings: AISettings) -> LLMClient:
    client = AsyncOpenAI(
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_url,
        timeout=_TIMEOUT_SECONDS,
        max_retries=_MAX_RETRIES,
    )
    return LLMClient(client, settings.llm_model, settings.temperature, settings.max_tokens)
