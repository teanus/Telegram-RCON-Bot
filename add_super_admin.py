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
from render_template import render_template_jinja
from resources import config


async def console_add_super_admin() -> str:
    """
    Добавляет супер-администратора через консоль.

    :return: Возвращает строку с результатом выполнения.
    :rtype: str
    """
    root = "template"

    if not config.console()["give_role"]:
        return render_template_jinja(
            "add_super_admin/false_give_role.jinja2", root_directory_name=root
        )

    admin_id = input(
        render_template_jinja(
            "add_super_admin/messages.jinja2", root_directory_name=root
        )
    )

    if admin_id == "":
        return render_template_jinja(
            "add_super_admin/exit.jinja2", root_directory_name=root
        )

    context = {"admin_id": admin_id}

    if await db.check_admin(admin_id):
        return render_template_jinja(
            "add_super_admin/admin_exists.jinja2", root_directory_name=root, **context
        )

    await db.add_admin(admin_id)

    return render_template_jinja(
        "add_super_admin/add_admin.jinja2", root_directory_name=root, **context
    )
