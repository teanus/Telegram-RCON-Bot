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

main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🆔 Айди"), KeyboardButton(text="❗ Ркон")],
        [KeyboardButton(text="🆘 Инфо"), KeyboardButton(text="⚙ Управление")],
        [KeyboardButton(text="🆘 Поддержка")],
    ],
)

admin_panel_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="📝 Роли"), KeyboardButton(text="📝 Команды")],
        [KeyboardButton(text="◀ Отмена")],
    ],
)

roles_panel = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="📝 Выдать"), KeyboardButton(text="📝 Снять")],
        [KeyboardButton(text="⏹ Назад")],
    ],
)

roles_switch_panel = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🪪 Админ"), KeyboardButton(text="🪪 Обычный")],
        [KeyboardButton(text="⏹ Назад")],
    ],
)

panel_commands_switch = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="⛔ Добавить"),
            KeyboardButton(text="🗑 Удалить"),
        ],
        [KeyboardButton(text="⏹ Назад")],
    ],
)

admin_back = ReplyKeyboardMarkup(
    resize_keyboard=True, keyboard=[[KeyboardButton(text="⏹ Назад")]]
)
