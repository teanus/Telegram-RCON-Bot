from aiogram import types
from provider import db
from keyboards import kb_admin, kb_client, kb_other


async def get_main_menu(user_id: int) -> types.ReplyKeyboardMarkup:
    if await db.check_admin_user(user_id):
        return kb_admin.main_menu
    elif await db.user_exists(user_id):
        return kb_client.main_menu
    return kb_other.main_menu
