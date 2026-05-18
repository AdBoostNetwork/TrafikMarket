# App Container

FastAPI-бэкенд Telegram Mini App. Обслуживает фронтенд: профиль, объявления, справочники, заказы.

## Структура пакета

```text
backend/app/
  main.py                        # точка входа: читает APP_HOST, APP_PORT из env, запускает uvicorn
  app.py                         # FastAPI инстанс, middleware, lifespan, подключение роутеров
  logger.py                      # get_logger(name) — логи пишутся в logs/app.log в корне проекта
  api/
    routers/                     # HTTP-слой, только маршрутизация и обработка ошибок
    schemas/                     # Pydantic response-модели
  services/                      # бизнес-логика use-case уровня
  repositories/                  # SQL-запросы (text queries), без бизнес-логики
  external_data/                 # клиент контейнера external-data (не реализован)
  db/
    session.py                   # make_session() → async_sessionmaker (NullPool)
    dependencies.py              # get_session — FastAPI Depends, init_session_factory()
  core/
    errors.py                    # иерархия ошибок
```

## Переменные окружения

| Переменная | Описание |
|---|---|
| `DATABASE_URL` | URL PostgreSQL (`postgres://...`) |
| `APP_HOST` | Хост uvicorn |
| `APP_PORT` | Порт uvicorn |
| `LOG_LEVEL` | Уровень логирования (по умолчанию `INFO`) |

## Запуск локально

```bash
export DATABASE_URL="postgres://postgres:postgres@localhost:5432/traffmarket?sslmode=disable"
export APP_HOST="127.0.0.1"
export APP_PORT="8000"
export PYTHONPATH=/path/to/TrafikMarket/backend

python -m app.main
```

## Архитектура запроса

```
Router → Depends(get_session) → Repository(session) → Service(repo) → Response
```

- `session_factory` инициализируется один раз в `lifespan` при старте
- Сессия живёт ровно один запрос, открывается и закрывается через `yield`
- Репозиторий получает сессию в конструктор, бизнес-логики не содержит
- Сервис получает репозиторий в конструктор, работает только с доменными объектами

## Ошибки

```python
AppError             # базовая
├── RepositoryError  # ошибка БД → HTTP 500
└── NotFoundError    # сущность не найдена → HTTP 404
```

## Роутеры

### `profile` — `/profile`

| Метод | URL | Описание |
|---|---|---|
| GET | `/profile/balance` | Свободный баланс пользователя (`current_balance - frozen_balance`) |

### `dictionaries` — `/dictionaries`

| Метод | URL | Описание |
|---|---|---|
| GET | `/dictionaries/wallpapers` | Список обоев интерфейса (`wallpaper_name`, `img_key`) |
| GET | `/dictionaries/countries` | Справочник стран (`id`, `name`) |
| GET | `/dictionaries/topics` | Справочник тематик (`id`, `name`) |
| GET | `/dictionaries/platforms` | Справочник платформ трафика (`id`, `name`) |
| GET | `/dictionaries/traffic-types` | Справочник типов трафика (`id`, `name`) |
| GET | `/dictionaries/audience-types` | Справочник типов аудитории (`id`, `name`) |

## Стиль кода

- SQL — `text(...)` inline в методе репозитория; модульные константы только для длинных или переиспользуемых запросов
- Логи: `logger.info("описание | key=value")`, русские описания
- Репозитории — классы с `__init__(self, session: AsyncSession)`
- Сервисы — классы с `__init__(self, repo: XxxRepository)`
- Dataclass `@dataclass(frozen=True)` — для внутренних структур между слоями
- Pydantic `BaseModel` — только для API-схем
