#          Free версия бота проекта LostWeyn
#              Telegram: t.me/lostweyn_project
#
#          Контакты разработчика:
#              VK: vk.com/dimawinchester
#              Telegram: t.me/teanus
#              Github: github.com/teanus
#              24serv: talk.24serv.pro/u/teanus
#
#
#     ██╗      ██████╗ ███████╗████████╗██╗    ██╗███████╗██╗   ██╗███╗   ██╗
#     ██║     ██╔═══██╗██╔════╝╚══██╔══╝██║    ██║██╔════╝╚██╗ ██╔╝████╗  ██║
#     ██║     ██║   ██║███████╗   ██║   ██║ █╗ ██║█████╗   ╚████╔╝ ██╔██╗ ██║
#     ██║     ██║   ██║╚════██║   ██║   ██║███╗██║██╔══╝    ╚██╔╝  ██║╚██╗██║
#     ███████╗╚██████╔╝███████║   ██║   ╚███╔███╔╝███████╗   ██║   ██║ ╚████║
#     ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚══╝╚══╝ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝


from create_bot import dp
from aiogram.utils import executor
from handlers import client, admin, other
from add_super_admin import console_add_super_admin


async def on_startup(_):
    print('Бот начал работу!')
    print(console_add_super_admin())


async def on_shutdown(_):
    print('Бот выключен')

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
