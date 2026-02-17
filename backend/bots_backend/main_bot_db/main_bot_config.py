import json
from pathlib import Path

from backend.classes import DbConfig


DB_SECRETS_PATH = Path(__file__).resolve().parents[3] / "data" / "db_secrets.json"


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

db_data = load_json(DB_SECRETS_PATH)

db_info = DbConfig(
    admin = db_data["admin"],
    password = db_data["password"],
    host = db_data["host"],
    port = db_data["port"],
    db_name = db_data["db_name"]
)