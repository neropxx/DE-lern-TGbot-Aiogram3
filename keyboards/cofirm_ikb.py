from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_confirm_ikb() -> InlineKeyboardMarkup:
    """
    Функция создания инлайн клавиатуры с единственной кнопкой

    :return: объект клавиатуры
    """
    confirm_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="CONFIRM 🟢", callback_data="CONFIRM")]
        ]
    )

    return confirm_ikb
