from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from backend.bots_backend.support_bot_db.users_db import config_tp_bot_buttons

def user_start_menu():
    """
    Стартовая менюшка
    :return:
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вывод⤴️", callback_data="support:undep"),
                InlineKeyboardButton(text="Пополнение⤵️", callback_data="support:dep"),
            ],
            [
                InlineKeyboardButton(text="Объявления 🗣", callback_data="support:announs"),
            ],
            [
                InlineKeyboardButton(text="Сделки 🤝", callback_data="support:deals"),
            ],
            [
                InlineKeyboardButton(text="Аккаунт👤", callback_data="support:acc"),
            ],
            [
                InlineKeyboardButton(text="Прочее🖌", callback_data="support:other"),
            ],
            [
                InlineKeyboardButton(text="Мои активные диалоги💬", callback_data="my_dialogs"),
            ]
        ]
    )


def user_dialogs_list_menu(dialog_list):
    """
    Меню с выбором активных диалогов
    :param dialog_list: конфигурационный словарь, ключ - название кнопки, значение - айди диалога
    :return:
    """
    menu=list([InlineKeyboardButton(text=dialog_name, callback_data=f"get_dialog:{dialog_list[dialog_name]}")] for dialog_name in dialog_list)
    menu.append([InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),])
    return InlineKeyboardMarkup(
        inline_keyboard=menu
    )


def user_dialog_menu():
    """Меню для диалога по обращению"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="История диалога⏮️", callback_data="dialog:get_history"),
                InlineKeyboardButton(text="Закончить диалог🔴", callback_data="dialog:finish_dialog"),
            ],
            [
                InlineKeyboardButton(text="Ответить✍️", callback_data="dialog:answer"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def return_button():
    """ Тут даже огузок поймет"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),]
        ]
    )