#           Free версия бота проекта LostWeyn
#               Telegram: t.me/lostweyn_project
#  #
#           Контакты разработчика:
#               VK: vk.com/dimawinchester
#               Telegram: t.me/teanus
#               Github: github.com/teanus
#               24serv: talk.24serv.pro/u/teanus
#  #
#  #
#      ██╗      ██████╗ ███████╗████████╗██╗    ██╗███████╗██╗   ██╗███╗   ██╗
#      ██║     ██╔═══██╗██╔════╝╚══██╔══╝██║    ██║██╔════╝╚██╗ ██╔╝████╗  ██║
#      ██║     ██║   ██║███████╗   ██║   ██║ █╗ ██║█████╗   ╚████╔╝ ██╔██╗ ██║
#      ██║     ██║   ██║╚════██║   ██║   ██║███╗██║██╔══╝    ╚██╔╝  ██║╚██╗██║
#      ███████╗╚██████╔╝███████║   ██║   ╚███╔███╔╝███████╗   ██║   ██║ ╚████║
#      ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚══╝╚══╝ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝


import Config
from locales import lang
from provider import sqlite_db


def console_add_super_admin():
    if Config.console_on_role:
        admin_id = input(lang.message_console_add_super_admin)
        if admin_id == '':
            return 'Close'
        elif sqlite_db.check_admin_user(admin_id):
            return admin_id + lang.message_panel_admin_is_exists
        else:
            sqlite_db.admin_add(admin_id)
            return admin_id + lang.message_sqlite_add_admin
    else:
        return
