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


from aiogram.exceptions import TelegramAPIError

from create_bot import bot
from provider import db
from resources import config


async def groups_logger(prefix: str, user_id: int, message: str) -> None:
    if config.telegram().get("on_logger_group"):
        user_type = "Админ" if await db.check_admin_user(user_id) else "Пользователь"
        log_message = f"{prefix} {user_type} с ID {user_id} - ввел команду: {message}"
        try:
            await bot.send_message(config.telegram().get("logger_chat_id"), log_message)
        except TelegramAPIError as e:
            print(f"Не удалось отправить сообщение журнала: {e}")
