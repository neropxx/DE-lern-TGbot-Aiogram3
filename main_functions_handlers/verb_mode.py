from aiogram import F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboards.to_verb_ikb import get_to_verb_ikb
from bot_set.bot_states import BotStates
from bot_set.my_bot import my_bot
from filters.word_filter import WordFilter
from processing.get_link import get_verb_link
from .regims_switcher import verb_mode_router


@verb_mode_router.message(F.text, StateFilter(BotStates.verb), ~F.text.startswith("/"), WordFilter())
async def verb_answer(message: types.Message, state: FSMContext):
    """Хендлер срабатавает только на текстовые сообщения,
    в состоянии машины состояний verb,
    если сообщение не начинается слешем (команда) /,
    если сообщение написано латиницей и не содержит специальных знаков или пробела, является длинее 1 символа

    Если глагол найден, пользователь получает изображение в ответ на свое текстовое сообщение
    к изображению прикреплена инлайн клавиатура с двумя кнопка"""
    word_link = get_verb_link(text=message.text)

    if word_link:
        await state.update_data(word_link=word_link)

        await my_bot.send_photo(chat_id=message.chat.id,
                                photo=word_link,
                                caption="Вот ваш глагол  👨🏻‍🏫",
                                reply_markup=get_to_verb_ikb())
    else:
        await message.reply(text="Такой глагол не найден  👮‍♂️")


@verb_mode_router.message(F.text, StateFilter(BotStates.verb), ~F.text.startswith("/"), ~WordFilter(),
                          ~F.text.in_(["Хочу узнать больше о существительных  💪", "существительные", "Существительные",
                                       "существительное", "Существительное"]))
async def verb_cyrillic_error_answer(message: types.Message):
    """Хенделр сообщений, отвечает на оишбочные текстовые сообщения в режиме работы бота"""
    await message.reply(text="Напишите глагол длинее 1го символа латиницей без использования специальных "
                             "знаков или пробелов! 🙅‍♂️")


@verb_mode_router.message(~F.text, StateFilter(BotStates.verb))
async def verb_message_type_error_answer(message: types.Message):
    """Хендлер сообщений, отвечающий на сообщения ошибочного формата: не текстовые"""
    await message.reply(text="Я понимаю только текстовые сообщения. Пожалуйста, напишите глагол сообщением "
                             "латиницей 🤷‍♂️")

