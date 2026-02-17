from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from ..keyboards.user_inline import user_dialogs_list_menu, user_dialog_menu, return_button, user_start_menu
from backend.bots_backend.support_bot_db.users_db import can_user_make_appeal, create_new_appeal, close_appeal, get_last_msg, config_tp_bot_buttons

from ..states.support import SupportState

router = Router()

@router.callback_query(lambda c: c.data.startswith("support:"))
async def create_new_dialog(callback: CallbackQuery, state: FSMContext):
    """Обработчик создания нового обращения"""
    user_id = callback.message.from_user.id
    if not can_user_make_appeal(user_id):
        await callback.message.answer("Вы достигли максимального количества обращений в ТП. Чтобы создать новое обращение, закончите диалог по одному из предыдущих"
                                      "Чтобы это сделать, следуйте инструкции:\n"
                                      "/start -> 'Мои активные диалоги💬' -> Выберете одно из ваших обращений -> 'Закончить диалог🔴'")
        await callback.answer()
        return None

    section_key = callback.data.split(":")[1]
    appeal_id = create_new_appeal(user_id, section_key)

    await state.update_data(appeal_id=appeal_id)
    await state.set_state(SupportState.waiting_for_question)

    await callback.message.answer(
        f"Задайте свой вопрос"
    )

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("get_dialog:"))
async def get_dialog(callback: CallbackQuery, state: FSMContext):
    """Обработчик получения информации по обращению"""
    appeal_id = callback.data.split(":")[1]
    await state.update_data(appeal_id=appeal_id)
    text, filenames, is_last_msg_from_user = get_last_msg(appeal_id)
    if is_last_msg_from_user:
        await callback.message.answer('Простите, наша администрация еще не успела вам ответить. Как только вам ответят, вам придет уведомление',
                                      reply_markup=user_dialog_menu())
        await callback.answer()
        return
    await callback.message.answer("Вот последний ответ от поддержки вам:")
    await callback.message.answer(
        f"<pre><code class=\"language-Админ\">{text}</code></pre>",
        parse_mode="HTML",
        reply_markup=user_dialog_menu()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("dialog:"))
async def dialog(callback: CallbackQuery, state: FSMContext):
    """Обработчик команд взаимодействия с обращением"""
    data = await state.get_data()
    appeal_id = data["appeal_id"]
    func_key = callback.data.split(":")[1]
    if func_key == "get_history":

        return
    elif func_key == "finish_dialog":
        close_appeal(appeal_id)
        await callback.message.answer("Ваше обращение успешно закрыто", reply_markup=return_button())
        await callback.answer()
        return
    elif func_key == "answer":
        await state.set_state(SupportState.waiting_for_question)
        await callback.message.answer('Напишите свой следующий вопрос')
        await callback.answer()
        return



@router.callback_query(F.data == "my_dialogs")
async def my_dialogs(callback: CallbackQuery):
    """Обработчик команды получения списка своих обращений"""
    user_id = callback.message.from_user.id
    dialog_list = config_tp_bot_buttons(user_id)
    if not dialog_list:
        await callback.message.answer("У вас нет текущих активных обращений", reply_markup = return_button())
        await callback.answer()
        return
    await callback.message.answer("Выберите обращение, которое вы хотите посмотреть:", reply_markup=user_dialogs_list_menu(dialog_list))
    await callback.answer()




@router.callback_query(F.data == "return_to_start")
async def return_to_start(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки возврата"""
    await state.clear()
    await callback.message.answer("Выберите тему для нового обращения, или перейдите к списку предыдущих.", reply_markup=user_start_menu())
    await callback.answer()