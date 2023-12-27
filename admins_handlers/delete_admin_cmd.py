from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import F

from bot_set.bot_states import BotStates
from bot_set.db_connection import db_conn
from bot_set.my_bot import my_bot
from bot_set.texts import NOT_ADMIN_DEL, INSTRUCTION_DEL, CANCELLING_DEL
from bot_set.super_admin_data import SUPER_ADMIN
from database.db_class import Database

delete_admin_router = Router()


@delete_admin_router.message(Command("delete_admin"))
async def delete_admin_cmd(message: Message, state: FSMContext) -> None:
    """
    Хендлер отлавливет команду удаления администратора

    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    if Database.is_admin(user_id=message.from_user.id, conn=db_conn):
        await message.reply(text=INSTRUCTION_DEL)
        await state.set_state(BotStates.wait_id_to_delete_admin)
    else:
        await message.reply(text=NOT_ADMIN_DEL)


@delete_admin_router.message(Command("cancel"), StateFilter(BotStates.wait_id_to_delete_admin))
async def cancel_admin_deleting(message: Message, state: FSMContext) -> None:
    """
    Хендлер отлавливает отмену выполнения удаления администратора

    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    await message.reply(text=CANCELLING_DEL)
    await state.clear()


@delete_admin_router.message(F.text.isdigit(), StateFilter(BotStates.wait_id_to_delete_admin))
async def get_id_to_delete_admin(message: Message, state: FSMContext):
    """
    Хендлер сообщения с ID администратора, которого нужно разжаловать

    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """

    if int(message.text) == SUPER_ADMIN:
        await message.reply(text="Суперадмина нельзя разжаловать! 🔴\n"
                                 "Введите другой ID либо отмените добавление администратора выполнив команду /cancel")
    else:
        answer_text = Database.delete_admin(user_id=int(message.text), conn=db_conn)
        await message.reply(text=answer_text)

        if answer_text == Database.SUCCESS_DEL:
            await my_bot.send_message(chat_id=int(message.text), text="Вы больше не администратор этого бота! 🔴")
            await state.clear()
