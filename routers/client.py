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

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from keyboards import kb_client, get_main_menu
from logger.group_logger import groups_logger
from logger.log import logger
from minecraft import rcon
from provider import db
from custom_filters import TextInFilter


class FsmClient(StatesGroup):
    rcon = State()


client_router = Router()


async def rcon_cmd(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id
    is_admin = await db.check_admin_user(chat_id)
    if is_admin or await db.user_exists(chat_id):
        role = "администратора" if is_admin else '"normal"'
        logger.info(
            f"Пользователь с id {user_id} вошел в rcon консоль с правами {role}"
        )
        await message.reply("Теперь пришли команду", reply_markup=kb_client.rcon_cancel)
        await state.set_state(FsmClient.rcon)
    else:
        await message.reply("У вас нет доступа к данной команде. Приобретите доступ.")


async def cancel_state_rcon(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    main_menu = await get_main_menu(chat_id)
    text = (
        "Ты вышел из консоли. Прикажи что исполнять!"
        if await db.check_admin_user(chat_id)
        else "Ты вышел из консоли. Каковы будут дальнейшие действия?"
    )
    await message.reply(text, reply_markup=main_menu)
    await state.clear()


async def get_command(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id
    low = message.text.lower()
    command = low.split(" ", 1)

    if not await db.check_admin_user(chat_id) and await db.command_exists(command[0]):
        logger.info(
            f"Пользователь с id {user_id} попытался выполнить заблокированную команду"
        )
        await groups_logger("RCON: ", user_id, message.text)
        await message.reply("Команда заблокирована! Используйте другую:)")
    else:
        result = rcon.command_execute(low)
        role = "Администратор" if await db.check_admin_user(chat_id) else "Пользователь"
        logger.info(f"{role} с id {user_id} выполнил команду: {low}")
        await groups_logger("RCON: ", user_id, message.text)
        await message.reply(f"Команда выполнена. Ответ сервера:\n{result}")
        await message.answer(
            "Вы можете продолжить выполнять команды. Просто пришлите мне их. Или введите отмена"
        )
        await state.set_state(FsmClient.rcon)


async def register_routers() -> None:
    client_router.message.register(
        rcon_cmd, TextInFilter(["/rcon", "❗ ркон"])
    )
    client_router.message.register(
        cancel_state_rcon, TextInFilter(["◀ отмена", "back"]), StateFilter(FsmClient.rcon)
    )
    client_router.message.register(get_command, StateFilter(FsmClient.rcon))
