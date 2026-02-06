# Конфигуратор app

import json
from pathlib import Path

from app_classes import AppDbConfig


DB_SECRETS_PATH = Path(__file__).resolve().parents[2] / "data" / "db_secrets.json"


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


db_data = load_json(DB_SECRETS_PATH)

DbConfig = AppDbConfig(
    admin = db_data["admin"],
    password = db_data["password"],
    host = db_data["host"],
    port = db_data["port"],
    db_name = db_data["db_name"]
)