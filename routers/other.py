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


from aiogram import Router, types
from aiogram import F
from aiogram.filters import Command
from custom_filters import TextInFilter

other_router = Router()


async def id_cmd(message: types.Message) -> None:
    chat_id = message.chat.id
    await message.reply(f"Ваш id: {chat_id}")


async def info_cmd(message: types.Message) -> None:
    await message.reply(
        "Бот написан на полностью бесплатной основе\nРазработчик: t.me/teanus"
    )


async def support_cmd(message: types.Message) -> None:
    await message.reply("Канал поддержки: site.ru")


def register_routers() -> None:
    other_router.message.register(id_cmd, TextInFilter(["/id", "🆔 айди"]))
    other_router.message.register(info_cmd(), TextInFilter(["/info", "🆘 инфо"]))
    other_router.message.register(support_cmd, TextInFilter(["/support","🆘 поддержка"]))
