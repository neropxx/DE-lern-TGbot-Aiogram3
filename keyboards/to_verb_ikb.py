from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_to_verb_ikb() -> InlineKeyboardMarkup:
    """Функция создает и возвращает инлайн клавиатуру для каждого глагола. Содержит 2 кнопки с колбеками."""

    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Präteritum  👀", callback_data="preteritum")],
            [InlineKeyboardButton(text="Präsens  👀", callback_data="presens")]
        ], row_width=2)

    return ikb
