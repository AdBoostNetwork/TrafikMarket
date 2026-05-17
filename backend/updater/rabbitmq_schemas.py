from dataclasses import dataclass


@dataclass(frozen=True)
class ChannelLink:
    """Ссылка канала объявления"""
    link_id: int | None
    url: str


@dataclass(frozen=True)
class TgstatUpdateTask:
    """Задача обновления объявления через TGStat"""
    announ_id: int
    links: list[ChannelLink]


@dataclass(frozen=True)
class MaxdashUpdateTask:
    """Задача обновления объявления через MAX Dashboard"""
    announ_id: int
    links: list[ChannelLink]
