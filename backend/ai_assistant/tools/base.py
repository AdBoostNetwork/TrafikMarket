import abc
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from ai_assistant.agent.context import ToolContext


class Tool(abc.ABC):
    name: str
    description: str
    Params: type[BaseModel]  # без user_id — он приходит из ctx, не от модели

    @abc.abstractmethod
    async def execute(self, ctx: "ToolContext", params: BaseModel) -> dict:
        ...

    def tool_spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.Params.model_json_schema(),
            },
        }
