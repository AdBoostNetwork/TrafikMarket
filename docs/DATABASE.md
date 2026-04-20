# PostgreSQL Schema

Техническая спецификация структуры базы данных PostgreSQL для проекта TrafikMarket.

- Текущая SQL-реализация: `migrations/db_structure.sql`.
- Источник описания: фактическая структура подключенной БД `TrafficMarketApp` (хост `127.0.0.1:5555`).

---

## 1. Логическая структура

| Таблица | Назначение |
|--------|------------|
| `accounts` | Аккаунты пользователей и базовые метрики профиля |
| `ad_requests` | Заявки на объявления рекламы |
| `ads` | Параметры объявлений типа «реклама» |
| `announ_price_history` | История цены объявлений |
| `announs` | Базовая сущность объявления |
| `audience_types` | Справочник типов аудитории |
| `channel_requests` | Заявки на объявления каналов |
| `channels` | Параметры объявлений типа «канал» |
| `countries` | Справочник стран |
| `deals` | Сделки между продавцом и покупателем |
| `imgs` | Изображения объявлений |
| `platforms` | Справочник платформ |
| `topics` | Справочник тематик |
| `traffic` | Параметры объявлений типа «трафик» |
| `traffic_requests` | Заявки на объявления трафика |
| `traffic_types` | Справочник типов трафика |
| `transactions` | Финансовые транзакции пользователей |

---

## 2. Таблицы и поля

### 2.1. `accounts`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `user_id` | `bigint` | да | `—` | — |
| `name` | `character varying(50)` | да | `—` | — |
| `current_balance` | `numeric(10,2)` | да | `0` | — |
| `success_count` | `integer` | да | `0` | — |
| `ref_link` | `character varying(50)` | да | `—` | — |
| `referrer_id` | `bigint` | нет | `—` | — |
| `is_banned` | `boolean` | да | `false` | — |
| `avatar_filename` | `character varying(100)` | нет | `—` | — |
| `good_marks` | `integer` | да | `0` | — |
| `bad_marks` | `integer` | да | `0` | — |
| `reg_date` | `date` | да | `—` | — |
| `vip_status` | `integer` | да | `1` | — |
| `deals_summ` | `numeric(10,2)` | да | `0` | — |
| `frozen_balance` | `numeric(10,2)` | да | `0` | — |
| `was_online` | `character varying(50)` | да | `0` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `accounts_pkey` | `user_id` |
| `FOREIGN KEY` | `fk_referrer` | `FOREIGN KEY (referrer_id) REFERENCES accounts(user_id) ON DELETE SET NULL NOT VALID` |

### 2.2. `ad_requests`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `id` | `integer` | да | `nextval('ad_requests_id_seq'::regclass)` | — |
| `user_id` | `bigint` | да | `—` | — |
| `announ_id` | `integer` | да | `—` | — |
| `format` | `character varying(20)` | да | `—` | — |
| `text` | `character varying(4000)` | да | `—` | — |
| `created_at` | `timestamp with time zone` | нет | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `ad_requests_pkey` | `id` |
| `FOREIGN KEY` | `ad_requests_announ_id_fkey` | `FOREIGN KEY (announ_id) REFERENCES announs(announ_id)` |
| `FOREIGN KEY` | `ad_requests_user_id_fkey` | `FOREIGN KEY (user_id) REFERENCES accounts(user_id)` |

### 2.3. `ads`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `ad_announ_id` | `integer` | да | `—` | — |
| `cover` | `integer` | да | `—` | — |
| `cpm` | `integer` | да | `—` | — |
| `er` | `integer` | да | `—` | — |
| `channel_link` | `character varying(100)` | да | `—` | — |
| `subs_count` | `integer` | да | `—` | — |
| `topic` | `integer` | да | `—` | — |
| `country` | `integer` | да | `—` | — |
| `red_label` | `boolean` | да | `false` | — |
| `black_label` | `boolean` | да | `false` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `ads_pkey` | `ad_announ_id` |
| `FOREIGN KEY` | `ads_country_fkey` | `FOREIGN KEY (country) REFERENCES countries(id)` |
| `FOREIGN KEY` | `ads_topic_fkey` | `FOREIGN KEY (topic) REFERENCES topics(id)` |
| `FOREIGN KEY` | `fk_announ_id` | `FOREIGN KEY (ad_announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

### 2.4. `announ_price_history`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `announ_id` | `integer` | да | `—` | — |
| `price` | `numeric(10,2)` | да | `—` | — |
| `price_date` | `date` | да | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `announ_price_history_pkey` | `announ_id, price_date` |
| `FOREIGN KEY` | `announ_price_history_announ_id_fkey` | `FOREIGN KEY (announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

### 2.5. `announs`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `announ_id` | `integer` | да | `nextval('announs_announ_id_seq'::regclass)` | — |
| `seller_id` | `bigint` | да | `—` | — |
| `type` | `character varying(16)` | да | `—` | — |
| `title` | `character varying(50)` | да | `—` | — |
| `short_text` | `character varying(128)` | да | `—` | — |
| `long_text` | `character varying(1024)` | да | `—` | — |
| `status` | `character varying(16)` | да | `—` | — |
| `article` | `bigint` | да | `nextval('announs_article_seq'::regclass)` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `announs_pkey` | `announ_id` |
| `FOREIGN KEY` | `fk_seller` | `FOREIGN KEY (seller_id) REFERENCES accounts(user_id) ON DELETE CASCADE` |

### 2.6. `audience_types`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `id` | `integer` | да | `nextval('audience_types_id_seq'::regclass)` | — |
| `type_name` | `character varying(100)` | да | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `audience_types_pkey` | `id` |

### 2.7. `channel_requests`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `id` | `integer` | да | `nextval('channel_requests_id_seq'::regclass)` | — |
| `user_id` | `bigint` | да | `—` | — |
| `username` | `character varying(33)` | да | `—` | — |
| `announ_id` | `integer` | нет | `—` | — |
| `status` | `character varying(16)` | нет | `—` | — |
| `created_at` | `timestamp with time zone` | нет | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `channel_requests_pkey` | `id` |
| `FOREIGN KEY` | `channel_requests_announ_id_fkey` | `FOREIGN KEY (announ_id) REFERENCES announs(announ_id)` |
| `FOREIGN KEY` | `channel_requests_user_id_fkey` | `FOREIGN KEY (user_id) REFERENCES accounts(user_id)` |

### 2.8. `channels`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `chn_announ_id` | `integer` | да | `—` | — |
| `chn_type` | `character varying(32)` | да | `—` | — |
| `subs_count` | `integer` | да | `—` | — |
| `cover_count` | `numeric(10,2)` | да | `—` | — |
| `profit` | `numeric(10,2)` | да | `—` | — |
| `on_requests` | `boolean` | да | `—` | — |
| `channel_link` | `character varying(100)` | да | `—` | — |
| `price` | `numeric(10,2)` | да | `—` | — |
| `author` | `boolean` | да | `—` | — |
| `topic` | `integer` | да | `—` | — |
| `country` | `integer` | да | `—` | — |
| `red_label` | `boolean` | да | `false` | — |
| `black_label` | `boolean` | да | `false` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `channels_pkey` | `chn_announ_id` |
| `FOREIGN KEY` | `channels_country_fkey` | `FOREIGN KEY (country) REFERENCES countries(id)` |
| `FOREIGN KEY` | `channels_topic_fkey` | `FOREIGN KEY (topic) REFERENCES topics(id)` |
| `FOREIGN KEY` | `fk_announ_id` | `FOREIGN KEY (chn_announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

### 2.9. `countries`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `id` | `integer` | да | `nextval('countries_id_seq'::regclass)` | — |
| `country_name` | `character varying(100)` | да | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `countries_pkey` | `id` |

### 2.10. `deals`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `deal_id` | `integer` | да | `nextval('deals_deal_id_seq'::regclass)` | — |
| `seller_id` | `bigint` | да | `—` | — |
| `buyer_id` | `bigint` | да | `—` | — |
| `deal_name` | `character varying(50)` | да | `—` | — |
| `price` | `numeric(10,2)` | да | `—` | — |
| `deal_info` | `character varying(50)` | да | `—` | — |
| `type` | `character varying(20)` | да | `—` | — |
| `complete_request` | `boolean` | нет | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `deals_pkey` | `deal_id` |
| `FOREIGN KEY` | `fk_buyer_id` | `FOREIGN KEY (buyer_id) REFERENCES accounts(user_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `fk_seller_id` | `FOREIGN KEY (seller_id) REFERENCES accounts(user_id) ON DELETE CASCADE` |

### 2.11. `imgs`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `img_id` | `integer` | да | `nextval('imgs_img_id_seq'::regclass)` | — |
| `img_announ_id` | `integer` | да | `—` | — |
| `img_filename` | `character varying(50)` | да | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `imgs_pkey` | `img_id` |
| `FOREIGN KEY` | `fk_announ_id` | `FOREIGN KEY (img_announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

### 2.12. `platforms`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `id` | `integer` | да | `nextval('platforms_id_seq'::regclass)` | — |
| `platform_name` | `character varying(100)` | да | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `platforms_pkey` | `id` |

### 2.13. `topics`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `id` | `integer` | да | `nextval('topics_id_seq'::regclass)` | — |
| `topic_name` | `character varying(100)` | да | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `topics_pkey` | `id` |

### 2.14. `traffic`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `trf_announ_id` | `integer` | да | `—` | — |
| `price` | `numeric(10,2)` | да | `—` | — |
| `min_leads` | `integer` | да | `—` | — |
| `max_leads` | `integer` | да | `—` | — |
| `topic` | `integer` | нет | `—` | — |
| `country` | `integer` | нет | `—` | — |
| `platform` | `integer` | нет | `—` | — |
| `audience_type` | `integer` | нет | `—` | — |
| `traffic_type` | `integer` | нет | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `traffic_pkey` | `trf_announ_id` |
| `FOREIGN KEY` | `fk_announ_id` | `FOREIGN KEY (trf_announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `traffic_audience_type_fkey` | `FOREIGN KEY (audience_type) REFERENCES audience_types(id)` |
| `FOREIGN KEY` | `traffic_country_fkey` | `FOREIGN KEY (country) REFERENCES countries(id)` |
| `FOREIGN KEY` | `traffic_platform_fkey` | `FOREIGN KEY (platform) REFERENCES platforms(id)` |
| `FOREIGN KEY` | `traffic_topic_fkey` | `FOREIGN KEY (topic) REFERENCES topics(id)` |
| `FOREIGN KEY` | `traffic_traffic_type_fkey` | `FOREIGN KEY (traffic_type) REFERENCES traffic_types(id)` |

### 2.15. `traffic_requests`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `id` | `integer` | да | `nextval('traffic_requests_id_seq'::regclass)` | — |
| `user_id` | `bigint` | да | `—` | — |
| `announ_id` | `integer` | да | `—` | — |
| `leads_count` | `integer` | да | `—` | — |
| `price` | `numeric(10,2)` | да | `—` | — |
| `created_at` | `timestamp with time zone` | нет | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `traffic_requests_pkey` | `id` |
| `FOREIGN KEY` | `traffic_requests_announ_id_fkey` | `FOREIGN KEY (announ_id) REFERENCES announs(announ_id)` |
| `FOREIGN KEY` | `traffic_requests_user_id_fkey` | `FOREIGN KEY (user_id) REFERENCES accounts(user_id)` |

### 2.16. `traffic_types`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `id` | `integer` | да | `—` | — |
| `traffic_type_name` | `character varying(100)` | да | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `traffic_types_pkey` | `id` |

### 2.17. `transactions`

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|--------|----------------|----------------|--------------|----------|
| `transaction_id` | `integer` | да | `—` | — |
| `user_id` | `bigint` | да | `—` | — |
| `status` | `character varying(16)` | да | `—` | — |
| `summ` | `numeric(10,2)` | да | `—` | — |
| `tr_type` | `character varying(3)` | да | `—` | — |
| `transaction_time` | `timestamp with time zone` | да | `—` | — |
| `sys_msg` | `character varying(64)` | нет | `—` | — |

Ограничения:

| Тип | Имя | Выражение |
|-----|-----|-----------|
| `PRIMARY KEY` | `transactions_pkey` | `transaction_id` |
| `FOREIGN KEY` | `fk_user_id` | `FOREIGN KEY (user_id) REFERENCES accounts(user_id) ON DELETE CASCADE NOT VALID` |

---

## 3. Связи между таблицами

Ключевые связи:

- `announs.seller_id -> accounts.user_id`
- `channels.chn_announ_id -> announs.announ_id`
- `ads.ad_announ_id -> announs.announ_id`
- `traffic.trf_announ_id -> announs.announ_id`
- `imgs.img_announ_id -> announs.announ_id`
- `announ_price_history.announ_id -> announs.announ_id`
- `channel_requests.announ_id -> announs.announ_id`
- `ad_requests.announ_id -> announs.announ_id`
- `traffic_requests.announ_id -> announs.announ_id`
- `deals.seller_id -> accounts.user_id`
- `deals.buyer_id -> accounts.user_id`
- `transactions.user_id -> accounts.user_id`
- `accounts.referrer_id -> accounts.user_id` (self-reference)

Справочные связи для классификации объявлений:

- `channels.topic -> topics.id`
- `channels.country -> countries.id`
- `ads.topic -> topics.id`
- `ads.country -> countries.id`
- `traffic.topic -> topics.id`
- `traffic.country -> countries.id`
- `traffic.platform -> platforms.id`
- `traffic.audience_type -> audience_types.id`
- `traffic.traffic_type -> traffic_types.id`

---

## 4. Примечания по текущей схеме

- В схеме используются PK/FK-ограничения, при этом отдельных непервичных индексов не обнаружено.
- Для части FK задано `ON DELETE CASCADE` (например, связи с `announs`).
- Для `accounts.referrer_id` используется `ON DELETE SET NULL`.
- Для некоторых FK в текущей БД присутствует флаг `NOT VALID` (например, `accounts.fk_referrer`, `transactions.fk_user_id`).
