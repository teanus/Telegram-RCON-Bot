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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from locales import lang

button_id = KeyboardButton(lang.button_message_id)
button_rcon = KeyboardButton(lang.button_message_rcon)
button_info = KeyboardButton(lang.button_message_info)
button_admin_panel = KeyboardButton(lang.button_message_panel_admin_settings)
button_support = KeyboardButton(lang.button_message_support)
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_id, button_rcon, button_info, button_support,
                                                          button_admin_panel)

button_cancel = KeyboardButton(lang.button_message_cancel)
button_panel_add_roles = KeyboardButton(lang.button_message_panel_add)
button_panel_commands = KeyboardButton(lang.button_message_panel_commands)
admin_panel_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_panel_add_roles, button_cancel,
                                                                 button_panel_commands)
button_panel_add_admin = KeyboardButton(lang.button_message_panel_add_admin)
button_panel_add_user = KeyboardButton(lang.button_message_panel_add_user)
button_back = KeyboardButton(lang.button_message_back)
admin_panel_add = ReplyKeyboardMarkup(resize_keyboard=True).add(button_panel_add_user,
                                                                button_back,
                                                                button_panel_add_admin)

button_panel_commands_add = KeyboardButton(lang.button_message_panel_commands_add)
button_panel_commands_remove = KeyboardButton(lang.button_message_panel_commands_remove)
button_back = KeyboardButton(lang.button_message_back)
panel_commands_switch = ReplyKeyboardMarkup(resize_keyboard=True).add(button_panel_commands_add, button_back,
                                                                             button_panel_commands_remove)

button_back = KeyboardButton(lang.button_message_back)
admin_back = ReplyKeyboardMarkup(resize_keyboard=True).add(button_back)
