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

import json
from typing import Dict, List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("template/messages"))


def load_keyboards(file_path: str) -> Dict[str, ReplyKeyboardMarkup]:
    """
    Загружает клавиатуры из JSON-файла и создает словарь объектов ReplyKeyboardMarkup.

    :param file_path: Путь к JSON-файлу, содержащему конфигурации клавиатур.
    :return: Словарь, где ключи - это названия клавиатур, а значения - объекты ReplyKeyboardMarkup.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    keyboards_dict = {}
    for name, params in data.items():
        if "keyboard" in params:
            keyboard_buttons = [
                [KeyboardButton(text=button) for button in row]
                for row in params["keyboard"]
            ]
            keyboards_dict[name] = ReplyKeyboardMarkup(
                resize_keyboard=params.get("resize_keyboard", True),
                keyboard=keyboard_buttons,
            )
    return keyboards_dict


def load_valid_commands(json_file_path: str) -> Dict[str, List[str]]:
    """
    Загружает допустимые команды из указанного JSON файла.

    :param json_file_path:
     Путь к JSON файлу, содержащему допустимые команды.
    :return:
        Словарь с допустимыми командами, где ключи - это состояния, а значения - списки команд.
    """
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data["valid_commands"]


def render_template_jinja(template_name, **context):
    template = env.get_template(template_name)
    return template.render(**context)
