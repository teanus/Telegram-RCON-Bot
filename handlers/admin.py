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
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from Config import black_list
from keyboards import kb_admin
from locales import lang
from provider import sqlite_db
from logger.group_logger import groups_logger


class AdminState(StatesGroup):
    settings = State()
    commands = State()
    command_add = State()
    command_remove = State()
    give = State()
    add_user = State()
    add_admin = State()


async def settings_panel(message: types.Message):
    chat_id = message.chat.id
    if sqlite_db.check_admin_user(chat_id):
        await message.reply(lang.message_panel_settings, reply_markup=kb_admin.admin_panel_menu)
        await AdminState.settings.set()


async def cancel_settings(message: types.Message, state: FSMContext):
    await message.reply(lang.message_panel_cancel, reply_markup=kb_admin.main_menu)
    await state.finish()


async def back_to_state_settings(message: types.Message, state: FSMContext):
    await message.reply(lang.message_back, reply_markup=kb_admin.admin_panel_menu)
    await state.set_state(AdminState.settings)


async def back_state_add(message: types.Message, state: FSMContext):
    await message.reply(lang.message_back, reply_markup=kb_admin.admin_panel_add)
    await state.set_state(AdminState.give)


async def back_state_commands_switch(message: types.Message, state: FSMContext):
    await message.reply(lang.message_back, reply_markup=kb_admin.panel_commands_switch)
    await state.set_state(AdminState.commands)


async def add_roles_switch(message: types.message):
    await message.reply(lang.message_panel_give, reply_markup=kb_admin.admin_panel_add)
    await AdminState.give.set()


async def roles_add_user(message: types.Message):
    await message.reply(lang.message_add_user, reply_markup=kb_admin.admin_back)
    await AdminState.add_user.set()


async def roles_add_admin(message: types.Message):
    await message.reply(lang.message_add_super_admin, reply_markup=kb_admin.admin_back)
    await AdminState.add_admin.set()


async def get_user_id(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if sqlite_db.user_exists(message.text):
        await message.reply(str(message.chat.id) + lang.message_panel_user_is_exists)
        await state.set_state(AdminState.add_user)
    else:
        await groups_logger('Set user role: ', user_id, message.text)
        await message.reply(str(message.chat.id) + sqlite_db.user_add(message.text))


async def get_admin_id(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if sqlite_db.check_admin_user(message.text):
        await message.reply(lang.message_panel_admin_is_exists)
        await state.set_state(AdminState.add_admin)
    else:
        await groups_logger('Set admin role: ', user_id, message.text)
        await message.reply(str(message.chat.id) + sqlite_db.user_add(message.text))


async def commands_settings(message: types.Message, state: FSMContext):
    await message.reply(lang.message_panel_blacklist_commands + str(black_list))
    await message.reply(lang.message_panel_commands, reply_markup=kb_admin.panel_commands_switch)
    await state.set_state(AdminState.commands)


async def button_commands_add(message: types.Message, state: FSMContext):
    await message.reply(lang.message_panel_commands_send, reply_markup=kb_admin.admin_back)
    await state.set_state(AdminState.command_add)


async def button_commands_remove(message: types.Message, state: FSMContext):
    await message.reply(lang.message_panel_commands_send, reply_markup=kb_admin.admin_back)
    await state.set_state(AdminState.command_remove)


async def command_add(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    low = message.text.lower()
    if low in black_list:
        await message.reply(lang.message_panel_blacklist_is_exists)
        await groups_logger('Add command (is exists): ', user_id, message.text)
        await state.set_state(AdminState.command_add)
    else:
        black_list.append(low)
        await groups_logger('Add command: ', user_id, message.text)
        await message.reply(lang.message_panel_commands_add + lang.message_panel_commands_send)
        await state.set_state(AdminState.command_add)


async def command_remove(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    low = message.text.lower()
    if low in black_list:
        black_list.remove(low)
        await groups_logger('Remove command: ', user_id, message.text)
        await message.reply(lang.message_panel_commands_remove + lang.message_panel_commands_send)
        await state.set_state(AdminState.command_remove)
    else:
        await groups_logger('Remove command (not exists): ', user_id, message.text)
        await message.reply(lang.message_panel_blacklist_not_exists)
        await state.set_state(AdminState.command_remove)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(settings_panel, Text(startswith=lang.button_message_panel_admin_settings,
                                                     ignore_case=True))
    dp.register_message_handler(cancel_settings, Text(equals=lang.button_message_cancel, ignore_case=True),
                                state=AdminState.settings)
    dp.register_message_handler(back_to_state_settings, Text(equals=lang.button_message_back, ignore_case=True),
                                state=[AdminState.give, AdminState.commands])
    dp.register_message_handler(back_state_add, Text(equals=lang.button_message_back, ignore_case=True),
                                state=[AdminState.add_user, AdminState.add_admin])
    dp.register_message_handler(back_state_commands_switch, Text(equals=lang.button_message_back, ignore_case=True),
                                state=[AdminState.command_add, AdminState.command_remove])
    dp.register_message_handler(add_roles_switch, Text(startswith=lang.button_message_panel_add, ignore_case=True),
                                state=AdminState.settings)
    dp.register_message_handler(roles_add_user, Text(equals=lang.button_message_panel_add_user, ignore_case=True),
                                state=AdminState.give)
    dp.register_message_handler(roles_add_admin, Text(equals=lang.button_message_panel_add_admin, ignore_case=True),
                                state=AdminState.give)
    dp.register_message_handler(get_user_id, state=AdminState.add_user)
    dp.register_message_handler(get_admin_id, state=AdminState.add_admin)
    dp.register_message_handler(commands_settings, Text(equals=lang.button_message_panel_commands, ignore_case=True),
                                state=AdminState.settings)
    dp.register_message_handler(button_commands_add, Text(equals=lang.button_message_panel_commands_add, ignore_case=True),
                                state=AdminState.commands)
    dp.register_message_handler(button_commands_remove, Text(equals=lang.button_message_panel_commands_remove, ignore_case=True),
                                state=AdminState.commands)
    dp.register_message_handler(command_add, state=AdminState.command_add)
    dp.register_message_handler(command_remove, state=AdminState.command_remove)
