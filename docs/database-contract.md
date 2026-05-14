# Database Contract

Техническая спецификация структуры базы данных PostgreSQL для проекта TrafikMarket.

## 1. Миграции

### 1.1 `001_create_users_table` (`2e48773d7daf`)

Создаёт таблицу `users`.

## 2. Таблицы и поля

### 2.1 `users`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `user_id` | `bigint` | да | `—` | Telegram ID пользователя |
| `name` | `text` | да | `—` | Имя пользователя из Telegram |
| `current_balance` | `numeric(10,2)` | да | `0` | Текущий баланс |
| `success_count` | `integer` | да | `0` | Количество успешных сделок |
| `ref_link` | `text` | да | `—` | Реферальная ссылка |
| `referrer_id` | `bigint` | нет | `—` | ID пригласившего пользователя |
| `is_banned` | `boolean` | да | `false` | Флаг бана |
| `avatar_filename` | `text` | нет | `—` | Хэш/имя файла аватарки |
| `good_marks` | `integer` | да | `0` | Количество положительных оценок |
| `bad_marks` | `integer` | да | `0` | Количество отрицательных оценок |
| `reg_date` | `date` | да | `—` | Дата регистрации |
| `vip_status` | `integer` | да | `0` | VIP-статус |
| `theme_mode` | `boolean` | да | `—` | Выбранная тема интерфейса (`false` — светлая, `true` — тёмная) |
| `deals_summ` | `numeric(10,2)` | да | `0` | Сумма сделок |
| `frozen_balance` | `numeric(10,2)` | да | `0` | Замороженный баланс |
| `was_online` | `timestamp with time zone` | да | `—` | Время последней активности пользователя |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `users_pkey` | `user_id` |
| `FOREIGN KEY` | `users_referrer_id_fkey` | `FOREIGN KEY (referrer_id) REFERENCES users(user_id) ON DELETE CASCADE` |
