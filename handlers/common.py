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


from aiogram import Dispatcher, types

from keyboards import kb_admin, kb_client, kb_other, get_main_menu
from provider import db


async def start(message: types.Message):
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


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start)
