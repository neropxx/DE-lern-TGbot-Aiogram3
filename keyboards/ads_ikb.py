from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_ads_ikb(ads_btn_text: str, ads_btn_link: str) -> InlineKeyboardMarkup:
    """
    Функция создает обхект инлайн клавиатуры с единственной кнопкой с текстом и ссылкой в кнопке
    клавиатура используется в рекламном посте

    :param ads_btn_text: текст на кнопке
    :param ads_btn_link: ссылка на кнопке
    :return: объект клавиатуры
    """
    ads_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ads_btn_text, url=ads_btn_link)],
        ], row_width=1
    )

    return ads_ikb
