# TrafikMarket — Telegram Mini App биржа

Платформа для торговли каналами, рекламой и трафиком внутри Telegram Mini App: регистрация продавцов → публикация объявлений → сделки → поддержка. Фоновый контур обновляет данные объявлений через внешние источники (TGStat, MAX Dashboard) независимо от пользовательского API.

**Workflow Docker-only.** На хосте достаточно Docker + Compose v2.

---

## Контейнеры

| Контейнер | Назначение |
|---|---|
| `postgres` | Основная БД: пользователи, объявления, сделки, поддержка |
| `migrate` | Применение Alembic-миграций (`upgrade head`) |
| `app` | FastAPI — публичный HTTP API для mini app |
| `frontend` | nginx — отдача статики mini app |
| `main-bot` | Основной Telegram-бот (aiogram) |
| `support-bot` | Бот поддержки (aiogram) |
| `external-data` | Шлюз внешних данных: TGStat, MAX Dashboard, курс USDT |
| `updater-scheduler` | Раз в сутки формирует задачи обновления → RabbitMQ |
| `updater-worker` | Читает задачи из RabbitMQ, запрашивает `external-data`, пишет в БД |
| `rabbitmq` | Брокер очередей фоновых задач |
| `redis` | FSM-состояние ботов, короткий кэш |
| `minio` | Object Storage для аватаров и медиа объявлений |

---

## Контракт взаимодействий

| Откуда | Куда | Протокол | Назначение |
|---|---|---|---|
| `frontend` | `app` | HTTP | Запросы mini app |
| `app` | `external-data` | HTTP (Docker network) | Данные TGStat / MAX / курс |
| `app` | `postgres` | SQL | Чтение/запись данных mini app |
| `app` | `redis` | Redis | Кэш горячих данных |
| `app` | `minio` | S3 API | Загрузка медиа, presigned URL |
| `main-bot` | `postgres` | SQL | Данные домена main bot |
| `main-bot` | `redis` | Redis | FSM / кэш бота |
| `main-bot` | `minio` | S3 API | Аватары и медиа |
| `support-bot` | `postgres` | SQL | Данные домена support bot |
| `support-bot` | `redis` | Redis | FSM / кэш бота поддержки |
| `support-bot` | `minio` | S3 API | Вложения |
| `updater-scheduler` | `postgres` | SQL | Чтение объявлений для формирования задач |
| `updater-scheduler` | `rabbitmq` | AMQP | Публикация задач обновления |
| `updater-worker` | `rabbitmq` | AMQP | Чтение / ack задач |
| `updater-worker` | `external-data` | HTTP (Docker network) | Обновлённые данные объявлений |
| `updater-worker` | `postgres` | SQL | Запись обновлений |

---

## Файловая карта

```
TrafikMarket/
├── alembic/
│   └── versions/               Миграции БД
├── backend/
│   └── app_backend/            Бэкенд app (FastAPI, DB-layer)
├── dockerfiles/                Dockerfile.migrate, .app, .main-bot, .support-bot
├── docs/                       Документации
├── frontend/                   Frontend 
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Документация

- [docs/database-contract.md](docs/database-contract.md) — полная схема PostgreSQL: таблицы, ограничения, миграции
