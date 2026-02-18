from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pathlib import Path

from backend.bots_backend.roles import is_admin, is_ceo
from backend.bots_backend.main_bot_db.accounts_db import is_new_user_db, save_new_user_db, change_name_db, change_username_db, change_avatar_id_db
from backend.classes import UserCreateSchema
from ..keyboards.other_buttons import user_mini_app_button
from ..keyboards.user_inline import user_start_menu
from ..keyboards.admins_inline import  admin_choice_menu, CEO_choice_menu

AVAS_DIR = Path("frontend") / "users_avas"
router = Router()


@router.message(CommandStart(), F.chat.type == "private")
async def start_handler(message: Message, state: FSMContext):
    parts = (message.text or "").split(maxsplit=1)
    payload = parts[1].strip() if len(parts) == 2 else None

    await state.clear()

    if not payload:
        await _update_user_info(message)
        await _simple_start(message)
        return

    if payload.startswith("ref:"):
        referi_id = payload.split(":", 1)[1]
        await _update_user_info(message, referi_id=int(referi_id))
        await _simple_start(message)
        return

    # 3) Для аргумента начинающегося с "deal:"
    if payload.startswith("deal:"):
        deal_value = payload.split(":", 1)[1]
        # TODO: обработка сделки
        return


async def _simple_start(message: Message):
    await message.bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=user_mini_app_button()
    )

    user_id = message.from_user.id
    if is_admin(user_id):
        if is_ceo(user_id):
            await message.answer(
                "От лица кого вы хотите войти?",
                reply_markup=CEO_choice_menu()
            )
            return
        await message.answer(
            "Здравствуйте! Выберите раздел:",
            reply_markup=admin_choice_menu(),
        )
        return
    await message.answer(
        "Здравствуйте! Выберите раздел вашего вопроса, или перейдите к своим активным диалогам::",
        reply_markup=user_start_menu(),
    )



async def _update_user_info(message: Message, referi_id: int|None = None):
    user_id = message.from_user.id
    current_name, current_username, current_avatar_id = await _get_tg_params(message)
    is_new, saved_name, saved_username, saved_avatar_id = await is_new_user_db(user_id)
    if is_new:
        new_user = UserCreateSchema(
            user_id=user_id,
            name=current_name,
            tg_username=f"https://t.me/{current_username}",
            avatar_id=current_avatar_id,
            ref_link=f"https://t.me/botnigger_testerbot?ref:{user_id}",
            referi_id=referi_id,
        )
        db_save_scs = await save_new_user_db(new_user)
        avatar_save_scs = await _update_avatar(message, user_id, current_avatar_id)
        if not (db_save_scs and avatar_save_scs):
            await message.answer("Наша платформа сейчас временно недоступна. Приносим извинения за неудобства")

    else:
        # TODO: тут добавить обработку ошибок
        if current_name != saved_name:
            scs = await change_name_db(user_id, current_name)
        if current_username != saved_username:
            scs = await change_username_db(user_id, current_username)
        if current_avatar_id != saved_avatar_id:
            db_save_scs = await change_avatar_id_db(user_id, current_avatar_id)
            avatar_save_scs = await _update_avatar(message, user_id, current_avatar_id)


async def _get_tg_params(message: Message)-> {str, str | None, str| None}:
    user = message.from_user
    name = " ".join(filter(None, [user.first_name, user.last_name])).strip()
    tg_username = f"https://t.me/{user.username}"
    photos = await message.bot.get_user_profile_photos(user_id=user.id, limit=1)
    if photos.total_count == 0:
        return name, tg_username, None
    else:
        photo = photos.photos[0][-1]
        return name, tg_username, photo.file_id

async def _update_avatar(message: Message, user_id, avatar_id: str | None):
    target = AVAS_DIR / f"{user_id}.jpg"
    if avatar_id:
        try:
            tg_file = await message.bot.get_file(avatar_id)
            target = AVAS_DIR / f"{user_id}.jpg"
            await message.bot.download_file(tg_file.file_path, destination=target)
            return True
        except:
            return False
    else:
        try:
            target.unlink()
            return True
        except FileNotFoundError:
            return True
        except:
            return False

