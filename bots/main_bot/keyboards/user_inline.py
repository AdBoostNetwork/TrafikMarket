from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def user_start_menu():
    """
    Стартовая менюшка
    :return:
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Открыть в приложении", web_app=WebAppInfo(url="https://example.com/")),
            ],
            [
                InlineKeyboardButton(text="Кошелек", callback_data="start:wallet"),
                InlineKeyboardButton(text="Маркет", callback_data="start:market"),
            ],
            [
                InlineKeyboardButton(text="Аукционы", callback_data="start:auction"),
                InlineKeyboardButton(text="Индекс цен", callback_data="start:price_index"),
            ],
            [
                InlineKeyboardButton(text="Траффы", callback_data="start:traffs"),
                InlineKeyboardButton(text="Поиск", callback_data="start:find"),
            ],
            [
                InlineKeyboardButton(text="PUSH", callback_data="start:pushs"),
                InlineKeyboardButton(text="Настройки", callback_data="start:settings"),
            ]
        ]
    )

def wallet_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 Открыть в приложении", web_app=WebAppInfo(url="https://example.com/")),
            ],
            [
                InlineKeyboardButton(text="Вывод⤴️", web_app=WebAppInfo(url="https://example.com/")),
                InlineKeyboardButton(text="Пополнение⤵️", web_app=WebAppInfo(url="https://example.com/")),
            ],
            [
                InlineKeyboardButton(text="Комиссии и лимиты", callback_data="limits"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )


def offers_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Мои офферы", callback_data="my:offers"),
            ],
            [
                InlineKeyboardButton(text="Создать оффер", callback_data="make_offer"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def push_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Текущие настройки Push", callback_data="my:push"),
            ],
            [
                InlineKeyboardButton(text="Добавить раздел, для получения Push", callback_data="make_push"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def instructions_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Раздел 1", callback_data="instr1"),
            ],
            [
                InlineKeyboardButton(text="Раздел 2", callback_data="instr2"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def settings_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Отправить сообщение", callback_data="sent_smth"),
            ],
            [
                InlineKeyboardButton(text="Получить сообщение", callback_data="get_msg"),
            ],
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