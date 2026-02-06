from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from backend.bots_backend.support_bot_db.users_db import config_tp_bot_buttons

def user_start_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Пополнения⬇️", callback_data="support:dep"),
                InlineKeyboardButton(text="Вывод⬆️", callback_data="support:undep"),
            ],
            [
                InlineKeyboardButton(text="Создание объявлений 🗣", callback_data="support:announs"),
                InlineKeyboardButton(text="Сделки 🤝", callback_data="support:deals"),
            ],
            [
                InlineKeyboardButton(text="Аккаунт👤", callback_data="support:acc"),
                InlineKeyboardButton(text="Прочее🖌", callback_data="support:other"),
            ],
            [
                InlineKeyboardButton(text="Мои активные диалоги💬", callback_data="my_dialogs"),
            ]
        ]
    )


def user_dialogs_list_menu(dialog_list):
    menu=list([InlineKeyboardButton(text=dialog_name, callback_data=f"get_dialog:{dialog_list[dialog_name]}")] for dialog_name in dialog_list)
    menu.append([InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),])
    return InlineKeyboardMarkup(
        inline_keyboard=menu
    )

def no_answer_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть историю диалога⏮️", callback_data="dialog:get_history"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def user_dialog_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть историю диалога⏮️", callback_data="dialog:get_history"),
                InlineKeyboardButton(text="Закончить диалог🔴", callback_data="dialog:finish_dialog"),
            ],
            [
                InlineKeyboardButton(text="Продолжить диалог✍️", callback_data="dialog:answer"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def return_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),]
        ]
    )