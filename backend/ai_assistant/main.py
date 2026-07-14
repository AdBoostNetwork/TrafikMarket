import uvicorn

from ai_assistant.core.config import load_ai_settings
from ai_assistant.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    settings = load_ai_settings()
    try:
        logger.info("ai-assistant запущен | host=%s | port=%s", settings.ai_host, settings.ai_port)
        uvicorn.run("ai_assistant.app:app", host=settings.ai_host, port=settings.ai_port)
    except Exception as e:
        logger.error("ai-assistant ошибка запуска | error=%s", str(e))
        raise


if __name__ == "__main__":
    main()
