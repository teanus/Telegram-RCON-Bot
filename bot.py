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


from aiogram.utils import executor

from add_super_admin import console_add_super_admin
from create_bot import dp
from handlers import admin, client, common, other

from logger.log import logger


async def on_startup(_) -> None:
    print("Бот начал работу!")
    logger.info("Бот запущен!")
    print(await console_add_super_admin())


async def on_shutdown(_) -> None:
    print("Бот выключен")
    logger.info("Бот выключен")


admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)
common.register_handlers_common(dp)

if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
