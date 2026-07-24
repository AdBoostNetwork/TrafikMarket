from collections.abc import AsyncIterator

from ai_assistant.llm.client import LLMClient, LLMMessage


async def stream_chat(client: LLMClient, system_prompt: str, message: str) -> AsyncIterator[str]:
    messages = [
        LLMMessage(role="system", content=system_prompt),
        LLMMessage(role="user", content=message),
    ]
    async for piece in client.stream_text(messages):
        yield piece
