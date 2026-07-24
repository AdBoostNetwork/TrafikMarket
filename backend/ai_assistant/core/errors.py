class AppError(Exception):
    """Базовая ошибка приложения"""


class RepositoryError(AppError):
    """Ошибка при запросе к БД → 500"""


class NotFoundError(AppError):
    """Сущность не найдена → 404"""


class LLMError(AppError):
    """Ошибка вызова LLM (OpenRouter) → 502"""
