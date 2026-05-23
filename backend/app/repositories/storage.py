import os

from app.core.errors import StorageError
from app.logger import get_logger

logger = get_logger(__name__)


class StorageRepository:
    def __init__(self, s3) -> None:
        self._s3 = s3
        self._bucket = os.environ["MINIO_BUCKET_ANNOUNCEMENTS"]

    async def upload_announcement_image(self, key: str, data: bytes) -> None:
        try:
            await self._s3.put_object(Bucket=self._bucket, Key=key, Body=data)
            logger.info("upload_announcement_image | key=%s", key)
        except Exception as e:
            logger.error("upload_announcement_image error | key=%s | error=%s", key, str(e))
            raise StorageError(str(e)) from e
