from dataclasses import dataclass


@dataclass()
class Appeal:
    user_from_id: int
    last_msg: str
    chat: str
    status: str