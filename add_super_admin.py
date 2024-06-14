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
    if not config.console()["give_role"]:
        return "Режим выдачи роли выключен. Пропускаем"

    admin_id = input(
        "Введите id для выдачи прав super-админа или нажмите Enter для пропуска: "
    )
    if admin_id == "":
        return "Закрытие"

    if await db.check_admin_user(admin_id):
        return f"{admin_id} уже есть в списке супер-админов"

    await db.add_admin(admin_id)
    return f"{admin_id} был добавлен в список супер-админов"
