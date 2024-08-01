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
from render_template import load_valid_commands, render_template_jinja
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
    if await db.check_admin(chat_id):
        context = {"chat_id": chat_id}

        message_text = render_template_jinja(
            "admin/settings_panel/message.jinja2", **context
        )
        await message.answer(message_text, reply_markup=kb_admin.admin_panel_menu)

        log_text = render_template_jinja(
            "admin/settings_panel/logger.jinja2", **context
        )
        logger.info(log_text)

        await state.set_state(AdminState.settings)


async def cancel_settings(message: types.Message, state: FSMContext) -> None:
    context = {}
    message_text = render_template_jinja("admin/cancel_settings.jinja2", **context)
    await message.answer(message_text, reply_markup=kb_admin.main_menu)
    await state.clear()


async def back_to_state(
    message: types.Message, state: FSMContext, state_to_set: State
) -> None:
    context = {}

    message_text = render_template_jinja("admin/back_to_state.jinja2", **context)
    await message.answer(message_text, reply_markup=kb_admin.roles_switch_panel)
    await state.set_state(state_to_set)


async def back_state_add(message: types.Message, state: FSMContext) -> None:
    await back_to_state(message, state, AdminState.give)


async def back_state_remove(message: types.Message, state: FSMContext) -> None:
    await back_to_state(message, state, AdminState.remove)


async def back_to_state_settings(message: types.Message, state: FSMContext) -> None:
    context = {}

    message_text = render_template_jinja(
        "admin/back_to_state_settings.jinja2", **context
    )
    await message.answer(message_text, reply_markup=kb_admin.admin_panel_menu)
    await state.set_state(AdminState.settings)


async def back_to_state_on_markup(
    message: types.Message,
    state: FSMContext,
    template_name: str,
    markup: types.ReplyKeyboardMarkup,
    state_to_set: State,
    **context,
) -> None:
    message_text = render_template_jinja(template_name, **context)
    await message.answer(message_text, reply_markup=markup)
    await state.set_state(state_to_set)


async def back_state_commands_switch(message: types.Message, state: FSMContext) -> None:
    await back_to_state_on_markup(
        message,
        state,
        "admin/back_state_commands_switch.jinja2",
        kb_admin.panel_commands_switch,
        AdminState.commands,
    )


async def back_state_remove_roles_switcher(
    message: types.Message, state: FSMContext
) -> None:
    await back_to_state_on_markup(
        message,
        state,
        "admin/back_state_remove_roles_switcher.jinja2",
        kb_admin.admin_panel_menu,
        AdminState.settings,
    )


async def back_state_roles(message: types.Message, state: FSMContext) -> None:
    await back_to_state_on_markup(
        message,
        state,
        "admin/back_state_remove_roles_switcher.jinja2",
        kb_admin.roles_panel,
        AdminState.roles_switch,
    )


async def roles_switch(message: types.Message, state: FSMContext) -> None:
    context = {}

    message_text = render_template_jinja("admin/roles_switch.jinja2", **context)
    await message.answer(message_text, reply_markup=kb_admin.roles_panel)
    await state.set_state(AdminState.roles_switch)


async def give_roles(message: types.Message, state: FSMContext) -> None:
    context = {}

    message_text = render_template_jinja("admin/roles_switch.jinja2", **context)
    await message.answer(message_text, reply_markup=kb_admin.roles_switch_panel)
    await state.set_state(AdminState.give)


async def remove_role(message: types.Message, state: FSMContext) -> None:
    context = {}

    message_text = render_template_jinja("admin/remove_role.jinja2", **context)
    await message.answer(message_text, reply_markup=kb_admin.roles_switch_panel)
    await state.set_state(AdminState.remove)


async def remove_role_user(message: types.Message, state: FSMContext) -> None:
    context = {}

    message_text = render_template_jinja("admin/remove_role_user.jinja2", **context)
    await message.answer(message_text, reply_markup=kb_admin.admin_back)
    await state.set_state(AdminState.remove_user)


async def remove_role_admin(message: types.Message, state: FSMContext) -> None:
    context = {}

    message_text = render_template_jinja("admin/remove_role_admin.jinja2", **context)
    await message.answer(message_text, reply_markup=kb_admin.admin_back)
    await state.set_state(AdminState.remove_admin)


async def roles_add_user(message: types.Message, state: FSMContext) -> None:
    context = {}

    message_text = render_template_jinja("admin/roles_add_user.jinja2", **context)
    await message.answer(message_text, reply_markup=kb_admin.admin_back)
    await state.set_state(AdminState.add_user)


async def roles_add_admin(message: types.Message, state: FSMContext) -> None:
    context = {}

    message_text = render_template_jinja("admin/roles_add_user.jinja2", **context)
    await message.answer(message_text, reply_markup=kb_admin.admin_back)
    await state.set_state(AdminState.add_admin)


async def get_add_user_id(message: types.Message) -> None:
    chat_id = message.chat.id
    text_id = message.text

    if not text_id.isdigit():
        context = {}
        message_text = render_template_jinja(
            "admin/get_add_user_id/invalid_id.jinja2", **context
        )
        await message.reply(message_text)
    elif await db.user_exists(text_id):
        context = {}
        message_text = render_template_jinja(
            "admin/get_add_user_id/user_exists.jinja2", **context
        )
        await message.answer(message_text)
    else:
        context = {"chat_id": chat_id, "message.text": message.text, "text_id": text_id}
        await groups_logger(
            "admin/get_add_user_id/groups_logger.jinja2", chat_id, message.text
        )
        await db.add_user(text_id)
        message_text = render_template_jinja(
            "admin/get_add_user_id/user_added.jinja2", **context
        )
        await message.answer(message_text)


async def get_add_admin_id(message: types.Message) -> None:
    chat_id = message.chat.id
    text_id = message.text
    if not text_id.isdigit():
        context = {}
        message_text = render_template_jinja(
            "admin/get_add_admin_id/invalid_id.jinja2", **context
        )
        await message.reply(message_text)
    elif await db.check_admin(message.text):
        context = {}
        message_text = render_template_jinja(
            "admin/get_add_admin_id/admin_exists.jinja2", **context
        )
        await message.answer(message_text)
    else:
        context = {"chat_id": chat_id, "message.text": message.text, "text_id": text_id}
        await groups_logger(
            "admin/get_add_admin_id/groups_logger.jinja2", chat_id, message.text
        )
        await db.add_user(text_id)
        message_text = render_template_jinja(
            "admin/get_add_admin_id/admin_added.jinja2", **context
        )
        await message.answer(message_text)


async def get_remove_user_id(message: types.Message) -> None:
    chat_id = message.chat.id
    if not await db.user_exists(message.text):
        context = {}
        message_text = render_template_jinja(
            "admin/get_remove_user_id/not_user_exists.jinja2", **context
        )
        await message.answer(message_text)
    else:
        context = {"chat_id": chat_id, "message_text": message.text}
        await groups_logger(
            render_template_jinja("admin/get_remove_user_id/groups_logger.jinja2"),
            chat_id,
            message.text,
        )
        logger.info(
            render_template_jinja("admin/get_remove_user_id/logger.jinja2", **context)
        )
        await message.answer(await db.user_remove(message.text))


async def get_remove_admin_id(message: types.Message) -> None:
    chat_id = message.chat.id
    if not await db.check_admin(message.text):
        context = {}
        message_text = render_template_jinja(
            "admin/get_remove_admin_id/not_admin_exists.jinja2", **context
        )
        await message.answer(message_text)
    else:
        context = {"chat_id": chat_id, "message_text": message.text}
        await groups_logger(
            render_template_jinja("admin/get_remove_admin_id/groups_logger.jinja2"),
            chat_id,
            message.text,
        )
        logger.info(
            render_template_jinja("admin/get_remove_admin_id/logger.jinja2", **context)
        )
        await message.answer(await db.admin_remove(message.text))


async def commands_settings(message: types.Message, state: FSMContext) -> None:
    commands = await db.commands_all()
    table = await get_commands_table_formatted(commands)
    await message.answer(
        render_template_jinja("admin/commands_settings/list_commands.jinja2")
    )
    await message.answer(f"```commands_list {table}```", parse_mode="Markdown")
    await message.answer(
        render_template_jinja("admin/commands_settings/messages.jinja2"),
        reply_markup=kb_admin.panel_commands_switch,
    )
    await state.set_state(AdminState.commands)


async def button_commands_add(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        render_template_jinja("admin/button_commands_add.jinja2"),
        reply_markup=kb_admin.admin_back,
    )
    await state.set_state(AdminState.command_add)


async def button_commands_remove(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        render_template_jinja("admin/button_commands_remove.jinja2"),
        reply_markup=kb_admin.admin_back,
    )
    await state.set_state(AdminState.command_remove)


async def command_add(message: types.Message) -> None:
    chat_id = message.chat.id
    low = message.text.lower()
    exists = await db.command_exists(low)

    if exists:
        context = {"chat_id": chat_id, "low": low}
        await message.answer(
            render_template_jinja("admin/command_add/command_exists_banned.jinja2")
        )
        logger.info(
            render_template_jinja("admin/command_add/logger_command_exists.jinja2")
        )
        await groups_logger(
            render_template_jinja(
                "admin/command_add/group_logger_command_exists.jinja2"
            ),
            chat_id,
            message.text,
        )
    else:
        await db.add_black_list(low)
        logger.info(
            render_template_jinja("admin/command_add/done_logger_banned_command.jinja2")
        )
        await groups_logger(
            render_template_jinja(
                "admin/command_add/done_group_logger_banned_command.jinja2"
            ),
            chat_id,
            message.text,
        )
        await message.answer(
            render_template_jinja(
                "admin/command_add/done_message_banned_command.jinja2"
            )
        )


async def command_remove(message: types.Message) -> None:
    chat_id = message.chat.id
    low = message.text.lower()
    exists = await db.command_exists(low)
    context = {"chat_id": chat_id, "low": low}

    if exists:
        await db.remove_black_list(low)
        log_message = render_template_jinja(
            "admin/command_remove/done_logger.jinja2", **context
        )
        success_message = render_template_jinja(
            "admin/command_remove/done_command_exists.jinja2"
        )
    else:
        log_message = render_template_jinja(
            "admin/command_remove/not_banned_logger.jinja2", **context
        )
        success_message = render_template_jinja(
            "admin/command_remove/not_banned_command.jinja2"
        )

    await groups_logger(
        render_template_jinja("admin/command_remove/groups_logger.jinja2"),
        chat_id,
        message.text,
    )
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
