from dataclasses import dataclass


@dataclass()
class DbConfig:
    admin: str
    password: str
    host: str
    port: int
    db_name: str


@dataclass()
class Appeal:
    user_from_id: int
    last_msg: str
    chat: str
    status: str
