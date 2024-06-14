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

common_router = Router()


@common_router.message()
async def start(message: Message) -> None:
    chat_id = message.chat.id
    menu = await get_main_menu(chat_id)
    text = (
        "Привет друг! О, ты же админ! Так начни управлять."
        if await db.check_admin_user(chat_id)
        else (
            "Привет друг. У тебя есть доступ к консоли, удачи!"
            if await db.user_exists(chat_id)
            else "Привет друг! Введи /info для отображения информации о боте!"
        )
    )
    await message.reply(text, reply_markup=menu)


def register_routers() -> None:
    common_router.message.register(start)
