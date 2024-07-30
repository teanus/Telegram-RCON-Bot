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

import os

from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from custom_filters import TextInFilter
from keyboards import kb_admin
from logger.group_logger import groups_logger
from logger.log import logger
from provider import db
from render_template import load_valid_commands
from tools import get_commands_table_formatted

json_file_path = os.path.join("template", "commands", "admin.json")
valid_commands = load_valid_commands(json_file_path)


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


admin_router = Router()


async def settings_panel(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    if await db.check_admin_user(chat_id):
        await message.answer(
            "Вы вошли в админ панель! Выберите действие",
            reply_markup=kb_admin.admin_panel_menu,
        )
        logger.info(f"Вход в админ панель выполнен пользователем с id: {chat_id}")
        await state.set_state(AdminState.settings)


async def cancel_settings(message: types.Message, state: FSMContext) -> None:
    await message.answer("Вы вышли из админ панели", reply_markup=kb_admin.main_menu)
    await state.clear()


async def back_to_state(
    message: types.Message, state: FSMContext, state_to_set: State
) -> None:
    await message.answer(
        "Возвращаемся назад!", reply_markup=kb_admin.roles_switch_panel
    )
    await state.set_state(state_to_set)


async def back_state_add(message: types.Message, state: FSMContext) -> None:
    await back_to_state(message, state, AdminState.give)


async def back_state_remove(message: types.Message, state: FSMContext) -> None:
    await back_to_state(message, state, AdminState.remove)


async def back_to_state_settings(message: types.Message, state: FSMContext) -> None:
    await message.answer("Возвращаемся назад!", reply_markup=kb_admin.admin_panel_menu)
    await state.set_state(AdminState.settings)


async def back_to_state_on_markup(
    message: types.Message,
    state: FSMContext,
    reply_text: str,
    markup,
    state_to_set: State,
) -> None:
    await message.answer(reply_text, reply_markup=markup)
    await state.set_state(state_to_set)


async def back_state_commands_switch(message: types.Message, state: FSMContext) -> None:
    await back_to_state_on_markup(
        message,
        state,
        "Возвращаемся назад!",
        kb_admin.panel_commands_switch,
        AdminState.commands,
    )


async def back_state_remove_roles_switcher(
    message: types.Message, state: FSMContext
) -> None:
    await back_to_state_on_markup(
        message,
        state,
        "Возвращаемся назад!",
        kb_admin.admin_panel_menu,
        AdminState.settings,
    )


async def back_state_roles(message: types.Message, state: FSMContext) -> None:
    await back_to_state_on_markup(
        message,
        state,
        "Возвращаемся назад!",
        kb_admin.roles_panel,
        AdminState.roles_switch,
    )


async def roles_switch(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Выберите действие или вернитесь назад.", reply_markup=kb_admin.roles_panel
    )
    await state.set_state(AdminState.roles_switch)


async def give_roles(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Выберите какую роль нужно выдать", reply_markup=kb_admin.roles_switch_panel
    )
    await state.set_state(AdminState.give)


async def remove_role(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Выберите какую роль нужно снять", reply_markup=kb_admin.roles_switch_panel
    )
    await state.set_state(AdminState.remove)


async def remove_role_user(message: types.Message, state: FSMContext) -> None:
    await message.answer("Введите id для снятия прав", reply_markup=kb_admin.admin_back)
    await state.set_state(AdminState.remove_user)


async def remove_role_admin(message: types.Message, state: FSMContext) -> None:
    await message.answer("Введите id для снятия роли", reply_markup=kb_admin.admin_back)
    await state.set_state(AdminState.remove_admin)


async def roles_add_user(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Введите id для выдачи прав пользователя: ", reply_markup=kb_admin.admin_back
    )
    await state.set_state(AdminState.add_user)


async def roles_add_admin(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Введите id для выдачи прав super-админа: ", reply_markup=kb_admin.admin_back
    )
    await state.set_state(AdminState.add_admin)


async def get_add_user_id(message: types.Message) -> None:
    chat_id = message.chat.id
    text_id = message.text
    if not text_id.isdigit():
        await message.reply(
            "Это не является ID, id должен содержать ТОЛЬКО цифры и ничего другого. Пример: 78715102429"
        )
    elif await db.user_exists(text_id):
        await message.answer(
            "Пользователь с таким id уже есть в списке. Введите другой id или нажмите 'назад'"
        )
    else:
        await groups_logger("Выдача роли обычного игрока: ", chat_id, message.text)
        await db.add_user(text_id)
        await message.answer(f"Роль 'обычная' выдана пользователю с id {message.text}")


async def get_add_admin_id(message: types.Message) -> None:
    chat_id = message.chat.id
    text_id = message.text
    if not text_id.isdigit():
        await message.reply(
            "Это не является ID, id должен содержать ТОЛЬКО цифры и ничего другого. Пример: 78715102429"
        )
    elif await db.check_admin_user(message.text):
        await message.answer(
            "Этот id уже имеет роль администратора. Введите другой id или нажмите 'назад'"
        )
    else:
        await groups_logger("Выдача роли администратора: ", chat_id, message.text)
        await db.add_admin(message.text)
        await message.answer(
            f"Вы выдали администратора пользователю с id {message.text}"
        )


async def get_remove_user_id(message: types.Message) -> None:
    chat_id = message.chat.id
    if not await db.user_exists(message.text):
        await message.answer(
            "Пользователь с таким id нет в списке. Введите другой id или нажмите 'назад'"
        )
    else:
        await groups_logger("Снятие роли пользователя: ", chat_id, message.text)
        logger.info(f"{chat_id} - снял роль пользователя с {message.text}")
        await message.answer(await db.user_remove(message.text))


async def get_remove_admin_id(message: types.Message) -> None:
    chat_id = message.chat.id
    if not await db.check_admin_user(message.text):
        await message.answer(
            "В бд нет администратора с таким id. Введите другой id или нажмите 'назад'"
        )
    else:
        logger.info(f"{chat_id} - снял роль администратора с {message.text}")
        await groups_logger("Снятие роли администратора: ", chat_id, message.text)
        await message.answer(await db.admin_remove(message.text))


async def commands_settings(message: types.Message, state: FSMContext) -> None:
    commands = await db.commands_all()
    table = await get_commands_table_formatted(commands)
    await message.answer("Список заблокированных команд на данный момент: ")
    await message.answer(f"```commands_list {table}```", parse_mode="Markdown")
    await message.answer(
        "Выберите, что нужно сделать. Добавить или удалить команды из списка. Либо вернитесь назад",
        reply_markup=kb_admin.panel_commands_switch,
    )
    await state.set_state(AdminState.commands)


async def button_commands_add(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Пришлите команду или вернитесь назад", reply_markup=kb_admin.admin_back
    )
    await state.set_state(AdminState.command_add)


async def button_commands_remove(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Пришлите команду или вернитесь назад", reply_markup=kb_admin.admin_back
    )
    await state.set_state(AdminState.command_remove)


async def command_add(message: types.Message) -> None:
    chat_id = message.chat.id
    low = message.text.lower()

    exists = await db.command_exists(low)

    if exists:
        await message.answer(
            "Эта команда была заблокирована ранее. Введите другую или вернитесь назад"
        )
        logger.info(
            f"{chat_id} - попытался заблокировать команду {low}, но она уже в списках"
        )
        await groups_logger("Попытался заблокировать команду: ", chat_id, message.text)
    else:
        await db.add_black_list(low)
        logger.info(f"{chat_id} - добавил команду в черный список. Команда: {low}")
        await groups_logger("Добавил команду в черный список", chat_id, message.text)
        await message.answer(
            "Команда была заблокирована. Пришлите еще одну команду, или вернитесь назад"
        )


async def command_remove(message: types.Message) -> None:
    chat_id = message.chat.id
    low = message.text.lower()
    exists = await db.command_exists(low)

    if exists:
        await db.remove_black_list(low)
        log_message = f"{chat_id} - разблокировал команду {low}"
        success_message = "Команда разблокирована! Пришлите еще команду для разблокировки, или вернитесь назад"
    else:
        log_message = (
            f"{chat_id} - попытался разблокировать команду {low}, но она не в списках"
        )
        success_message = (
            "Данная команда не находится в списке заблокированных. Пришлите другую команду, "
            "или вернитесь назад "
        )

    await groups_logger("Удаление команды: ", chat_id, message.text)
    logger.info(log_message)
    await message.answer(success_message)


async def register_routers() -> None:
    admin_router.message.register(
        settings_panel, TextInFilter(valid_commands["settings"])
    )
    admin_router.message.register(
        cancel_settings,
        TextInFilter(valid_commands["cancel"]),
        StateFilter(AdminState.settings),
    )


admin_router.message.register(
    roles_switch, TextInFilter(valid_commands["role"]), StateFilter(AdminState.settings)
)
admin_router.message.register(
    commands_settings,
    TextInFilter(valid_commands["commands"]),
    StateFilter(AdminState.settings),
)

admin_router.message.register(
    back_to_state_settings,
    TextInFilter(valid_commands["back"]),
    StateFilter(AdminState.commands),
)

admin_router.message.register(
    back_state_add,
    TextInFilter(["⏹ назад"]),
    StateFilter(AdminState.add_user, AdminState.add_admin),
)

admin_router.message.register(get_add_user_id, StateFilter(AdminState.add_user))
admin_router.message.register(get_add_admin_id, StateFilter(AdminState.add_admin))

admin_router.message.register(
    back_state_remove_roles_switcher,
    TextInFilter(valid_commands["back"]),
    StateFilter(AdminState.roles_switch),
)
admin_router.message.register(
    back_state_roles,
    TextInFilter(valid_commands["back"]),
    StateFilter(AdminState.remove, AdminState.give),
)
admin_router.message.register(
    back_state_remove,
    TextInFilter(valid_commands["back"]),
    StateFilter(AdminState.remove_user, AdminState.remove_admin),
)
admin_router.message.register(
    back_state_commands_switch,
    TextInFilter(valid_commands["back"]),
    StateFilter(AdminState.command_add, AdminState.command_remove),
)

admin_router.message.register(
    give_roles,
    TextInFilter(valid_commands["give_role"]),
    StateFilter(AdminState.roles_switch),
)
admin_router.message.register(
    remove_role,
    TextInFilter(valid_commands["remove_role"]),
    StateFilter(AdminState.roles_switch),
)
admin_router.message.register(
    roles_add_user,
    TextInFilter(valid_commands["role_normal"]),
    StateFilter(AdminState.give),
)
admin_router.message.register(
    roles_add_admin,
    TextInFilter(valid_commands["role_admin"]),
    StateFilter(AdminState.give),
)
admin_router.message.register(
    remove_role_user,
    TextInFilter(valid_commands["role_normal"]),
    StateFilter(AdminState.remove),
)
admin_router.message.register(
    remove_role_admin,
    TextInFilter(valid_commands["role_admin"]),
    StateFilter(AdminState.remove),
)

admin_router.message.register(get_remove_user_id, StateFilter(AdminState.remove_user))
admin_router.message.register(get_remove_admin_id, StateFilter(AdminState.remove_admin))

admin_router.message.register(
    button_commands_add,
    TextInFilter(valid_commands["add_command"]),
    StateFilter(AdminState.commands),
)
admin_router.message.register(
    button_commands_remove,
    TextInFilter(valid_commands["remove_command"]),
    StateFilter(AdminState.commands),
)
admin_router.message.register(command_add, StateFilter(AdminState.command_add))
admin_router.message.register(command_remove, StateFilter(AdminState.command_remove))
