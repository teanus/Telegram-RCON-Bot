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
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards import kb_admin
from provider import db
from logger.group_logger import groups_logger


class AdminState(StatesGroup):
    settings = State()
    commands = State()
    command_add = State()
    command_remove = State()
    roles_switch = State()
    give = State()
    remove = State()
    remove_user = State()
    remove_admin = State()
    add_user = State()
    add_admin = State()


async def settings_panel(message: types.Message):
    chat_id = message.from_user.id
    if await db.check_admin_user(chat_id):
        await message.reply(
            "Вы вошли в админ панель! Выберите действие",
            reply_markup=kb_admin.admin_panel_menu,
        )
        await AdminState.settings.set()


async def cancel_settings(message: types.Message, state: FSMContext):
    # выходит из админ панели
    await message.reply("Вы вышли из админ панели", reply_markup=kb_admin.main_menu)
    await state.finish()


async def back_to_state_settings(message: types.Message, state: FSMContext):
    # выходит из панели выбора действия над командами
    await message.reply("Возвращаемся назад!)", reply_markup=kb_admin.admin_panel_menu)
    await state.set_state(AdminState.settings)


async def back_state_add(message: types.Message, state: FSMContext):
    # выходит из выдачи ролей
    await message.reply(
        "Возвращаемся назад!)", reply_markup=kb_admin.roles_switch_panel
    )
    await state.set_state(AdminState.give)


async def back_state_remove(message: types.Message, state: FSMContext):
    # выходит из удаления роли
    await message.reply(
        "Возвращаемся назад!)", reply_markup=kb_admin.roles_switch_panel
    )
    await state.set_state(AdminState.remove)


async def back_state_commands_switch(message: types.Message, state: FSMContext):
    await message.reply(
        "Возвращаемся назад!)", reply_markup=kb_admin.panel_commands_switch
    )
    await state.set_state(AdminState.commands)


async def back_state_remove_roles_switcher(message: types.Message, state: FSMContext):
    # выходит из панели роли
    await message.reply("Возвращаемся назад!)", reply_markup=kb_admin.admin_panel_menu)
    await state.set_state(AdminState.settings)


async def back_state_roles(message: types.Message, state: FSMContext):
    # назад к панели ролей
    await message.reply("Возвращаемся назад!)", reply_markup=kb_admin.roles_panel)
    await state.set_state(AdminState.roles_switch)


async def back_state_remove_command(message: types.Message, state: FSMContext):
    # назад к панели действия над командами
    await message.reply(
        "Возвращаемся назад!)", reply_markup=kb_admin.panel_commands_switch
    )
    await state.set_state(AdminState.commands)


async def roles_switch(message: types.message):
    await message.reply(
        "Выберите действие или вернитесь назад. ", reply_markup=kb_admin.roles_panel
    )
    await AdminState.roles_switch.set()


async def give_roles(message: types.message):
    await message.reply(
        "Выберите какую роль нужно выдать", reply_markup=kb_admin.roles_switch_panel
    )
    await AdminState.give.set()


async def remove_role(message: types.message):
    await message.reply(
        "Выберите какую роль нужно снять", reply_markup=kb_admin.roles_switch_panel
    )
    await AdminState.remove.set()


async def remove_role_user(message: types.message):
    await message.reply("Введите id для снятия прав", reply_markup=kb_admin.admin_back)
    await AdminState.remove_user.set()


async def remove_role_admin(message: types.message):
    await message.reply("Введите id для снятия роли", reply_markup=kb_admin.admin_back)
    await AdminState.remove_admin.set()


async def roles_add_user(message: types.Message):
    await message.reply(
        "Введите id для выдачи прав пользователя: ", reply_markup=kb_admin.admin_back
    )
    await AdminState.add_user.set()


async def roles_add_admin(message: types.Message):
    await message.reply(
        "Введите id для выдачи прав super-админа: ", reply_markup=kb_admin.admin_back
    )
    await AdminState.add_admin.set()


async def get_add_user_id(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await db.user_exists(message.text):
        await message.reply(
            f'Пользователь с таким  id уже есть в списке.\nВведите другой id или нажмите "назад"'
        )
        await state.set_state(AdminState.add_user)
    else:
        await groups_logger("Выдача роли обычного игрока: ", user_id, message.text)
        await message.reply(await db.add_user(message.text))


async def get_add_admin_id(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await db.check_admin_user(message.text):
        await message.reply(
            f'Этот id уже имеет роль администратора.\nВведите другой id или нажмите "назад"'
        )
        await state.set_state(AdminState.add_admin)
    else:
        await groups_logger("Выдача роли администратора: ", user_id, message.text)
        await message.reply(await db.add_user(message.text))


async def get_remove_user_id(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not await db.user_exists(message.text):
        await message.reply(
            f'Пользователь с таким  id нет в списке.\nВведите другой id или нажмите "назад"'
        )
        await state.set_state(AdminState.remove_user)
    else:
        await groups_logger("Снятие роли пользователя: ", user_id, message.text)
        await message.reply(await db.user_remove(message.text))


async def get_remove_admin_id(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not await db.check_admin_user(message.text):
        await message.reply(
            f'В бд нет администратора с таким id.\nВведите другой id или нажмите "назад"'
        )
        await state.set_state(AdminState.remove_admin)
    else:
        await groups_logger("Снятие роли администратора: ", user_id, message.text)
        await message.reply(await db.admin_remove(message.text))


async def commands_settings(message: types.Message, state: FSMContext):
    await message.reply(
        f"Список заблокированных команд на данный момент:\n {await db.commands_all()}"
    )
    await message.reply(
        "Выберите, что нужно сделать. Добавить или удалить команды из списка. Либо вернитесь назад",
        reply_markup=kb_admin.panel_commands_switch,
    )
    await state.set_state(AdminState.commands)


async def button_commands_add(message: types.Message, state: FSMContext):
    await message.reply(
        "Пришлите команду или вернитесь назад", reply_markup=kb_admin.admin_back
    )
    await state.set_state(AdminState.command_add)


async def button_commands_remove(message: types.Message, state: FSMContext):
    await message.reply(
        "Пришлите команду или вернитесь назад", reply_markup=kb_admin.admin_back
    )
    await state.set_state(AdminState.command_remove)


async def command_add(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    low = message.text.lower()
    if await db.command_exists(low):
        await message.reply(
            "Эта команда была заблокирована ранее. Введите другую или вернитесь назад"
        )
        await groups_logger("Попытался заблокировать команду: ", user_id, message.text)
        await state.set_state(AdminState.command_add)
    else:
        await db.add_black_list(low)
        await groups_logger("Добавил команду в черный список", user_id, message.text)
        await message.reply(
            "Команда была заблокирована.\nПришлите еще одну команду, или вернитесь назад"
        )
        await state.set_state(AdminState.command_add)


async def command_remove(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    low = message.text.lower()
    if await db.command_exists(low):
        await db.remove_black_list(low)
        await groups_logger("Удаление команды: ", user_id, message.text)
        await message.reply(
            "Команда разблокирована!\nПришлите еще команду для разблокировки, или вернитесь назад"
        )
        await state.set_state(AdminState.command_remove)
    else:
        await groups_logger(
            "Удаление команды (в списке отсутствует): ", user_id, message.text
        )
        await message.reply(
            "Данная команда не находится в списке заблокированных.\nПришлите другую команду, или вернитесь назад"
        )
        await state.set_state(AdminState.command_remove)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        settings_panel, Text(startswith="⚙управление", ignore_case=True)
    )
    dp.register_message_handler(
        cancel_settings,
        Text(equals="◀отмена", ignore_case=True),
        state=AdminState.settings,
    )
    dp.register_message_handler(
        back_to_state_settings,
        Text(equals="⏹назад", ignore_case=True),
        state=[AdminState.commands],
    )
    dp.register_message_handler(
        back_state_add,
        Text(equals="⏹назад", ignore_case=True),
        state=[AdminState.add_user, AdminState.add_admin],
    )
    dp.register_message_handler(
        back_state_remove_roles_switcher,
        Text(equals="⏹назад", ignore_case=True),
        state=AdminState.roles_switch,
    )
    dp.register_message_handler(
        back_state_roles,
        Text(equals="⏹назад", ignore_case=True),
        state=[AdminState.remove, AdminState.give],
    )
    dp.register_message_handler(
        back_state_remove,
        Text(equals="⏹назад", ignore_case=True),
        state=[AdminState.remove_user, AdminState.remove_admin],
    )
    dp.register_message_handler(
        back_state_remove_command,
        Text(equals="⏹назад", ignore_case=True),
        state=[AdminState.command_add, AdminState.command_remove],
    )
    dp.register_message_handler(
        roles_switch,
        Text(startswith="📝роли", ignore_case=True),
        state=AdminState.settings,
    )
    dp.register_message_handler(
        give_roles,
        Text(equals="📝выдать", ignore_case=True),
        state=AdminState.roles_switch,
    )
    dp.register_message_handler(
        remove_role,
        Text(equals="📝снять", ignore_case=True),
        state=AdminState.roles_switch,
    )
    dp.register_message_handler(
        remove_role_user,
        Text(equals="🪪обычный", ignore_case=True),
        state=AdminState.remove,
    )
    dp.register_message_handler(
        remove_role_admin,
        Text(equals="🪪админ", ignore_case=True),
        state=AdminState.remove,
    )
    dp.register_message_handler(get_remove_user_id, state=AdminState.remove_user)
    dp.register_message_handler(get_remove_admin_id, state=AdminState.remove_admin)
    dp.register_message_handler(
        roles_add_user, Text(equals="🪪обычный", ignore_case=True), state=AdminState.give
    )
    dp.register_message_handler(
        roles_add_admin, Text(equals="🪪админ", ignore_case=True), state=AdminState.give
    )
    dp.register_message_handler(get_add_user_id, state=AdminState.add_user)
    dp.register_message_handler(get_add_admin_id, state=AdminState.add_admin)
    dp.register_message_handler(get_remove_user_id, state=AdminState.remove_user)
    dp.register_message_handler(get_remove_admin_id, state=AdminState.remove_admin)
    dp.register_message_handler(
        commands_settings,
        Text(equals="📝команды", ignore_case=True),
        state=AdminState.settings,
    )
    dp.register_message_handler(
        button_commands_add,
        Text(equals="⛔добавить", ignore_case=True),
        state=AdminState.commands,
    )
    dp.register_message_handler(
        button_commands_remove,
        Text(equals="🗑удалить", ignore_case=True),
        state=AdminState.commands,
    )
    dp.register_message_handler(command_add, state=AdminState.command_add)
    dp.register_message_handler(command_remove, state=AdminState.command_remove)
