from aiogram.filters import CommandStart
from aiogram import Router
from aiogram import types

from datetime import datetime

from bot_set.texts import START_TEXT
from keyboards.menu_kb import get_menu_kb
from database.db_class import Database
from bot_set.db_connection import db_conn


start_router = Router()


@start_router.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    """Команда /start добавляет в БД запись о новом пользователе
    Если этот пользователь является владельцем бота, его профиль в БД получает статус администратора

    Команда удаляется и пользователь получает пригласительное сообщение с клавиатурой, где есть 2 кнопки
    Каждая кнопка клавиатуры соответствует одному из двух режимов бота"""

    Database.new_user_create(user_id=message.from_user.id,
                             date=str(datetime.now()),
                             conn=db_conn)

    await message.delete()
    await message.answer(text=START_TEXT, reply_markup=get_menu_kb())
