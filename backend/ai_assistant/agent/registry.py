from ai_assistant.agent.context import ToolContext
from ai_assistant.logger import get_logger
from ai_assistant.tools.base import Tool

logger = get_logger(__name__)


class Registry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool_cls: type[Tool]) -> type[Tool]:
        tool = tool_cls()
        if tool.name in self._tools:
            raise ValueError(f"инструмент с именем '{tool.name}' уже зарегистрирован")
        self._tools[tool.name] = tool
        logger.info("инструмент зарегистрирован | name=%s", tool.name)
        return tool_cls

    def specs(self) -> list[dict]:
        return [tool.tool_spec() for tool in self._tools.values()]

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError:
            raise ValueError(f"неизвестный инструмент '{name}'") from None

    async def dispatch(self, name: str, ctx: ToolContext, arguments: dict) -> dict:
        tool = self.get(name)
        params = tool.Params.model_validate(arguments)
        return await tool.execute(ctx, params)


registry = Registry()
register = registry.register
