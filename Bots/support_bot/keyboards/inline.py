from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def support_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Финансы", callback_data="support:finance")],
            [InlineKeyboardButton(text="Заказы", callback_data="support:orders")],
            [InlineKeyboardButton(text="Модерация объявлений", callback_data="support:moderation")],
        ]
    )
