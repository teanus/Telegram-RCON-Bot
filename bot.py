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


from create_bot import dp
from aiogram.utils import executor
from handlers import client, admin, other, common
from add_super_admin import console_add_super_admin


async def on_startup(_):
    print("Бот начал работу!")
    print(await console_add_super_admin())


async def on_shutdown(_):
    print("Бот выключен")


admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)
common.register_handlers_common(dp)

if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
