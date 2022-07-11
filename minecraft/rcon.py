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


from mcrcon import MCRcon
from resources import config


def replace_color_tag(text):
    color_tags = ["§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "§0", "§c", "§e", "§a", "§b", "§d", "§f", "§l",
                  "§m", "§n", "§o", "§r"]
    for char in color_tags:
        text = text.replace(char, '')
    return text


def command_execute(command):
    try:
        with MCRcon(config.rcon()['HOST'], config.rcon()['PASSWORD'], config.rcon()['PORT']) as mcr:
            mcr.connect()
            response = mcr.command(command)
            return replace_color_tag(response)
    finally:
        return 'Произошла ошибка RCON. Повторите попытку'
