# updater

Фоновый контур обновления данных объявлений. Состоит из двух контейнеров:

- **`updater-scheduler`** — раз в сутки читает объявления из БД и публикует задачи обновления в очереди RabbitMQ.
- **`updater-worker`** *(не реализован)* — читает задачи из очередей, запрашивает внешние источники данных (`external-data`), обновляет записи в БД.

---

## 1. Назначение и границы

`updater-scheduler` — единственная точка формирования задач обновления. Он не обращается к внешним API и не пишет в БД — только читает объявления и публикует задачи.

Контейнер запускается один раз в сутки в заданный час по UTC+3. После каждого прогона время следующего запуска пересчитывается заново — дрейф цикла исключён. При ошибке выборки из БД или публикации в RabbitMQ цикл пропускается, ошибка логируется, scheduler продолжает работу.

---

## 2. Конфигурация

| Переменная           | Описание                                                  |
|----------------------|-----------------------------------------------------------|
| `DATABASE_URL`       | URL подключения к PostgreSQL (`postgres://...`)           |
| `RABBITMQ_URL`       | URL подключения к RabbitMQ (`amqp://...`)                 |
| `SCHEDULER_RUN_HOUR` | Час запуска по UTC+3 (0–23)                               |
| `TGSTAT_QUEUE`       | Имя очереди задач TGStat                                  |
| `MAXDASH_QUEUE`      | Имя очереди задач MAX Dashboard                           |
| `LOG_LEVEL`          | Уровень логирования (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

`DATABASE_URL` и `RABBITMQ_URL` задаются напрямую в `docker-compose.yml` без переменной окружения хоста.

---

## 3. Поведение при запуске

При старте scheduler вычисляет, сколько секунд осталось до ближайшего наступления `SCHEDULER_RUN_HOUR` по UTC+3, и уходит в `asyncio.sleep`. После пробуждения:

1. Открывает соединение с PostgreSQL (`NullPool` — без пула, соединение на один прогон).
2. Открывает соединение с RabbitMQ (`connect_robust`).
3. Выполняет 10 SQL-запросов — по числу типов объявлений для двух платформ.
4. Формирует задачи, публикует их в очереди RabbitMQ (`PERSISTENT` delivery mode).
5. Закрывает соединение с RabbitMQ.
6. Пересчитывает время следующего запуска и снова уходит в sleep.

---

## 4. Очереди RabbitMQ

Обе очереди объявляются как durable при каждой публикации.

### Структура сообщения

```json
{
  "announ_id": 42,
  "links": [
    { "link_id": null, "url": "https://t.me/channel_name" }
  ]
}
```

`link_id` — идентификатор строки из таблицы `*_links` для сетевых объявлений (нужен worker-у для записи обновлённых данных в правильную строку). Для одиночных объявлений `link_id = null`.

### updater.tgstat

Задачи из шести источников — все с фильтром `tgstat_announ = true AND status = 'active'`:

| Источник           | Тип задачи | `link_id` |
|--------------------|------------|-----------|
| `tg_channels`      | одиночный  | `null`    |
| `tg_chns_nets`     | сетевой    | id из `tg_chns_nets_links`  |
| `tg_ads`           | одиночный  | `null`    |
| `tg_net_ads`       | сетевой    | id из `tg_net_ads_links`    |
| `stories`          | одиночный  | `null`    |
| `stories_nets`     | сетевой    | id из `stories_nets_links`  |

### updater.maxdash

Задачи из четырёх источников — все с фильтром `maxdash_announ = true AND status = 'active'`:

| Источник           | Тип задачи | `link_id` |
|--------------------|------------|-----------|
| `max_channels`     | одиночный  | `null`    |
| `max_chns_nets`    | сетевой    | id из `max_chns_nets_links` |
| `max_ads`          | одиночный  | `null`    |
| `max_net_ads`      | сетевой    | id из `max_net_ads_links`   |

---

## 5. Логи

```bash
# realtime
docker compose logs -f scheduler

# последние 50 строк
docker compose logs --tail=50 scheduler
```

Логи также пишутся в файл внутри контейнера:

```
/app/backend/updater/scheduler/logs/updater-scheduler.log
```

```bash
docker compose exec scheduler cat backend/updater/scheduler/logs/updater-scheduler.log
```

---

## 6. Тестирование без ожидания расписания

Принудительный запуск одного цикла без перезапуска контейнера:

```bash
docker compose exec scheduler python -c "
import asyncio
from updater.scheduler.db.session import make_session
from updater.scheduler.messaging.rabbitmq_client import connect
from updater.scheduler.runner import _run_once

async def main():
    session_factory = make_session()
    connection = await connect()
    try:
        async with session_factory() as session:
            channel = await connection.channel()
            await _run_once(session, channel)
    finally:
        await connection.close()

asyncio.run(main())
"
```

---

## 7. Связанные документы

- `docs/database-contract.md` — схема БД: таблицы объявлений, флаги `tgstat_announ` / `maxdash_announ`
- `backend/updater/rabbitmq_schemas.py` — dataclass-схемы задач (`TgstatUpdateTask`, `MaxdashUpdateTask`, `ChannelLink`)
- `backend/updater/scheduler/` — исходный код scheduler
