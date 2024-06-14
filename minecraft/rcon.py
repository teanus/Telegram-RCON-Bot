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


import os
from typing import List, Union
from dotenv import load_dotenv
from aiomcrcon import Client

load_dotenv()


def replace_color_tag(text: str) -> str:
    color_tags = [
        "§1",
        "§2",
        "§3",
        "§4",
        "§5",
        "§6",
        "§7",
        "§8",
        "§9",
        "§0",
        "§c",
        "§e",
        "§a",
        "§b",
        "§d",
        "§f",
        "§l",
        "§m",
        "§n",
        "§o",
        "§r",
    ]
    for char in color_tags:
        text = text.replace(char, "")
    return text


async def command_execute(command: str) -> Union[str, List[str]]:
    rcon_host = os.getenv("rcon_host")
    rcon_port = int(os.getenv("rcon_port"))
    rcon_password = os.getenv("rcon_password")
    try:
        async with Client(rcon_host, rcon_port, rcon_password) as mcr:
            response, status = await mcr.send_cmd(command)
            if status != 0:
                return f"Ошибка выполнения команды: статус {status}"
            return replace_color_tag(response)
    except ValueError:
        return "Ошибка: Неправильный формат порта RCON."
    except ConnectionError:
        return "Произошла ошибка RCON. Повторите попытку."
