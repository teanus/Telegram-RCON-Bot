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
from render_template import render_template_jinja
from resources import config


async def groups_logger(prefix: str, user_id: int, message: str) -> None:
    """
    Логирует сообщения в группы, если включен лагер групп.

    :param prefix: Префикс сообщения.
    :param user_id: ID пользователя.
    :param message: Сообщение для логирования.
    :return: None
    """
    if config.telegram().get("on_logger_group"):
        is_admin = await db.check_admin(user_id)
        context = {
            "prefix": prefix,
            "is_admin": is_admin,
            "user_id": user_id,
            "message": message,
        }
        log_message = render_template_jinja(
            "messages.jinja2", "template/group_logger", **context
        )
        try:
            await bot.send_message(config.telegram().get("logger_chat_id"), log_message)
        except TelegramAPIError as error:
            print(f"The log message could not be sent: {error}")
