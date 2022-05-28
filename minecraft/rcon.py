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


from mcrcon import MCRcon
from Config import MC_HOST, MC_PASSWORD, MC_PORT
from locales import lang


def replace_color_tag(text):
    color_tags = ["§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "§0", "§c", "§e", "§a", "§b", "§d", "§f", "§l",
                  "§m", "§n", "§o", "§r"]
    for char in color_tags:
        text = text.replace(char, '')
    return text


def command_execute(command):
    try:
        with MCRcon(MC_HOST, MC_PASSWORD, MC_PORT) as mcr:
            mcr.connect()
            response = mcr.command(command)
            return replace_color_tag(response)
    except:
        return lang.message_server_error
