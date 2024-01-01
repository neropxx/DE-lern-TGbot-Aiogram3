from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

from datetime import datetime

from database.db_class import Database
from bot_set.db_connection import db_conn
from bot_set.texts import INSTRUCTION, CANCELLING, NOT_ADMIN
from bot_set.bot_states import BotStates
from bot_set.my_bot import my_bot


add_admin_router = Router()


@add_admin_router.message(Command("add_admin"))
async def add_admin_cmd(message: Message, state: FSMContext) -> None:
    """
    Хендлер команды добавления администратора. Если команду вызвал НЕ администратор, команда будет прервана middleware
    :param message: объект сообщения
    :param state: объект состояния бота
    :return: None
    """
    await message.reply(text=INSTRUCTION)
    await state.set_state(BotStates.wait_id_to_add_admin)

    # if Database.is_admin(user_id=message.from_user.id, conn=db_conn):
    #     await message.reply(text=INSTRUCTION)
    #     await state.set_state(BotStates.wait_id_to_add_admin)
    # # else:
    # #     await message.reply(text=NOT_ADMIN)


@add_admin_router.message(Command("cancel"), StateFilter(BotStates.wait_id_to_add_admin))
async def cancel_adding_cmd(message: Message, state: FSMContext) -> None:
    """
    Хендлер обрабатывает команду /cancel, которая отменяет добавление нового администратора
    :param message: объект сообщения
    :param state: объект состояния бота
    :return: None
    """
    await message.reply(text=CANCELLING)
    await state.clear()


@add_admin_router.message(F.text.isdigit(), StateFilter(BotStates.wait_id_to_add_admin))
async def get_new_admin_id(message: Message, state: FSMContext) -> None:
    """
    Хендлер обрабатывает сообщение с id пользователя, которого назначают администратором.
    Если назначение прошло успешно, пользователь, назначеный админом получает об этом сообщение, а
    назначивший администратор получает информацию о результате выполнения функции в любом случае.
    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """

    answer_text = Database.add_admin(conn=db_conn, user_id=int(message.text), date=str(datetime.now()))
    await message.reply(text=answer_text)

    if answer_text == Database.SUCCESS_ADD:
        await my_bot.send_message(chat_id=int(message.text), text="Вас назначили администратором этого бота! 🟢")
        await state.clear()

