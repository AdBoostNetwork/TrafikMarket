# minio

Object Storage для медиафайлов платформы: аватарки пользователей, изображения объявлений, обои интерфейса, иконки новостей. Совместим с S3 API.

---

## 1. Назначение и границы

`minio` — единственное хранилище бинарных файлов в проекте. В БД хранятся только ключи объектов (`img_key`, `icon_key`, `avatar_filename`), сами файлы лежат в MinIO.

Загрузку файлов выполняют: `app` (изображения объявлений и медиафайлы откликов через API) и боты (аватарки пользователей). Чтение — публичное, без авторизации, по прямому HTTP-URL.

`minio-init` — одноразовый контейнер, который создаёт бакеты и устанавливает политику публичного чтения. Запускается после старта `minio` и завершается.

---

## 2. Конфигурация

| Переменная | Описание |
|---|---|
| `MINIO_ROOT_USER` | Логин администратора MinIO (он же Access Key для S3-клиентов) |
| `MINIO_ROOT_PASSWORD` | Пароль администратора MinIO (он же Secret Key для S3-клиентов) |

Переменные задаются в `docker-compose.yml` с дефолтами `minioadmin` / `minioadmin`. В `app` MinIO-клиент подключается через отдельные переменные:

| Переменная | Значение |
|---|---|
| `MINIO_ENDPOINT` | `http://minio:9000` |
| `MINIO_ACCESS_KEY` | `${MINIO_ROOT_USER}` |
| `MINIO_SECRET_KEY` | `${MINIO_ROOT_PASSWORD}` |
| `MINIO_BUCKET_AVATARS` | `avatars` |
| `MINIO_BUCKET_ANNOUNCEMENTS` | `announcements` |
| `MINIO_BUCKET_WALLPAPERS` | `wallpapers` |
| `MINIO_BUCKET_NEWS` | `news` |
| `MINIO_BUCKET_REQUESTS` | `requests` |

---

## 3. Бакеты и формат ключей

| Бакет | Содержимое | Формат ключа | Пример |
|---|---|---|---|
| `avatars` | Аватарки пользователей | `{user_id}.jpg` | `123456789.jpg` |
| `announcements` | Изображения объявлений | `{uuid}.jpg` | `f47ac10b-58cc-4372-a567.jpg` |
| `requests` | Медиафайлы откликов на рекламу и сторис | `{uuid}.ext` | `a1b2c3d4-5e6f-7890.mp4` |
| `wallpapers` | Обои интерфейса mini app | `{uuid}.jpg` | `3e4d5f6a-1b2c-4d5e.jpg` |
| `news` | Иконки новостей кошелька | `{uuid}.jpg` | `9a8b7c6d-2e3f-4a5b.jpg` |

Все бакеты публичные — объекты доступны по прямому URL без авторизации:

```
http://localhost:9000/{bucket}/{key}
```

Бакет `requests` хранит медиафайлы откликов: фото/видео рекламных откликов (`ad_requests_media.media_key`, до 10 файлов на отклик) и медиафайл отклика на сторис (`stories_requests.story_media`). Расширение файла сохраняется оригинальное.

Контент `wallpapers` и `news` заливается администратором вручную через веб-консоль. Ключ после загрузки вручную прописывается в БД.

---

## 4. Поведение при запуске

`minio-init` запускается после того, как `minio` прошёл healthcheck. Выполняет последовательно:

1. Регистрирует alias `minio` в `mc` с адресом и учётными данными.
2. Создаёт четыре бакета (`--ignore-existing` — идемпотентно при перезапуске).
3. Устанавливает политику `download` (публичное чтение) на каждый бакет.
4. Завершается с кодом `0`.

`app` зависит от `minio-init` с условием `service_completed_successfully` — гарантирует, что бакеты существуют до старта API.

---

## 5. Веб-консоль

MinIO Console доступна на порту `9001`:

```
http://localhost:9001
```

Логин и пароль — значения `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` (по умолчанию `minioadmin` / `minioadmin`).

---

## 6. Связанные документы

- `docs/database-contract.md` — таблицы `images`, `wallpapers`, `news`, `users`: поля `img_key`, `icon_key`, `avatar_filename`
- `docs/app.md` — контейнер `app`: загрузка изображений объявлений через API
