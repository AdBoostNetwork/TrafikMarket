class SchedulerError(Exception):
    """Базовая ошибка планировщика"""


class RepositoryError(SchedulerError):
    """Ошибка при запросе к БД"""


class PublishError(SchedulerError):
    """Ошибка при публикации задачи в RabbitMQ"""
