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


import yaml
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'config.yaml'


def read_yaml():
    with open(path, "r") as file:
        return yaml.safe_load(file)


def telegram():
    return read_yaml()['Telegram']


def database():
    return read_yaml()['database']


def rcon():
    return read_yaml()['rcon']


def console():
    return read_yaml()['console']


def black_list():
    return read_yaml()['black_list']

