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


import json
from pathlib import Path
from typing import Any, Dict

path: Path = Path(__file__).resolve().parents[1] / "config.json"


def read_json() -> Dict[str, Any]:
    """
    Читает и возвращает содержимое конфигурационного файла в виде словаря.

    :return: Словарь с данными из JSON-файла.
    :rtype: Dict[str, Any]
    """
    with open(path, "r") as file:
        return json.load(file)


def telegram() -> Dict[str, Any]:
    """
    Возвращает настройки для Telegram из конфигурационного файла.

    :return: Словарь с настройками Telegram.
    :rtype: Dict[str, Any]
    """
    return read_json()["Telegram"]


def database() -> Dict[str, Any]:
    """
    Возвращает настройки базы данных из конфигурационного файла.

    :return: Словарь с настройками базы данных.
    """
    return read_json()["database"]


def sqlite() -> Dict[str, Any]:
    """
    Возвращает настройки для SQLite из конфигурационного файла.

    :return: Словарь с настройками SQLite.
    :rtype: Dict[str, Any]
    """
    return read_json()["sqlite"]


def postgresql() -> Dict[str, Any]:
    """
    Возвращает настройки для PostgreSQL из конфигурационного файла.

    :return: Словарь с настройками PostgreSQL.
    :rtype: Dict[str, Any]
    """
    return read_json()["postgresql"]


def console() -> Dict[str, Any]:
    """
    Возвращает настройки выдачи прав из конфигурационного файла.

    :return: Словарь с настройками выдачи.
    :rtype: Dict[str, Any]
    """
    return read_json()["console"]


def logging_config() -> Dict[str, Any]:
    """
    Возвращает настройки логирования из конфигурационного файла.

    :return: Словарь с настройками логирования.
    :rtype: Dict[str, Any]
    """
    return read_json()["logging"]


def name_fields_table_list_commands() -> Dict[str, Any]:
    """
    Возвращает настройки полей таблицы команд из конфигурационного файла.

    :return: Словарь с настройками полей таблицы команд.
    :rtype: Dict[str, Any]
    """
    return read_json()["name_fields_table_list_commands"]
