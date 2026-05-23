import os
from collections.abc import AsyncGenerator

import aioboto3

from app.logger import get_logger
from app.storage.client import make_storage

logger = get_logger(__name__)

_storage_session: aioboto3.Session | None = None
_storage_endpoint: str | None = None


def init_storage_client() -> None:
    global _storage_session, _storage_endpoint
    _storage_session = make_storage()
    _storage_endpoint = os.environ["MINIO_ENDPOINT"]
    logger.info("storage_client инициализирован")


async def get_storage() -> AsyncGenerator:
    if _storage_session is None or _storage_endpoint is None:
        raise RuntimeError("storage_client не инициализирован")
    async with _storage_session.client("s3", endpoint_url=_storage_endpoint) as s3:
        yield s3
