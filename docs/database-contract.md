# Database Contract

Техническая спецификация структуры базы данных PostgreSQL для проекта TrafikMarket.

## 1. Миграции

### `001_create_users_table`

Создаёт таблицу `users`.

### `002_create_dictionaries`

Создаёт таблицы справочников: `countries`, `topics`, `platforms`, `traffic_types`, `audience_types`.

### `003_seed_dictionaries`

Заполняет таблицы справочников начальными значениями.

### `004_create_announs`

Создаёт таблицы `announ_types`, `announs`, `images` и sequence `announs_article_seq` (старт с 30000).

### `005_create_tg_channels`

Создаёт таблицу `tg_channels` (единичные Telegram-каналы).

### `006_create_tg_chns_nets`

Создаёт таблицы `tg_chns_nets`, `tg_chns_nets_links`, `tg_chns_nets_topics`, `tg_chns_nets_countries` (сети Telegram-каналов).

### `007_create_max_channels`

Создаёт таблицу `max_channels` (единичные каналы MAX).

### `008_create_max_chns_nets`

Создаёт таблицы `max_chns_nets`, `max_chns_nets_links`, `max_chns_nets_topics` (сети каналов MAX).

### `009_create_tg_ads`

Создаёт таблицы `tg_ads` и `tg_ads_prices` (реклама в единичных Telegram-каналах).

### `010_create_tg_net_ads`

Создаёт таблицы `tg_net_ads`, `tg_net_ads_links`, `tg_net_ads_prices`, `tg_net_ads_topics`, `tg_net_ads_countries` (реклама в сетях Telegram-каналов).

### `011_create_max_ads`

Создаёт таблицы `max_ads` и `max_ads_prices` (реклама в единичных каналах MAX).

### `012_create_max_net_ads`

Создаёт таблицы `max_net_ads`, `max_net_ads_links`, `max_net_ads_prices`, `max_net_ads_topics` (реклама в сетях каналов MAX).

### `013_create_stories`

Создаёт таблицы `stories` и `stories_prices` (реклама через сторис в единичных Telegram-каналах).

### `014_create_stories_nets`

Создаёт таблицы `stories_nets`, `stories_nets_links`, `stories_nets_prices`, `stories_nets_topics`, `stories_nets_countries` (реклама через сторис в сетях Telegram-каналов).

### `015_create_traffic`

Создаёт таблицу `traffic` (объявления трафика).

## 2. Спецификация таблиц

### 1. `users`

Пользователи платформы. Основная сущность — регистрируется при первом обращении к боту. Хранит финансовый профиль (балансы), репутацию (оценки), реферальную принадлежность и метаданные аккаунта.

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

### 2 `countries`

Справочник стран. Используется для геотаргетинга объявлений.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID страны |
| `country_name` | `text` | да | `—` | Название страны |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `countries_pkey` | `id` |
| `UNIQUE` | `countries_country_name_key` | `country_name` |

### 3 `topics`

Справочник тематик. Используется для классификации объявлений по тематике контента.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID тематики |
| `topic_name` | `text` | да | `—` | Название тематики |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `topics_pkey` | `id` |
| `UNIQUE` | `topics_topic_name_key` | `topic_name` |

### 4 `platforms`

Справочник платформ трафика. Используется для указания источника трафика в объявлениях.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID платформы |
| `platform_name` | `text` | да | `—` | Название платформы трафика |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `platforms_pkey` | `id` |
| `UNIQUE` | `platforms_platform_name_key` | `platform_name` |

### 5 `traffic_types`

Справочник типов трафика (прямой пост, инвайтинг, таргет и др.). Используется в объявлениях типа «трафик».

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID типа трафика |
| `traffic_type_name` | `text` | да | `—` | Название типа трафика |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `traffic_types_pkey` | `id` |
| `UNIQUE` | `traffic_types_traffic_type_name_key` | `traffic_type_name` |

### 6 `audience_types`

Справочник типов аудитории (мца, жца, смешанная). Используется в объявлениях типа «трафик».

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID типа аудитории |
| `type_name` | `text` | да | `—` | Название типа аудитории |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `audience_types_pkey` | `id` |
| `UNIQUE` | `audience_types_type_name_key` | `type_name` |

### 7 `announ_types`

Справочник типов объявлений (каналы, реклама, трафик и их разновидности по платформам). Расширяется по мере добавления новых типов.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID типа объявления |
| `type_name` | `text` | да | `—` | Название типа объявления |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `announ_types_pkey` | `id` |
| `UNIQUE` | `announ_types_type_name_key` | `type_name` |

### 8 `announs`

Базовая сущность объявления. Хранит общие поля для всех типов объявлений. Детальные параметры вынесены в отдельные таблицы, связанные с `announ_id`. Артикул (`article`) — человекочитаемый идентификатор для отображения пользователю и поиска через бот.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `announ_id` | `serial` | да | `auto` | ID объявления |
| `seller_id` | `bigint` | да | `—` | Telegram ID продавца |
| `type` | `integer` | да | `—` | Тип объявления (FK → `announ_types.id`) |
| `title` | `varchar(50)` | да | `—` | Название объявления |
| `short_text` | `varchar(128)` | да | `—` | Краткое описание |
| `long_text` | `varchar(1024)` | нет | `—` | Подробное описание |
| `status` | `varchar(16)` | да | `—` | Статус объявления |
| `article` | `bigint` | да | `nextval('announs_article_seq')` | Артикул объявления (sequence с 30000) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `announs_pkey` | `announ_id` |
| `UNIQUE` | `announs_article_key` | `article` |
| `FOREIGN KEY` | `announs_seller_id_fkey` | `FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `announs_type_fkey` | `FOREIGN KEY (type) REFERENCES announ_types(id) ON DELETE CASCADE` |

### 9 `tg_channels`

Параметры объявлений типа «единичный Telegram-канал». Связана 1:1 с `announs` через `chn_announ_id`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `chn_announ_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |
| `price` | `numeric(10,2)` | да | `—` | Цена канала |
| `chn_type` | `boolean` | нет | `—` | Тип канала |
| `topic` | `integer` | да | `—` | Тематика (FK → `topics.id`) |
| `country` | `integer` | да | `—` | Страна (FK → `countries.id`) |
| `subs_count` | `integer` | нет | `—` | Количество подписчиков |
| `cover_count` | `numeric(10,2)` | нет | `—` | Охват канала |
| `err` | `numeric(10,2)` | нет | `—` | ERR |
| `profitability` | `numeric(10,2)` | нет | `—` | Доходность |
| `on_requests` | `boolean` | да | `—` | Принимает заявки |
| `requests_count` | `integer` | нет | `—` | Количество заявок |
| `author` | `boolean` | да | `—` | Авторский канал |
| `red_label` | `boolean` | да | `false` | Красная метка |
| `black_label` | `boolean` | да | `false` | Чёрная метка |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_channels_pkey` | `chn_announ_id` |
| `FOREIGN KEY` | `tg_channels_chn_announ_id_fkey` | `FOREIGN KEY (chn_announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `tg_channels_topic_fkey` | `FOREIGN KEY (topic) REFERENCES topics(id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `tg_channels_country_fkey` | `FOREIGN KEY (country) REFERENCES countries(id) ON DELETE CASCADE` |

### 10 `tg_chns_nets`

Параметры объявлений типа «сеть Telegram-каналов». Связана 1:1 с `announs`. Ссылки, тематики и страны вынесены в отдельные таблицы.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `net_announ_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `price` | `numeric(10,2)` | да | `—` | Цена сети |
| `subs_count` | `integer` | нет | `—` | Суммарное количество подписчиков |
| `cover_count` | `numeric(10,2)` | нет | `—` | Суммарный охват сети |
| `err` | `numeric(10,2)` | нет | `—` | ERR сети |
| `profitability` | `numeric(10,2)` | нет | `—` | Доходность |
| `on_requests` | `boolean` | да | `—` | Принимает заявки |
| `requests_count` | `integer` | нет | `—` | Количество заявок |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_chns_nets_pkey` | `net_announ_id` |
| `FOREIGN KEY` | `tg_chns_nets_net_announ_id_fkey` | `FOREIGN KEY (net_announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

### 11 `tg_chns_nets_links`

Ссылки на отдельные каналы внутри сети. Метки `red_label` и `black_label` задаются на уровне каждого канала.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `net_announ_id` | `integer` | да | `—` | ID объявления-сети (FK → `tg_chns_nets.net_announ_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |
| `red_label` | `boolean` | да | `false` | Красная метка |
| `black_label` | `boolean` | да | `false` | Чёрная метка |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_chns_nets_links_pkey` | `id` |
| `FOREIGN KEY` | `tg_chns_nets_links_net_announ_id_fkey` | `FOREIGN KEY (net_announ_id) REFERENCES tg_chns_nets(net_announ_id) ON DELETE CASCADE` |

### 12 `tg_chns_nets_topics`

Тематики сети каналов. Связь многие-ко-многим между `tg_chns_nets` и `topics`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `net_announ_id` | `integer` | да | `—` | ID объявления-сети (FK → `tg_chns_nets.net_announ_id`) |
| `topic_id` | `integer` | да | `—` | ID тематики (FK → `topics.id`) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_chns_nets_topics_pkey` | `(net_announ_id, topic_id)` |
| `FOREIGN KEY` | `tg_chns_nets_topics_net_announ_id_fkey` | `FOREIGN KEY (net_announ_id) REFERENCES tg_chns_nets(net_announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `tg_chns_nets_topics_topic_id_fkey` | `FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE` |

### 13 `tg_chns_nets_countries`

Страны сети каналов. Связь многие-ко-многим между `tg_chns_nets` и `countries`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `net_announ_id` | `integer` | да | `—` | ID объявления-сети (FK → `tg_chns_nets.net_announ_id`) |
| `country_id` | `integer` | да | `—` | ID страны (FK → `countries.id`) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_chns_nets_countries_pkey` | `(net_announ_id, country_id)` |
| `FOREIGN KEY` | `tg_chns_nets_countries_net_announ_id_fkey` | `FOREIGN KEY (net_announ_id) REFERENCES tg_chns_nets(net_announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `tg_chns_nets_countries_country_id_fkey` | `FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE` |

### 14 `max_channels`

Параметры объявлений типа «единичный канал MAX». Связана 1:1 с `announs` через `chn_announ_id`. В отличие от `tg_channels` не имеет поля страны и меток.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `chn_announ_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |
| `price` | `numeric(10,2)` | да | `—` | Цена канала |
| `chn_type` | `boolean` | нет | `—` | Тип канала |
| `topic` | `integer` | да | `—` | Тематика (FK → `topics.id`) |
| `subs_count` | `integer` | нет | `—` | Количество подписчиков |
| `cover_count` | `numeric(10,2)` | нет | `—` | Охват канала |
| `err` | `numeric(10,2)` | нет | `—` | ERR |
| `profitability` | `numeric(10,2)` | нет | `—` | Доходность |
| `on_requests` | `boolean` | да | `—` | Принимает заявки |
| `requests_count` | `integer` | нет | `—` | Количество заявок |
| `author` | `boolean` | да | `—` | Авторский канал |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_channels_pkey` | `chn_announ_id` |
| `FOREIGN KEY` | `max_channels_chn_announ_id_fkey` | `FOREIGN KEY (chn_announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `max_channels_topic_fkey` | `FOREIGN KEY (topic) REFERENCES topics(id) ON DELETE CASCADE` |

### 15 `max_chns_nets`

Параметры объявлений типа «сеть каналов MAX». Связана 1:1 с `announs`. В отличие от `tg_chns_nets` не имеет таблицы стран и меток на ссылках.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `net_announ_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `price` | `numeric(10,2)` | да | `—` | Цена сети |
| `subs_count` | `integer` | нет | `—` | Суммарное количество подписчиков |
| `cover_count` | `numeric(10,2)` | нет | `—` | Суммарный охват сети |
| `err` | `numeric(10,2)` | нет | `—` | ERR сети |
| `profitability` | `numeric(10,2)` | нет | `—` | Доходность |
| `on_requests` | `boolean` | да | `—` | Принимает заявки |
| `requests_count` | `integer` | нет | `—` | Количество заявок |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_chns_nets_pkey` | `net_announ_id` |
| `FOREIGN KEY` | `max_chns_nets_net_announ_id_fkey` | `FOREIGN KEY (net_announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

### 16 `max_chns_nets_links`

Ссылки на отдельные каналы внутри сети MAX. Без меток.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `net_announ_id` | `integer` | да | `—` | ID объявления-сети (FK → `max_chns_nets.net_announ_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_chns_nets_links_pkey` | `id` |
| `FOREIGN KEY` | `max_chns_nets_links_net_announ_id_fkey` | `FOREIGN KEY (net_announ_id) REFERENCES max_chns_nets(net_announ_id) ON DELETE CASCADE` |

### 17 `max_chns_nets_topics`

Тематики сети каналов MAX. Связь многие-ко-многим между `max_chns_nets` и `topics`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `net_announ_id` | `integer` | да | `—` | ID объявления-сети (FK → `max_chns_nets.net_announ_id`) |
| `topic_id` | `integer` | да | `—` | ID тематики (FK → `topics.id`) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_chns_nets_topics_pkey` | `(net_announ_id, topic_id)` |
| `FOREIGN KEY` | `max_chns_nets_topics_net_announ_id_fkey` | `FOREIGN KEY (net_announ_id) REFERENCES max_chns_nets(net_announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `max_chns_nets_topics_topic_id_fkey` | `FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE` |

### 18 `tg_ads`

Параметры объявлений типа «реклама в единичном Telegram-канале». Связана 1:1 с `announs`. Цены по форматам размещения вынесены в `tg_ads_prices`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |
| `topic` | `integer` | да | `—` | Тематика (FK → `topics.id`) |
| `country` | `integer` | да | `—` | Страна (FK → `countries.id`) |
| `subs_count` | `integer` | да | `—` | Количество подписчиков |
| `cover_count` | `numeric(10,2)` | да | `—` | Охват канала |
| `err` | `numeric(10,2)` | нет | `—` | ERR |
| `red_label` | `boolean` | да | `false` | Красная метка |
| `black_label` | `boolean` | да | `false` | Чёрная метка |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_ads_pkey` | `ad_id` |
| `FOREIGN KEY` | `tg_ads_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `tg_ads_topic_fkey` | `FOREIGN KEY (topic) REFERENCES topics(id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `tg_ads_country_fkey` | `FOREIGN KEY (country) REFERENCES countries(id) ON DELETE CASCADE` |

### 19 `tg_ads_prices`

Цены по форматам размещения рекламы. Формат — произвольная строка (например, `1/24`, `1/48`). Одно объявление может иметь несколько форматов с разными ценами.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `tg_ads.ad_id`) |
| `format` | `text` | да | `—` | Формат размещения |
| `price` | `numeric(10,2)` | да | `—` | Цена за формат |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_ads_prices_pkey` | `id` |
| `FOREIGN KEY` | `tg_ads_prices_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES tg_ads(ad_id) ON DELETE CASCADE` |

### 20 `tg_net_ads`

Параметры объявлений типа «реклама в сети Telegram-каналов». Связана 1:1 с `announs`. Ссылки, цены, тематики и страны вынесены в отдельные таблицы.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `subs_count` | `integer` | да | `—` | Суммарное количество подписчиков |
| `cover_count` | `numeric(10,2)` | да | `—` | Суммарный охват сети |
| `err` | `numeric(10,2)` | нет | `—` | ERR |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_net_ads_pkey` | `ad_id` |
| `FOREIGN KEY` | `tg_net_ads_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

### 21 `tg_net_ads_links`

Ссылки на каналы внутри рекламной сети. Метки задаются на уровне каждого канала.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `tg_net_ads.ad_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |
| `red_label` | `boolean` | да | `false` | Красная метка |
| `black_label` | `boolean` | да | `false` | Чёрная метка |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_net_ads_links_pkey` | `id` |
| `FOREIGN KEY` | `tg_net_ads_links_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES tg_net_ads(ad_id) ON DELETE CASCADE` |

### 22 `tg_net_ads_prices`

Цены по форматам размещения рекламы в сети. Формат — произвольная строка.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `tg_net_ads.ad_id`) |
| `format` | `text` | да | `—` | Формат размещения |
| `price` | `numeric(10,2)` | да | `—` | Цена за формат |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_net_ads_prices_pkey` | `id` |
| `FOREIGN KEY` | `tg_net_ads_prices_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES tg_net_ads(ad_id) ON DELETE CASCADE` |

### 23 `tg_net_ads_topics`

Тематики рекламной сети. Связь многие-ко-многим между `tg_net_ads` и `topics`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `tg_net_ads.ad_id`) |
| `topic_id` | `integer` | да | `—` | ID тематики (FK → `topics.id`) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_net_ads_topics_pkey` | `(ad_id, topic_id)` |
| `FOREIGN KEY` | `tg_net_ads_topics_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES tg_net_ads(ad_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `tg_net_ads_topics_topic_id_fkey` | `FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE` |

### 24 `tg_net_ads_countries`

Страны рекламной сети. Связь многие-ко-многим между `tg_net_ads` и `countries`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `tg_net_ads.ad_id`) |
| `country_id` | `integer` | да | `—` | ID страны (FK → `countries.id`) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `tg_net_ads_countries_pkey` | `(ad_id, country_id)` |
| `FOREIGN KEY` | `tg_net_ads_countries_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES tg_net_ads(ad_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `tg_net_ads_countries_country_id_fkey` | `FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE` |

### 25 `max_ads`

Параметры объявлений типа «реклама в единичном канале MAX». Связана 1:1 с `announs`. В отличие от `tg_ads` не имеет страны и меток, тематика одна (не список). Цены по форматам вынесены в `max_ads_prices`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |
| `topic` | `integer` | да | `—` | Тематика (FK → `topics.id`) |
| `subs_count` | `integer` | да | `—` | Количество подписчиков |
| `cover_count` | `numeric(10,2)` | да | `—` | Охват канала |
| `err` | `numeric(10,2)` | нет | `—` | ERR |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_ads_pkey` | `ad_id` |
| `FOREIGN KEY` | `max_ads_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `max_ads_topic_fkey` | `FOREIGN KEY (topic) REFERENCES topics(id) ON DELETE CASCADE` |

### 26 `max_ads_prices`

Цены по форматам размещения рекламы в MAX. Формат — произвольная строка.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `max_ads.ad_id`) |
| `format` | `text` | да | `—` | Формат размещения |
| `price` | `numeric(10,2)` | да | `—` | Цена за формат |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_ads_prices_pkey` | `id` |
| `FOREIGN KEY` | `max_ads_prices_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES max_ads(ad_id) ON DELETE CASCADE` |

### 27 `max_net_ads`

Параметры объявлений типа «реклама в сети каналов MAX». Связана 1:1 с `announs`. В отличие от `tg_net_ads` не имеет стран и меток на ссылках.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `subs_count` | `integer` | да | `—` | Суммарное количество подписчиков |
| `cover_count` | `numeric(10,2)` | да | `—` | Суммарный охват сети |
| `err` | `numeric(10,2)` | нет | `—` | ERR |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_net_ads_pkey` | `ad_id` |
| `FOREIGN KEY` | `max_net_ads_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

### 28 `max_net_ads_links`

Ссылки на каналы внутри рекламной сети MAX. Без меток.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `max_net_ads.ad_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_net_ads_links_pkey` | `id` |
| `FOREIGN KEY` | `max_net_ads_links_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES max_net_ads(ad_id) ON DELETE CASCADE` |

### 29 `max_net_ads_prices`

Цены по форматам размещения рекламы в сети MAX. Формат — произвольная строка.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `max_net_ads.ad_id`) |
| `format` | `text` | да | `—` | Формат размещения |
| `price` | `numeric(10,2)` | да | `—` | Цена за формат |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_net_ads_prices_pkey` | `id` |
| `FOREIGN KEY` | `max_net_ads_prices_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES max_net_ads(ad_id) ON DELETE CASCADE` |

### 30 `max_net_ads_topics`

Тематики рекламной сети MAX. Связь многие-ко-многим между `max_net_ads` и `topics`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `ad_id` | `integer` | да | `—` | ID объявления (FK → `max_net_ads.ad_id`) |
| `topic_id` | `integer` | да | `—` | ID тематики (FK → `topics.id`) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `max_net_ads_topics_pkey` | `(ad_id, topic_id)` |
| `FOREIGN KEY` | `max_net_ads_topics_ad_id_fkey` | `FOREIGN KEY (ad_id) REFERENCES max_net_ads(ad_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `max_net_ads_topics_topic_id_fkey` | `FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE` |

### 31 `stories`

Параметры объявлений типа «реклама через сторис в единичном Telegram-канале». Связана 1:1 с `announs`. Структура аналогична `tg_ads`. Цены по форматам вынесены в `stories_prices`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `story_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |
| `topic` | `integer` | да | `—` | Тематика (FK → `topics.id`) |
| `country` | `integer` | да | `—` | Страна (FK → `countries.id`) |
| `subs_count` | `integer` | да | `—` | Количество подписчиков |
| `cover_count` | `numeric(10,2)` | да | `—` | Охват канала |
| `err` | `numeric(10,2)` | нет | `—` | ERR |
| `red_label` | `boolean` | да | `false` | Красная метка |
| `black_label` | `boolean` | да | `false` | Чёрная метка |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `stories_pkey` | `story_id` |
| `FOREIGN KEY` | `stories_story_id_fkey` | `FOREIGN KEY (story_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `stories_topic_fkey` | `FOREIGN KEY (topic) REFERENCES topics(id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `stories_country_fkey` | `FOREIGN KEY (country) REFERENCES countries(id) ON DELETE CASCADE` |

### 32 `stories_prices`

Цены по форматам размещения рекламы через сторис. Формат — произвольная строка.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `story_id` | `integer` | да | `—` | ID объявления (FK → `stories.story_id`) |
| `format` | `text` | да | `—` | Формат размещения |
| `price` | `numeric(10,2)` | да | `—` | Цена за формат |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `stories_prices_pkey` | `id` |
| `FOREIGN KEY` | `stories_prices_story_id_fkey` | `FOREIGN KEY (story_id) REFERENCES stories(story_id) ON DELETE CASCADE` |

### 33 `stories_nets`

Параметры объявлений типа «реклама через сторис в сети Telegram-каналов». Связана 1:1 с `announs`. Метки вынесены на уровень каждой ссылки в `stories_nets_links`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `story_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `subs_count` | `integer` | да | `—` | Суммарное количество подписчиков |
| `cover_count` | `numeric(10,2)` | да | `—` | Суммарный охват сети |
| `err` | `numeric(10,2)` | нет | `—` | ERR |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `stories_nets_pkey` | `story_id` |
| `FOREIGN KEY` | `stories_nets_story_id_fkey` | `FOREIGN KEY (story_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

### 34 `stories_nets_links`

Ссылки на каналы внутри сети сторис. Метки задаются на уровне каждого канала.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `story_id` | `integer` | да | `—` | ID объявления (FK → `stories_nets.story_id`) |
| `link` | `text` | да | `—` | Ссылка на канал |
| `red_label` | `boolean` | да | `false` | Красная метка |
| `black_label` | `boolean` | да | `false` | Чёрная метка |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `stories_nets_links_pkey` | `id` |
| `FOREIGN KEY` | `stories_nets_links_story_id_fkey` | `FOREIGN KEY (story_id) REFERENCES stories_nets(story_id) ON DELETE CASCADE` |

### 35 `stories_nets_prices`

Цены по форматам размещения сторис в сети. Формат — произвольная строка.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `serial` | да | `auto` | ID записи |
| `story_id` | `integer` | да | `—` | ID объявления (FK → `stories_nets.story_id`) |
| `format` | `text` | да | `—` | Формат размещения |
| `price` | `numeric(10,2)` | да | `—` | Цена за формат |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `stories_nets_prices_pkey` | `id` |
| `FOREIGN KEY` | `stories_nets_prices_story_id_fkey` | `FOREIGN KEY (story_id) REFERENCES stories_nets(story_id) ON DELETE CASCADE` |

### 36 `stories_nets_topics`

Тематики сети сторис. Связь многие-ко-многим между `stories_nets` и `topics`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `story_id` | `integer` | да | `—` | ID объявления (FK → `stories_nets.story_id`) |
| `topic_id` | `integer` | да | `—` | ID тематики (FK → `topics.id`) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `stories_nets_topics_pkey` | `(story_id, topic_id)` |
| `FOREIGN KEY` | `stories_nets_topics_story_id_fkey` | `FOREIGN KEY (story_id) REFERENCES stories_nets(story_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `stories_nets_topics_topic_id_fkey` | `FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE` |

### 37 `stories_nets_countries`

Страны сети сторис. Связь многие-ко-многим между `stories_nets` и `countries`.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `story_id` | `integer` | да | `—` | ID объявления (FK → `stories_nets.story_id`) |
| `country_id` | `integer` | да | `—` | ID страны (FK → `countries.id`) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `stories_nets_countries_pkey` | `(story_id, country_id)` |
| `FOREIGN KEY` | `stories_nets_countries_story_id_fkey` | `FOREIGN KEY (story_id) REFERENCES stories_nets(story_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `stories_nets_countries_country_id_fkey` | `FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE` |

### 38 `traffic`

Параметры объявлений типа «трафик». Связана 1:1 с `announs`. Все атрибуты — ссылки на справочники.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `traffic_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `price` | `numeric(10,2)` | да | `—` | Цена за подписчика |
| `min_subs` | `integer` | да | `—` | Минимальное количество подписчиков |
| `max_subs` | `integer` | да | `—` | Максимальное количество подписчиков |
| `topic` | `integer` | да | `—` | Тематика (FK → `topics.id`) |
| `country` | `integer` | да | `—` | Страна (FK → `countries.id`) |
| `platform` | `integer` | да | `—` | Платформа трафика (FK → `platforms.id`) |
| `type` | `integer` | да | `—` | Тип трафика (FK → `traffic_types.id`) |
| `auditory` | `integer` | да | `—` | Тип аудитории (FK → `audience_types.id`) |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `traffic_pkey` | `traffic_id` |
| `FOREIGN KEY` | `traffic_traffic_id_fkey` | `FOREIGN KEY (traffic_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `traffic_topic_fkey` | `FOREIGN KEY (topic) REFERENCES topics(id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `traffic_country_fkey` | `FOREIGN KEY (country) REFERENCES countries(id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `traffic_platform_fkey` | `FOREIGN KEY (platform) REFERENCES platforms(id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `traffic_type_fkey` | `FOREIGN KEY (type) REFERENCES traffic_types(id) ON DELETE CASCADE` |
| `FOREIGN KEY` | `traffic_auditory_fkey` | `FOREIGN KEY (auditory) REFERENCES audience_types(id) ON DELETE CASCADE` |

### 39 `images`

Изображения объявлений. Хранит ключи файлов в MinIO; одно объявление может иметь несколько изображений. Удаляются каскадно вместе с объявлением.

| Столбец | Тип / атрибут | Обязательность | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | `bigserial` | да | `auto` | ID изображения |
| `img_announ_id` | `integer` | да | `—` | ID объявления (FK → `announs.announ_id`) |
| `img_key` | `text` | да | `—` | Ключ изображения в MinIO |

Ограничения:

| Тип | Имя | Выражение |
|---|---|---|
| `PRIMARY KEY` | `images_pkey` | `id` |
| `FOREIGN KEY` | `images_img_announ_id_fkey` | `FOREIGN KEY (img_announ_id) REFERENCES announs(announ_id) ON DELETE CASCADE` |

## 3. Начальные данные справочников

Начальные значения добавляются миграцией `003_seed_dictionaries`.