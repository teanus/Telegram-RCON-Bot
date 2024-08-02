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

from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


class TextInFilter(BaseFilter):
    """
    Фильтр для проверки наличия текста сообщения в заданном списке текстов.

    :param texts: Список строк для проверки.
    """

    def __init__(self, texts: List[str]):
        """
        Инициализация фильтра.

        :param texts: Список строк для проверки.
        """
        self.texts = [text.lower() for text in texts]

    async def __call__(self, message: Message) -> bool:
        """
        Проверка, содержится ли текст сообщения в списке текстов.

        :param message: Сообщение Telegram.
        :return: True, если текст сообщения содержится в списке, иначе False.
        :rtype: bool
        """
        return message.text.lower() in self.texts
