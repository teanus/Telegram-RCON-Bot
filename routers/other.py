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
from render_template import load_valid_commands

other_router = Router()

json_file_path = os.path.join("template", "commands", "other.json")
valid_commands = load_valid_commands(json_file_path)


async def id_cmd(message: types.Message) -> None:
    chat_id = message.chat.id
    await message.reply(f"Ваш id: {chat_id}")


async def info_cmd(message: types.Message) -> None:
    await message.reply(
        "Бот написан на полностью бесплатной основе\nРазработчик: t.me/teanus"
    )


async def support_cmd(message: types.Message) -> None:
    await message.reply("Канал поддержки: site.ru")


async def register_routers() -> None:
    other_router.message.register(id_cmd, TextInFilter(valid_commands["id"]))
    other_router.message.register(info_cmd, TextInFilter(valid_commands["info"]))
    other_router.message.register(support_cmd, TextInFilter(valid_commands["support"]))
