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


from resources import config
from create_bot import bot
from provider import db


async def groups_logger(prefix, user_id, message):
    if not config.telegram()["on_logger_group"]:
        return
    else:
        if await db.check_admin_user(user_id):
            message = f"{prefix} Админ с ID {user_id} - ввел команду: {message}"
            await bot.send_message(config.telegram()["logger_chat_id"], message)
        else:
            message = f"{prefix} Пользователь с ID {user_id} - ввел команду: {message}"
            await bot.send_message(config.telegram()["logger_chat_id"], message)
