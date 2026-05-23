from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Статус успешного выполнения операции"""
    success: bool = True
