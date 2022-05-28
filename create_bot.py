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


from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Config import TELEGRAM_TOKEN


storage = MemoryStorage()

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)
