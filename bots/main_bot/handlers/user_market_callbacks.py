from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import asyncio

from ..states.support import SupportState
from ..keyboards.user_market_inline import sections_menu, channels_announs_menu, return_button, my_announ_menu, not_my_announ_menu

from backend.bots_backend.main_bot_db.main_bot_classes import AnnounsList, AnnounOfAd, AnnounOfTraff, AnnounOfChannel

from backend.bots_backend.main_bot_db.main_bot_db import get_announ

router = Router()

"""Обработчики для инлайн кнопок из раздела маркета в боте"""


"""просмотр чужих объявлений"""
@router.callback_query(F.data == "buy")
async def buy_handler(callback: CallbackQuery):
    await callback.message.edit_text("Выберите раздел", reply_markup=sections_menu("buy"))
    await callback.answer()

@router.callback_query(F.data.startswith("buy:"))
async def buy_sections_handler(callback: CallbackQuery):
    key = callback.data.split(":")[1]
    if key == "channels":
        await callback.message.edit_text("Здесь вы можете приобрести канал", reply_markup=channels_announs_menu([], 0, 9))

    elif key == "ad":
        await callback.message.edit_text("Здесь вы можете приобрести канал",
                                         reply_markup=channels_announs_menu([], 0, 9))
    elif key == "traffic":
        await callback.message.edit_text("<UNK> <UNK> <UNK> <UNK> <UNK>",)

    else:
        await callback.message.edit_text("С этим разделом возникла ошибка. Подождите пока ее устранят, или обратитесь в поддержку")


@router.callback_query(F.data.startswith("announ:"))
async def announ_handler(callback: CallbackQuery):
    article = callback.data.split(":")[1]
    announ = await get_announ(article)
    if announ.seller_id == callback.message.from_user.id:
        keyboard = my_announ_menu(announ.article)
    else:
        keyboard = not_my_announ_menu(announ.article)

    if isinstance(announ, AnnounOfAd):
        await callback.message.edit_text("<UNK> <UNK> <UNK> <UNK> <UNK>", reply_markup=keyboard)
    elif isinstance(announ, AnnounOfChannel):
        await callback.message.edit_text("<UNK> <UNK> <UNK> <UNK>", reply_markup=keyboard)
    elif isinstance(announ, AnnounOfTraff):
        await callback.message.edit_text("<UNK> <UNK> <UNK> <UNK> <UNK>", reply_markup=keyboard)
    else:
        await callback.message.edit_text("С данным объявлением возникла ошибка. Возможно, оно больше не действительно", reply_markup=return_button())
    await callback.answer()





