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


from provider import db
from resources import config


async def console_add_super_admin() -> str:
    if config.console()["give_role"]:
        admin_id = input(
            "Введите id для выдачи прав super-админа или нажмите Enter для пропуска: "
        )
        if admin_id == "":
            return "Закрытие"
        elif await db.check_admin_user(admin_id):
            return admin_id + " уже есть в списке супер-админов"
        else:
            await db.add_admin(admin_id)
            return admin_id + " был добавлен в список супер-админов"
    else:
        return "Режим выдачи роли выключен. Пропускаем"
