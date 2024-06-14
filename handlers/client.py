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


from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import kb_admin, kb_client
from logger.group_logger import groups_logger
from logger.log import logger
from minecraft import rcon
from provider import db


class FsmOther(StatesGroup):
    rcon = State()


async def rcon_cmd(message: types.Message) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id
    if await db.check_admin_user(chat_id):
        logger.info(
            f"Пользователь с id {user_id} вошел в rcon консоль с правами администратора"
        )
        await message.reply("Теперь пришли команду", reply_markup=kb_client.rcon_cancel)
        await FsmOther.rcon.set()
    elif await db.user_exists(chat_id):
        logger.info(
            f"Пользователь с id {user_id} вошел в rcon консоль с правами \"normal\""
        )
        await message.reply("Теперь пришли команду", reply_markup=kb_client.rcon_cancel)
        await FsmOther.rcon.set()
    else:
        await message.reply("У вас нет доступа к данной команде. Приобретите доступ.")


async def cancel_state_rcon(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    if await db.check_admin_user(chat_id):
        await message.reply(
            "Ты вышел из консоли. Прикажи что исполнять!",
            reply_markup=kb_admin.main_menu,
        )
        await state.finish()
    else:
        await message.reply(
            "Ты вышел из консоли. Каковы будут дальнейшие действия?",
            reply_markup=kb_client.main_menu,
        )
        await state.finish()


async def get_command(message: types.Message) -> None:
    chat_id = message.chat.id
    low = message.text.lower()
    command = low.split(" ", 1)
    user_id = message.from_user.id
    if not await db.check_admin_user(chat_id):
        if await db.command_exists(command[0]):
            logger.info(
                f"Пользователь с id {user_id} попытался выполнить заблокированную команду"
            )
            await groups_logger("RCON: ", user_id, message.text)
            await message.reply("Команда заблокирована! Используйте другую:)")
        else:
            logger.info(f"Пользователь с id {user_id} выполнил команду: {message.text}")
            await groups_logger("RCON: ", user_id, message.text)
            await message.reply(
                f"Команда выполнена. Ответ сервера:\n{rcon.command_execute(low)}"
            )
            await message.answer(
                "Вы можете продолжить выполнять команды. Просто пришлите мне их. Или введите отмена"
            )
        await FsmOther.rcon.set()
    else:
        await message.reply(
            f"Команда выполнена. Ответ сервера:\n{rcon.command_execute(low)}"
        )
        logger.info(f"Администратор с id {user_id} выполнил команду: {message.text}")


def register_handlers_client(dp: Dispatcher) -> None:
    dp.register_message_handler(
        rcon_cmd, Text(startswith=["❗ркон", "/rcon"], ignore_case=True)
    )
    dp.register_message_handler(
        cancel_state_rcon, Text(equals="◀отмена"), state=FsmOther.rcon
    )
    dp.register_message_handler(get_command, state=FsmOther.rcon)
