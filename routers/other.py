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

from aiogram import F, Router, types

from custom_filters import TextInFilter
from render_template import load_valid_commands, render_template_jinja

other_router = Router()

json_file_path = os.path.join("template", "commands", "other.json")
valid_commands = load_valid_commands(json_file_path)


async def id_command(message: types.Message) -> None:
    chat_id = message.chat.id
    context = {"chat_id": chat_id}
    await message.reply(render_template_jinja("other/id_command.jinja2", **context))


async def info_command(message: types.Message) -> None:
    await message.answer("Разработчик: t.me/teanus\nСайт: https://teanus.ru")


async def support_command(message: types.Message) -> None:
    await message.reply(render_template_jinja("other/support_command.jinja2"))


async def register_routers() -> None:
    other_router.message.register(id_command, TextInFilter(valid_commands["id"]))
    other_router.message.register(info_command, TextInFilter(valid_commands["info"]))
    other_router.message.register(
        support_command, TextInFilter(valid_commands["support"])
    )
