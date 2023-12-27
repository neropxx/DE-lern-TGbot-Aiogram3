from aiogram import F
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest

from bot_set.bot_states import BotStates
from bot_set.my_bot import my_bot
from filters.word_filter import WordFilter
from processing.get_link import get_noun_link
from .regims_switcher import noun_mode_router


@noun_mode_router.message(F.text, StateFilter(BotStates.noun), ~F.text.startswith("/"), WordFilter())
async def noun_answer(message: types.Message):
    """Хендлер срабатавает только на текстовые сообщения,
    в состоянии машины состояний noun,
    если сообщение не начинается слешем (команда) /,
    если сообщение написано латиницей и не содержит специальных знаков или пробела, является длинее 1 символа

    Если существительное найдено, пользователь получает изображение в ответ на свое текстовое сообщение"""

    try:
        await my_bot.send_photo(chat_id=message.chat.id,
                                photo=get_noun_link(text=message.text),
                                caption="Вот ваше существительное  👨🏻‍🏫")
    except TelegramBadRequest:
        await message.reply(text="Такое существительно не найдено  👮‍♂️")


@noun_mode_router.message(F.text, StateFilter(BotStates.noun), ~F.text.startswith("/"), ~WordFilter(),
                          F.text.in_({"Хочу узнать больше о глаголах  🧠", "глагол", "Глагол", "глаголы", "Глаголы"}))
async def noun_cyrillic_error_answer(message: types.Message):
    """Хенделр сообщений, отвечает на оишбочные текстовые сообщения в режиме работы бота"""
    await message.reply(text="Напишите существительное длинее 1го символа латиницей без использования специальных "
                             "знаков или пробелов! 🙅‍♂️")


@noun_mode_router.message(~F.text, StateFilter(BotStates.noun))
async def noun_message_type_error_answer(message: types.Message):
    """Хендлер сообщений, отвечающий на сообщения ошибочного формата: не текстовые"""
    await message.reply(text="Я понимаю только текстовые сообщения. Пожалуйста, напишите существительное сообщением "
                             "латиницей 🤷‍♂️")
