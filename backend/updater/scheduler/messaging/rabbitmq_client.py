import dataclasses
import json
import os

import aio_pika
from aio_pika.abc import AbstractChannel

from updater.scheduler.logger import get_logger
from updater.rabbitmq_schemas import TgstatUpdateTask, MaxdashUpdateTask
from updater.scheduler.core.errors import PublishError

logger = get_logger(__name__)

TGSTAT_QUEUE = os.getenv("TGSTAT_QUEUE")
MAXDASH_QUEUE = os.getenv("MAXDASH_QUEUE")


async def connect() -> aio_pika.abc.AbstractRobustConnection:
    return await aio_pika.connect_robust(os.environ["RABBITMQ_URL"])


async def publish_task(channel: AbstractChannel, task: TgstatUpdateTask | MaxdashUpdateTask, queue_name: str) -> None:
    try:
        queue = await channel.declare_queue(queue_name, durable=True)
        body = json.dumps(dataclasses.asdict(task)).encode()
        await channel.default_exchange.publish(
            aio_pika.Message(body=body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key=queue.name,
        )
    except Exception as e:
        logger.error("Ошибка публикации задачи | queue=%s | announ_id=%d | %s", queue_name, task.announ_id, str(e))
        raise PublishError(f"publish_task queue={queue_name} announ_id={task.announ_id}: {e}") from e
