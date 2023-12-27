from bot_set.bot_states import BotStates
from bot_set.links import VERB_LINK, PRESENS_LINK
from bot_set.my_bot import my_bot

from aiogram import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import callback_query
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

prasens_router = Router()


@prasens_router.callback_query(F.data == "presens", StateFilter(BotStates.verb))
async def prasens_callback(callback_data: callback_query, state: FSMContext) -> None:
    """
    Хендлер колбека от клавиатуры под информацией о глаголе
    Выводит пользователю информацию о текущем глаголе в презенсе

    :param callback_data: объект колбека
    :param state: объект состояния
    :return: None
    """

    data = await state.get_data()
    wort_link = PRESENS_LINK + (data["word_link"].replace(VERB_LINK, ""))

    await callback_data.answer(text="Будет выполнено  🫡")

    try:
        await my_bot.send_photo(chat_id=callback_data.from_user.id,
                                photo=wort_link,
                                caption="Этот глагол в Präsens  👨🏻‍🏫")
    except TelegramBadRequest:
        await my_bot.send_message(chat_id=callback_data.from_user.id,
                                  text="Для этого глагола данные не найдены  👮‍♂️")
