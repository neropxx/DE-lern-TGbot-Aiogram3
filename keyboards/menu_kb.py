from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu_kb() -> ReplyKeyboardMarkup:
    """Функция создает и возвращает клавиатуру для меню бота"""

    menu_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Хочу узнать больше о глаголах  🧠"),
             KeyboardButton(text="Хочу узнать больше о существительных  💪")]
        ],
        resize_keyboard=True)

    return menu_kb
