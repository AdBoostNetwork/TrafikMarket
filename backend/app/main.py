import os

import uvicorn

from app.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    host = os.environ["APP_HOST"]
    port = int(os.environ["APP_PORT"])
    try:
        logger.info("app запущен | host=%s | port=%s", host, port)
        uvicorn.run("app.app:app", host=host, port=port)
    except Exception as e:
        logger.error("app ошибка запуска | error=%s", str(e))
        raise


if __name__ == "__main__":
    main()
