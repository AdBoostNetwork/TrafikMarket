from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import asyncio

from ..states.support import SupportState
from ..keyboards.user_market_inline import sections_menu, announs_list_menu, return_button, my_announ_menu, not_my_announ_menu

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
        await callback.message.edit_text("Здесь вы можете приобрести канал",)

    elif key == "ad":
        await callback.message.edit_text("Здесь вы можете приобрести канал",)
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
        text = _general_announ_text(announ)
        await callback.message.edit_text(text, reply_markup=keyboard)
    elif isinstance(announ, AnnounOfChannel):
        await callback.message.edit_text("<UNK> <UNK> <UNK> <UNK>", reply_markup=keyboard)
    elif isinstance(announ, AnnounOfTraff):
        await callback.message.edit_text("<UNK> <UNK> <UNK> <UNK> <UNK>", reply_markup=keyboard)
    else:
        await callback.message.edit_text("С данным объявлением возникла ошибка. Возможно, оно больше не действительно", reply_markup=return_button())
    await callback.answer()



def _general_announ_text(announ) -> str:
    return f"""Объявление #{announ.article}
    <b>{announ.title}</b>
    
    <a href="https://example.com">{announ.seller_name}</a>
    {announ.seller_deals_number} сделок {announ.seller_scs_deals_percent}% успешных
    
    <blockquote expandable>Короткое описание
    {announ.short_about}</blockquote>

    <blockquote expandable>Длинное описание
    {announ.long_about}</blockquote>"""

def _announ_of_channel_text(announ) -> str:
    general_text=_general_announ_text(announ)
    channel_text = f""" Канал - <a href="{announ.channel_link}">{announ.channel_topic}</a>
"""
    return general_text + channel_text

def _announ_of_traff_text(announ) -> str:
    text=_general_announ_text(announ)
    return text

def _announ_of_ad_text(announ) -> str:
    text=_general_announ_text(announ)
    return text



"""Действия со своим объявлением"""
@router.callback_query(F.data.startswith("get_responses:"))
async def get_responses(callback: CallbackQuery):
    article = callback.data.split(":")[1]


@router.callback_query(F.data.startswith("change_it:"))
async def change_its_handler(callback: CallbackQuery):
    return

@router.callback_query(F.data.startswith("finish_announ:"))
async def finish_announ(callback: CallbackQuery):
    return









