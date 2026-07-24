from pydantic import BaseModel, Field, ConfigDict

class ChatRequest(BaseModel):
    user_id: int
    message: str = Field(min_length=1, max_length=4096)

    model_config = ConfigDict(str_strip_whitespace=True)
