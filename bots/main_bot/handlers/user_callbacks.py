from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import asyncio

from ..states.support import SupportState



from ..keyboards.user_inline import user_start_menu, wallet_menu, market_menu, return_button, sections_menu, offers_menu, push_menu, instructions_menu, channels_announs_menu, settings_menu

router = Router()

#обработчики кнопок стартового меню
@router.callback_query(F.data.startswith("start:"))
async def stars(callback: CallbackQuery):
    key = callback.data.split(":")[1]
    if key == "wallet":
        await callback.message.edit_text("Ваш баланс:\n300$\nВаш замороженный баланс:\n150$", reply_markup=wallet_menu())
        await callback.answer()
    elif key == "market":
        await callback.message.edit_text("Что вы хотите:", reply_markup=market_menu())
        await callback.answer()
    elif key == "offers":
        await callback.message.edit_text("Выберите раздел офферов:", reply_markup=offers_menu())
        await callback.answer()
    elif key == "find":
        await callback.message.edit_text("Введите атикул товара, который вы хотите найти:", reply_markup=return_button())
        await callback.answer()
    elif key == "push":
        await callback.message.edit_text("Введите атикул товара, который вы хотите найти:", reply_markup=push_menu())
        await callback.answer()
    elif key == "VIP_status":
        await callback.message.edit_text("До вип статуса вам не хватает сделок на 400 USDT", reply_markup=return_button())
        await callback.answer()
    elif key == "instructions":
        await callback.message.edit_text("По какому разделу вам нужна помощь?", reply_markup=instructions_menu())
        await callback.answer()
    elif key == "settings":
        await callback.message.edit_text("По какому разделу вам нужна помощь?", reply_markup=settings_menu())
        await callback.answer()
    else:
        await callback.message.edit_text("С данным разделом возникла ошибка", reply_markup=return_button())
        await callback.answer()




@router.callback_query(F.data == "limits")
async def stars(callback: CallbackQuery):
    await callback.message.edit_text("Инфа о комсе и лимитах", reply_markup=return_button())
    await callback.answer()


@router.callback_query(F.data.startswith("channels_list:"))
async def stars(callback: CallbackQuery):
    parts = callback.data.split(":")  # ИЗМЕНЕНО: было callback.query.data
    current_page = int(parts[1])      # ИЗМЕНЕНО: привёл к int
    max_page = int(parts[2])          # ИЗМЕНЕНО: привёл к int

    await callback.message.edit_text(
        "Здесь вы можете приобрести канал",
        reply_markup=channels_announs_menu([], current_page - 1, max_page)
    )
    await callback.answer()


@router.callback_query(F.data == "return_to_start")
async def return_to_start(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки возврата"""
    await state.clear()
    await callback.message.edit_text("Текст текст", reply_markup=user_start_menu())
    await callback.answer()


@router.callback_query(F.data == "sent_smth")
async def return_to_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportState.waiting_for_msg)
    await callback.message.edit_text("Скинь дикпик")
    await callback.answer()
