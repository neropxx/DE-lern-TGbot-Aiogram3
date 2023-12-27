from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_choose_button_regim_ikb() -> InlineKeyboardMarkup:
    """
    Функция создания инлайн клавиатуры с двумя кнопками

    :return: объект клавиатуры
    """
    button_choose_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="WITH BUTTON 🟩", callback_data="WITH BUTTON")],
            [InlineKeyboardButton(text="WITHOUT BUTTON 🟥", callback_data="WITHOUT BUTTON")]
        ], row_width=2
    )

    return button_choose_ikb
