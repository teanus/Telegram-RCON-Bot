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


import asyncio

from add_super_admin import console_add_super_admin
from create_bot import bot, dp
from logger.log import logger
from routers.admin import admin_router
from routers.admin import register_routers as register_admin_handlers
from routers.client import client_router
from routers.client import register_routers as register_client_handlers
from routers.common import common_router
from routers.common import register_routers as register_common_handlers
from routers.other import other_router
from routers.other import register_routers as register_other_handlers


async def on_startup() -> None:
    await console_add_super_admin()
    print("Бот начал работу!")
    logger.info("Бот запущен!")


async def on_shutdown() -> None:
    print("Бот выключен")
    logger.info("Бот выключен")


async def main():
    dp.startup.register(on_startup)

    dp.include_router(other_router)
    dp.include_router(client_router)
    dp.include_router(admin_router)
    dp.include_router(common_router)
    # Регистрация обработчиков для каждого роутера
    await register_other_handlers()
    await register_client_handlers()
    await register_admin_handlers()
    await register_common_handlers()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
