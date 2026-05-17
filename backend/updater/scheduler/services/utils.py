from itertools import groupby
from typing import TypeVar

from updater.rabbitmq_schemas import ChannelLink, TgstatUpdateTask, MaxdashUpdateTask

Task = TypeVar("Task", TgstatUpdateTask, MaxdashUpdateTask)


def build_single_tasks(rows, task_class: type[Task]) -> list[Task]:
    return [
        task_class(
            announ_id=row["announ_id"],
            links=[ChannelLink(link_id=None, url=row["link"])],
        )
        for row in rows
    ]


def build_network_tasks(rows, task_class: type[Task]) -> list[Task]:
    tasks = []
    sorted_rows = sorted(rows, key=lambda r: r["announ_id"])
    for announ_id, group in groupby(sorted_rows, key=lambda r: r["announ_id"]):
        links = [ChannelLink(link_id=row["link_id"], url=row["url"]) for row in group]
        tasks.append(task_class(announ_id=announ_id, links=links))
    return tasks
