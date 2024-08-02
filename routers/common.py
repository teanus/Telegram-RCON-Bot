#
#           Контакты разработчика:
#               VK: vk.com/dimawinchester
#               Telegram: t.me/teanus
#               Github: github.com/teanus
#
#
#
# ████████╗███████╗ █████╗ ███╗   ██╗██╗   ██╗███████╗
# ╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██║   ██║██╔════╝
#    ██║   █████╗  ███████║██╔██╗ ██║██║   ██║███████╗
#    ██║   ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║╚════██║
#    ██║   ███████╗██║  ██║██║ ╚████║╚██████╔╝███████║
#    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝


from aiogram import Router
from aiogram.types import Message

from keyboards import get_main_menu
from provider import db
from render_template import render_template_jinja

common_router = Router()


async def start(message: Message) -> None:
    """
    Обрабатывает команду /start. Отправляет пользователю начальное сообщение с меню и информацией о доступе.

    :param message: Сообщение от пользователя.
    :type message: types.Message
    :return: None
    """
    chat_id = message.chat.id
    menu = await get_main_menu(chat_id)
    is_admin = await db.check_admin(chat_id)
    has_access = await db.user_exists(chat_id)
    context = {"is_admin": is_admin, "has_access": has_access}

    text = render_template_jinja("common/start.jinja2", **context)
    await message.reply(text, reply_markup=menu)


async def register_routers() -> None:
    """
    Регистрация routers для обработки сообщений common.

    :return: None
    """
    common_router.message.register(start)
