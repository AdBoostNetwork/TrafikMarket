#Классы app
from dataclasses import dataclass


@dataclass(frozen=True)
class AppDbConfig:
    """Класс конфигурации данных БД основного приложения"""
    admin: str
    password: str
    host: str
    port: int
    db_name: str


@dataclass(frozen=True)
class FastApiConfig:
    """Класс конфигурации хоста и порта основного приложения"""
    host: str
    port: int