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


from pathlib import Path
from typing import Any, Dict
import json

path: Path = Path(__file__).resolve().parents[1] / "config.json"


def read_json() -> Dict[str, Any]:
    with open(path, "r") as file:
        return json.load(file)


def telegram() -> Dict[str, Any]:
    return read_json()["Telegram"]


def database() -> Dict[str, Any]:
    return read_json()["database"]


def sqlite() -> Dict[str, Any]:
    return read_json()["sqlite"]


def postgresql() -> Dict[str, Any]:
    return read_json()["postgresql"]


def console() -> Dict[str, Any]:
    return read_json()["console"]


def logging_config() -> Dict[str, Any]:
    return read_json()["logging"]
