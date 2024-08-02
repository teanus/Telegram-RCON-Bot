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
from keyboards import get_main_menu, kb_client
from logger.group_logger import groups_logger
from logger.log import logger
from minecraft import rcon
from provider import db
from render_template import load_valid_commands, render_template_jinja

json_file_path = os.path.join("template", "commands", "client.json")
valid_commands = load_valid_commands(json_file_path)


class FsmClient(StatesGroup):
    rcon = State()


client_router = Router()


async def rcon_cmd(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду RCON от пользователя, проверяет права доступа и отвечает на сообщение.

    :param message: Сообщение от пользователя.
    :type message: types.Message
    :param state: Состояние конечного автомата.
    :type state: FSMContext
    :return: None
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    is_admin = await db.check_admin(chat_id)
    context = {"user_id": user_id, "is_admin": is_admin}

    if is_admin or await db.user_exists(chat_id):
        logger.info(render_template_jinja("client/rcon_cmd/logger.jinja2", **context))
        await message.reply(
            render_template_jinja("client/rcon_cmd/reply.jinja2"),
            reply_markup=kb_client.rcon_cancel,
        )
        await state.set_state(FsmClient.rcon)
    else:
        await message.reply(render_template_jinja("client/rcon_cmd/no_access.jinja2"))


async def cancel_state_rcon(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает отмену состояния RCON и возвращает в главное меню.

    :param message: Сообщение от пользователя.
    :type message: types.Message
    :param state: Состояние конечного автомата.
    :type state: FSMContext
    :return
    """
    chat_id = message.chat.id
    main_menu = await get_main_menu(chat_id)
    is_admin = await db.check_admin(chat_id)
    context = {"is_admin": is_admin}

    text = render_template_jinja("client/cancel_state_rcon/messages.jinja2", **context)
    await message.reply(text, reply_markup=main_menu)
    await state.clear()


async def get_command(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду RCON от пользователя и отправляет результат выполнения команды.

    :param message: Сообщение от пользователя.
    :type message: types.Message
    :param state: Состояние конечного автомата.
    :type state: FSMContext
    :return: None
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    low = message.text.lower()
    command = low.split(" ", 1)
    is_admin = await db.check_admin(chat_id)
    context = {
        "user_id": user_id,
        "command": low,
        "is_admin": is_admin,
        "blocked_command": not is_admin and await db.command_exists(command[0]),
    }

    if context["blocked_command"]:
        logger.info(
            render_template_jinja("client/get_command/logger.jinja2", **context)
        )
        await groups_logger("RCON: ", user_id, message.text)
        await message.reply(
            render_template_jinja("client/get_command/messages.jinja2", **context)
        )
    else:
        result = rcon.command_execute(low)
        context.update({"result": result})
        logger.info(
            render_template_jinja("client/get_command/logger.jinja2", **context)
        )
        await groups_logger("RCON: ", user_id, message.text)
        await message.reply(
            render_template_jinja("client/get_command/messages.jinja2", **context)
        )
        await message.answer(
            render_template_jinja("client/get_command/continue.jinja2")
        )
        await state.set_state(FsmClient.rcon)


async def register_routers() -> None:
    """
    Регистрация routers для обработки сообщений client.

    :return: None
    """
    client_router.message.register(rcon_cmd, TextInFilter(valid_commands["rcon"]))
    client_router.message.register(
        cancel_state_rcon,
        TextInFilter(valid_commands["cancel"]),
        StateFilter(FsmClient.rcon),
    )
    client_router.message.register(get_command, StateFilter(FsmClient.rcon))
