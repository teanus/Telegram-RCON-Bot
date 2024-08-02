from aiogram import types

from keyboards import kb_admin, kb_client, kb_other
from provider import db


async def get_main_menu(user_id: int) -> types.ReplyKeyboardMarkup:
    """
    Получает главное меню в зависимости от роли пользователя.

    :param user_id: ID пользователя.
    :return: Главное меню в виде клавиатуры.
    :rtype: types.ReplyKeyboardMarkup
    """
    if await db.check_admin(user_id):
        return kb_admin.main_menu
    elif await db.user_exists(user_id):
        return kb_client.main_menu
    return kb_other.main_menu
