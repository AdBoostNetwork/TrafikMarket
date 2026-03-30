from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def market_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Купить", callback_data="buy"),
                InlineKeyboardButton(text="Продать", callback_data="sell"),
            ],
            [
                InlineKeyboardButton(text="Мои объявления 🗣", callback_data="my:announs"),
            ],
            [
                InlineKeyboardButton(text="Мои сделки 🤝", callback_data="my:deals"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]

        ]
    )

def sections_menu(action: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Каналы", callback_data=f"{action}:channels"),
            ],
            [
                InlineKeyboardButton(text="Реклама", callback_data=f"{action}:ad"),
            ],
            [
                InlineKeyboardButton(text="Траффик", callback_data=f"{action}:traffic"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def announs_list_menu(announs_list: set, current_index: int, max_index: int, announs_type: str):
    """
    :param announs_type: channel/ad/traff, нужен для фильтров

    """
    if announs_type == "channel":
        filtr_button = [InlineKeyboardButton(text="Фильтры и сортировка", callback_data="channel_filtrs")]
    elif announs_type == "ad":
        filtr_button = [InlineKeyboardButton(text="Фильтры и сортировка", callback_data="ad_filtrs")]
    elif announs_type == "traffic":
        filtr_button = [InlineKeyboardButton(text="Фильтры и сортировка", callback_data="traff_filtrs")]
    else:
        filtr_button = None

    return InlineKeyboardMarkup(
        inline_keyboard=[
            filtr_button,
            list([InlineKeyboardButton(text=dialog_name, callback_data=f"get_announ:{announs_list[dialog_name]}")] for dialog_name in announs_list),
            *_enumerate_config(current_index, max_index),
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def not_my_announ_menu(article: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть в приложении", web_app=WebAppInfo(url="https://example.com/")),
            ],
            [
                InlineKeyboardButton(text="Купить", callback_data=f"buy_it:{article}"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="buy"),
            ]

        ]
    )

def not_my_announ_of_traff_menu(article: int, ad_format: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть в приложении", web_app=WebAppInfo(url="https://example.com/")),
            ],
            #TODO: тут нужно реализовать список форатов рекламы
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="buy"),
            ]
        ]
    )


def my_announ_menu(article: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть в приложении", web_app=WebAppInfo(url="https://example.com/")),
            ],
            [
                InlineKeyboardButton(text="Посмотреть отклики", callback_data=f"get_responses:{article}"),
            ],
            [
                InlineKeyboardButton(text="Редактировать объявление", callback_data=f"change_it:{article}"),
            ],
            [
                InlineKeyboardButton(text="Закрыть объявление", callback_data=f"finish_announ:{article}"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="start:market"),
            ]
        ]
    )


def return_to_announs_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="buy"),
            ]
        ]
    )

def return_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def _enumerate_config(current_index: int, max_index: int):
    if max_index < 1:
        max_index = 1
    current_index = max(0, min(current_index, max_index - 1))
    current_page = current_index + 1  # 1-based

    def make_button(text: str, page: int) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=text,
            callback_data=f"channels_list:{page}:{max_index}"
        )

    # <= 5 страниц — просто показать все
    if max_index <= 5:
        visible_pages = list(range(1, max_index + 1))
        row = [
            make_button(f"•{p}•" if p == current_page else f"{p}", p)
            for p in visible_pages
        ]
        return [row]

    # > 5 — всегда 5 кнопок
    if current_page <= 3:
        visible_pages = [1, 2, 3, 4, max_index]
    elif current_page >= max_index - 2:
        visible_pages = [1, max_index - 3, max_index - 2, max_index - 1, max_index]
    else:
        visible_pages = [1, current_page - 1, current_page, current_page + 1, max_index]

    # флаги крайних зон
    is_near_start = current_page in (1, 2)
    is_near_end = current_page in (max_index, max_index - 1)

    row: list[InlineKeyboardButton] = []

    for page in visible_pages:
        # текущая
        if page == current_page:
            text = f"•{page}•"

        # первая
        elif page == 1:
            text = "<<1" if current_page >= 4 else "1"

        # последняя
        elif page == max_index:
            text = f"{max_index}>>" if (max_index - current_page) >= 3 else f"{max_index}"

        else:
            text = f"{page}"

            # спец-правило старта: ">" только у 4
            if is_near_start:
                if page == 4:
                    text = f"{page}>"

            # спец-правило конца: "<" только у (max-3)
            elif is_near_end:
                if page == (max_index - 3):
                    text = f"<{page}"

            # обычные правила середины
            else:
                if page == current_page - 1 and page not in (1, 2):
                    text = f"<{page}"
                elif page == current_page + 1 and page not in (max_index, max_index - 1):
                    text = f"{page}>"

        row.append(make_button(text, page))

    return [row]