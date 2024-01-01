from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.dispatcher.middlewares.error import CancelHandler
from aiogram.types import Message, CallbackQuery
from aiogram.types import TelegramObject

from typing import Callable, Awaitable, Dict, Any, Union

from database.db_class import Database
from bot_set.db_connection import db_conn
from bot_set.my_bot import my_bot


class AdminCheckMiddleware(BaseMiddleware):
    """
    Класс middleware првоеряющий, является ли пользователь администратором. Если пользователь не администратор,
    пользователь получит сообщение об этом и процесс прервется.
    """
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:
        if not Database.is_admin(user_id=event.from_user.id, conn=db_conn):
            await my_bot.send_message(chat_id=event.from_user.id,
                                      text="Для выполнения этой команды вы должны быть администратором! 🟥")
            return
        return await handler(event, data)
