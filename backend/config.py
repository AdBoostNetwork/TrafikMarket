import json
import os
from pathlib import Path
from urllib.parse import unquote, urlparse

from .app_backend.app_classes import AppDbConfig, FastApiConfig


DB_SECRETS_PATH = Path(__file__).resolve().parents[1] / "data" / "db_secrets.json"
APP_SECRETS_PATH = Path(__file__).resolve().parents[1] / "data" / "app_secrets.json"


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def _normalize_db_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def _db_config_from_url(url: str) -> AppDbConfig:
    parsed = urlparse(_normalize_db_url(url))
    return AppDbConfig(
        admin=unquote(parsed.username or ""),
        password=unquote(parsed.password or ""),
        host=parsed.hostname or "localhost",
        port=parsed.port or 5432,
        db_name=(parsed.path or "/").lstrip("/") or "postgres",
    )


db_url = os.getenv("DATABASE_URL")
app_data = load_json(APP_SECRETS_PATH)

if db_url:
    DbConfig = _db_config_from_url(db_url)
else:
    db_data = load_json(DB_SECRETS_PATH)
    DbConfig = AppDbConfig(
        admin = db_data["admin"],
        password = db_data["password"],
        host = db_data["host"],
        port = db_data["port"],
        db_name = db_data["db_name"]
    )

AppConfig = FastApiConfig(
    host = os.getenv("APP_HOST", app_data["host"]),
    port = int(os.getenv("APP_PORT", str(app_data["port"])))
)

tgstat_token = os.getenv("TGSTAT_TOKEN", app_data["tgstat_token"])
