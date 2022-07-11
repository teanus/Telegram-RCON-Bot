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


from aiogram import types, Dispatcher
from keyboards import kb_client, kb_admin, kb_other
from provider import sqlite_db


async def start(message: types.Message):
    chat_id = message.chat.id
    if sqlite_db.check_admin_user(chat_id):
        await message.reply('Привет друг! О, ты же админ! Так начни управлять.', reply_markup=kb_admin.main_menu)
    elif sqlite_db.user_exists(chat_id):
        await message.reply('Привет друг. У тебя есть доступ к консоли, удачи!', reply_markup=kb_client.main_menu)
    else:
        await message.reply('Привет друг! Введи /info для отображения информации о боте!',
                            reply_markup=kb_other.main_menu)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'старт'])
