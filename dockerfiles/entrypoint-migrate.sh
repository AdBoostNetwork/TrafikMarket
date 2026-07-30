#!/bin/sh
set -e

: "${AI_APP_PASSWORD:?AI_APP_PASSWORD is not set}"
: "${DATABASE_URL:?DATABASE_URL is not set}"

MAIN_DB="traffmarket"
AI_DB="traffmarket_ai"
AI_ROLE="ai_assistant"

# URL той же БД, но с базой помощника вместо основной — для шага 3 (GRANT в новой БД)
AI_ADMIN_URL=$(printf '%s' "$DATABASE_URL" | sed "s#/${MAIN_DB}#/${AI_DB}#")

# 1) роль-владелец БД помощника (идемпотентно); пароль экранируем — в SQL-литерал он не биндится
if [ -z "$(psql "$DATABASE_URL" -tAc "SELECT 1 FROM pg_roles WHERE rolname='${AI_ROLE}'")" ]; then
  ESCAPED_PASSWORD=$(printf '%s' "$AI_APP_PASSWORD" | sed "s/'/''/g")
  psql "$DATABASE_URL" -c "CREATE ROLE ${AI_ROLE} LOGIN PASSWORD '${ESCAPED_PASSWORD}'"
fi

# 2) сама база помощника (владелец — роль); CREATE DATABASE не живёт в транзакции, поэтому вне alembic
if [ -z "$(psql "$DATABASE_URL" -tAc "SELECT 1 FROM pg_database WHERE datname='${AI_DB}'")" ]; then
  psql "$DATABASE_URL" -c "CREATE DATABASE ${AI_DB} OWNER ${AI_ROLE}"
fi

# 3) права на схему public новой БД (PostgreSQL 16 не даёт CREATE в public по умолчанию) — идемпотентно
psql "$AI_ADMIN_URL" -c "GRANT ALL ON SCHEMA public TO ${AI_ROLE}"

# 4) миграции основной БД (как раньше)
exec alembic upgrade head
