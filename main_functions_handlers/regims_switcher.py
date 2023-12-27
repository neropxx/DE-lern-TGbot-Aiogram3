from aiogram import F
from aiogram.fsm.context import FSMContext
from bot_set.bot_states import BotStates
from aiogram.filters import StateFilter
from aiogram import types
from aiogram import Router

noun_mode_router = Router()
verb_mode_router = Router()


@verb_mode_router.message(F.text.in_(["Хочу узнать больше о глаголах  🧠", "глагол", "Глагол", "глаголы", "Глаголы"]),
                          StateFilter(BotStates.verb))
async def verb_mode_ready(message: types.Message) -> None:
    """Хендлер сообщает пользователю, если бот уже работает в режиме, запрошенном пользователем"""
    await message.reply(text="Бот уже работает в этом режиме!  🛑")


# @verb_mode_router.message((F.text.in_({"Хочу узнать больше о глаголах  🧠", "глагол", "Глагол", "глаголы", "Глаголы"})),
#                           BotStates.verb)
# async def verb_mode_ready(message: types.Message) -> None:
#     await message.reply(text="Бот уже работает в этом режиме!  🛑")


@verb_mode_router.message(F.text.in_({"Хочу узнать больше о глаголах  🧠", "глагол", "Глагол", "глаголы", "Глаголы"}),
                          ~StateFilter(BotStates.verb))
async def verb_mode(message: types.Message, state: FSMContext) -> None:
    """Хендлер переключатель состояния в режим работы с глаголами
    Срабатывает только если:
    текущее состояние не verb, вызван ключевым словом режима
    """
    await state.set_state(BotStates.verb)
    await message.reply(text="Теперь отправь мне любой глагол на немецком языке  🇩🇪")


@noun_mode_router.message(F.text.in_(["Хочу узнать больше о существительных  💪", "существительные", "Существительные",
                                      "существительное", "Существительное"]), StateFilter(BotStates.noun))
async def noun_mode_ready(message: types.Message) -> None:
    """Хендлер сообщает пользователю, если бот уже работает в режиме, запрошенном пользователем"""
    await message.reply(text="Бот уже работает в этом режиме!  🛑")

#
# @noun_mode_router.message(F.text.in_(["Хочу узнать больше о существительных  💪", "существительные", "Существительные",
#                                       "существительное", "Существительное"]), BotStates.noun)
# async def noun_mode_ready(message: types.Message) -> None:
#     """Хендлер отлавливает попытку переключить машину состояний в уже действующий режим работы с существительными"""
#     await message.reply(text="Бот уже работает в этом режиме!  🛑")


@noun_mode_router.message(F.text.in_(["Хочу узнать больше о существительных  💪", "существительные", "Существительные",
                                      "существительное", "Существительное"]), ~StateFilter(BotStates.noun))
async def noun_mode(message: types.Message, state: FSMContext) -> None:
    """Хендлер переключатель состояния в режим работы с существительными
    Срабатывает только если:
    текущее состояние не noun, вызван ключевым словом режима
    """
    await state.set_state(BotStates.noun)
    await message.reply(text="Теперь отправь мне любое существительное на немецком языке 🇩🇪")
