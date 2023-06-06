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


from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_id = KeyboardButton("🆔айди")
button_rcon = KeyboardButton("❗ркон")
button_info = KeyboardButton("🆘инфо")
button_admin_panel = KeyboardButton("⚙управление")
button_support = KeyboardButton("🆘поддержка")
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_id, button_rcon, button_info, button_support, button_admin_panel
)

button_cancel = KeyboardButton("◀отмена")
button_panel_roles = KeyboardButton("📝роли")
button_panel_commands = KeyboardButton("📝команды")
admin_panel_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_panel_roles, button_cancel, button_panel_commands
)

button_panel_add_roles = KeyboardButton("📝выдать")
button_panel_remove_roles = KeyboardButton("📝снять")
button_back = KeyboardButton("⏹назад")
roles_panel = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_panel_add_roles, button_back, button_panel_remove_roles
)

button_panel_admin = KeyboardButton("🪪админ")
button_panel_user = KeyboardButton("🪪обычный")
button_back = KeyboardButton("⏹назад")
roles_switch_panel = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_panel_user, button_back, button_panel_admin
)

button_panel_commands_add = KeyboardButton("⛔добавить")
button_panel_commands_remove = KeyboardButton("🗑удалить")
button_back = KeyboardButton("⏹назад")
panel_commands_switch = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_panel_commands_add, button_back, button_panel_commands_remove
)
button_back = KeyboardButton("⏹назад")
admin_back = ReplyKeyboardMarkup(resize_keyboard=True).add(button_back)
