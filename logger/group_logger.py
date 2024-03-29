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


from create_bot import bot
from provider import db
from resources import config


async def groups_logger(prefix: str, user_id: str, message: str) -> None:
    if not config.telegram()["on_logger_group"]:
        return
    else:
        if await db.check_admin_user(user_id):
            message = f"{prefix} Админ с ID {user_id} - ввел команду: {message}"
            await bot.send_message(config.telegram()["logger_chat_id"], message)
        else:
            message = f"{prefix} Пользователь с ID {user_id} - ввел команду: {message}"
            await bot.send_message(config.telegram()["logger_chat_id"], message)
