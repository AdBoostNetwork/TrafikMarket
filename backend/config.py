import os
from dotenv import load_dotenv
from .classes import DbConfig


load_dotenv()

MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
SUPP_BOT_TOKEN = os.getenv("SUPPORT_BOT_TOKEN")

DB_CONFIG = DbConfig(
    admin=os.getenv("DB_ADMIN"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    db_name=os.getenv("DB_NAME"),
)