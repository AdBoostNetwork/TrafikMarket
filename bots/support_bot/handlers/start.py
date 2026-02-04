from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..keyboards.user_inline import user_start_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Здравствуйте! Выберите раздел:",
        reply_markup=user_start_menu(),
    )
