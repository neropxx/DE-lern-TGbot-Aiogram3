from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_choose_photo_regim_ikb() -> InlineKeyboardMarkup:
    """
    Функция создания инлайн клавиатуры с двумя кнопками

    :return: объект клавиатуры
    """
    photo_choose_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="WITH PHOTO 📸", callback_data="WITH PHOTO")],
            [InlineKeyboardButton(text="WITHOUT PHOTO 📷", callback_data="WITHOUT PHOTO")]
        ], row_width=2
    )

    return photo_choose_ikb
