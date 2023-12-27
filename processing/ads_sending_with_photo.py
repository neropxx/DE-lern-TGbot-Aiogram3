from bot_set.my_bot import my_bot
from database.db_class import Database
from bot_set.db_connection import db_conn

from aiogram.exceptions import TelegramAPIError
from datetime import datetime


async def sending_with_photo(author_id: int, text: str, photo_id: int, regim: str) -> None:
    """
    Функция выполняет рассылку рекламных сообщений в формате текст+фото
    после выполнения рассылки отправляется отчет сообщение автору рассылки.

    :param author_id: TELEGRAM ID пользователя, создавшего рассылку
    :param text: рекламный текст
    :param photo_id: Telegram ID рекламного фото
    :param regim: режим отправки (active - только активным пользователям, all - всем пользователям)
    :return: None
    """
    users_list = Database.get_users(regim=regim, conn=db_conn)
    success = 0
    failed = 0

    for i_user_id in users_list:
        try:
            await my_bot.send_photo(chat_id=i_user_id[0],
                                    photo=photo_id,
                                    caption=text)
            success += 1
            Database.update_activ_date(user_id=i_user_id[0],
                                       date=str(datetime.now()),
                                       conn=db_conn)
        except TelegramAPIError as ex:
            # print("При рассылке возникла ошибка: ", ex)
            failed += 1
            Database.update_activ_status(user_id=i_user_id[0],
                                         conn=db_conn)
    else:
        await my_bot.send_message(chat_id=author_id,
                                  text="Рассылка выполнена! Успешно отправлено {} сообщений\n"
                                       "Не доставлено {} сообщений".format(success, failed))
