#           Free версия бота проекта LostWeyn
#               Telegram: t.me/lostweyn_project
#  #
#           Контакты разработчика:
#               VK: vk.com/dimawinchester
#               Telegram: t.me/teanus
#               Github: github.com/teanus
#               24serv: talk.24serv.pro/u/teanus
#  #
#  #
#      ██╗      ██████╗ ███████╗████████╗██╗    ██╗███████╗██╗   ██╗███╗   ██╗
#      ██║     ██╔═══██╗██╔════╝╚══██╔══╝██║    ██║██╔════╝╚██╗ ██╔╝████╗  ██║
#      ██║     ██║   ██║███████╗   ██║   ██║ █╗ ██║█████╗   ╚████╔╝ ██╔██╗ ██║
#      ██║     ██║   ██║╚════██║   ██║   ██║███╗██║██╔══╝    ╚██╔╝  ██║╚██╗██║
#      ███████╗╚██████╔╝███████║   ██║   ╚███╔███╔╝███████╗   ██║   ██║ ╚████║
#      ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚══╝╚══╝ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from Config import black_list
from locales import lang
from keyboards import kb_other, kb_admin, kb_client
from minecraft.rcon import command_execute
from provider import sqlite_db
from logger.group_logger import groups_logger
from aiogram.dispatcher import FSMContext


class FsmOther(StatesGroup):
    rcon = State()


async def start(message: types.Message):
    chat_id = message.chat.id
    if sqlite_db.check_admin_user(chat_id):
        await message.reply(lang.message_start, reply_markup=kb_admin.main_menu)
    else:
        await message.reply(lang.message_start, reply_markup=kb_other.main_menu)


async def rcon_cmd(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if sqlite_db.check_admin_user(user_id):
        await message.reply(lang.message_rcon, reply_markup=kb_client.rcon_cancel)
        await FsmOther.rcon.set()
    elif sqlite_db.user_exists(chat_id):
        await message.reply(lang.message_rcon, reply_markup=kb_client.rcon_cancel)
        await FsmOther.rcon.set()
    else:
        await message.reply(lang.message_no_access)


async def cancel_state_rcon(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if sqlite_db.check_admin_user(chat_id):
        await message.reply(lang.message_start, reply_markup=kb_admin.main_menu)
        await state.finish()
    else:
        await message.reply(lang.message_start, reply_markup=kb_other.main_menu)
        await state.finish()


async def get_command(message: types.Message, state: FSMContext):
    low = message.text.lower()
    command = low.split(' ', 1)
    user_id = message.from_user.id
    if command[0] in black_list:
        await groups_logger('RCON: ', user_id, message.text)
        await message.reply(lang.message_block_commands)
    else:
        await groups_logger('RCON: ', user_id, message.text)
        await message.reply(lang.message_command_response + command_execute(low))
        await message.answer(lang.message_rcon_state)
        await state.set_state(FsmOther.rcon)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'старт'])
    dp.register_message_handler(rcon_cmd, Text(startswith=[lang.button_message_rcon, '/rcon'], ignore_case=True))
    dp.register_message_handler(cancel_state_rcon, Text(equals=lang.button_message_cancel),
                                state=FsmOther.rcon)
    dp.register_message_handler(get_command, state=FsmOther.rcon)

