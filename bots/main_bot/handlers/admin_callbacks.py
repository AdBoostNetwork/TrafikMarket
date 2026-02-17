from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from backend.bots_backend.support_bot_db.admins_db import get_last_msg
from ..keyboards.admins_inline import admin_dialog_menu, admin_dialogs_list_menu


router = Router()

@router.callback_query(F.data.startswith("choice:"))
async def get_dialog(callback: CallbackQuery):
    """Обработчик выбора"""
    key = callback.data.split(":")[1]
    if key == "user":
        await callback.message.edit_text(
            "хай",
            reply_markup=user_start_menu()
        )
        await callback.answer()
        return
    elif key == "admin":
        await callback.message.edit_text(
            "хай",
            reply_markup=admins_start_menu()
        )
        await callback.answer()
        return
    elif key == "CEO":
        await callback.message.edit_text(
            "Новый текст сообщения",
            reply_markup=admins_start_menu()
        )
        await callback.answer()

@router.callback_query(F.data == "adm_get_dialogs")
async def adm_get_dialogs(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    circle = data.get("circle", 0)
    dialogs_list, is_end = adm_get_dialogs(circle)
    if is_end:
        await state.update_data(circle=0)
    else:
        await state.update_data(circle=circle+1)
    await callback.message.answer("Выберите вопрос:", reply_markup = admin_dialogs_list_menu(dialogs_list, is_end))
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("adm_get_dialog:"))
async def adm_get_dialog(callback: CallbackQuery, state: FSMContext):
    appeal_id = callback.data.split(":")[1]
    await state.update_data(appeal_id=appeal_id)
    text, filenames, is_last_msg_from_user = get_last_msg(appeal_id)
    await callback.message.answer("Вот последний вопрос юзера:")
    await callback.message.answer(
        f"<pre><code class=\"language-Пользователь\">{text}</code></pre>",
        parse_mode="HTML",
        reply_markup=admin_dialog_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "get_latest_dialog")
async def adm_get_dialogs(callback: CallbackQuery, state: FSMContext):
    appeal_id = callback.data.split(":")[1]
    text, filenames, is_last_msg_from_user = get_last_msg(appeal_id)
    await callback.message.answer("Вот последний вопрос юзера:")
    await callback.message.answer(
        f"<pre><code class=\"language-Пользователь\">{text}</code></pre>",
        parse_mode="HTML",
        reply_markup=admin_dialog_menu()
    )
    await callback.answer()

