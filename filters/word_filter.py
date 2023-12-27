from aiogram.filters import Filter
from aiogram.types import Message
from string import printable


class WordFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        """Кастомный фильтр проводит проверку введеного текста

        Возврашает True, если текст соответствует условиями:
        - Содержит буквы только немецкого алфавита
        - Не содержит знаков припенания, спец символов или пробелов
        - Слово длинее одного символа
        """

        allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZüöäßÜÖÄ")
        text = message.text.strip()

        if all(char in allowed_characters for char in text) and len(text) > 1:
            return True
        return False
