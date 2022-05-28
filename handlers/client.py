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


from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from locales import lang


async def id_cmd(message: types.Message):
    chat_id = message.chat.id
    await message.reply(lang.message_id + str(chat_id))


async def info_cmd(message: types.Message):
    await message.reply(lang.message_info)


async def support_cmd(message: types.Message):
    await message.reply(lang.message_support)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(id_cmd, Text(startswith=[lang.button_message_id, '/id'], ignore_case=True))
    dp.register_message_handler(info_cmd, Text(startswith=[lang.button_message_info, '/info'], ignore_case=True))
    dp.register_message_handler(support_cmd, Text(startswith=[lang.button_message_support, '/support'],
                                                  ignore_case=True))
