from dataclasses import dataclass


@dataclass(frozen=True)
class DbConfig:
    """Класс конфигурации данных БД"""
    admin: str
    password: str
    host: str
    port: int
    db_name: str


@dataclass(frozen=True)
class UserCreateSchema:
    """Класс данных пользователя при создании аккаунта"""
    user_id: int
    name: str
    tg_username: str | None
    avatar_id: int | None
    referi_if: int | None