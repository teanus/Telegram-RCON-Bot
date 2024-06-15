from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


class TextInFilter(BaseFilter):
    def __init__(self, texts: List[str]):
        self.texts = [text.lower() for text in texts]

    async def __call__(self, message: Message) -> bool:
        return message.text.strip().lower() in self.texts
