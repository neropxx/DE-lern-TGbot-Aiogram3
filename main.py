import asyncio
from datetime import datetime
#импорт класс бота для типизации переменной в функции on_startup
from aiogram import Bot

#импорт созданного заранее объекта класса бота
from bot_set.my_bot import my_bot
#импорт созданного заранее объекта класса диспетчера
from bot_set.my_dispatcher import dp
#импорт класса взаимодействия с БД
from database.db_class import Database
#импорт заранее созданного коннектора к БД
from bot_set.db_connection import db_conn
#импорт мидлвари для регистрации
from bot_set.middleware import AdminCheckMiddleware

#импорт роутера и хендлера команды /start
from main_functions_handlers.start import start_router
from main_functions_handlers.start import start_cmd

#импорт роутеров и хендлеров переключения основных режимов работы бота
from main_functions_handlers.regims_switcher import verb_mode_router, noun_mode_router
from main_functions_handlers.regims_switcher import verb_mode, noun_mode, verb_mode_ready, noun_mode_ready
#импорт хендлеров, обрабатывающих обращения к боту в основных режимах работы: ответ на запрошенное слово,
#обработка ошибки (некорректного обращения, задачи), обработка ошибки (не текстовое обращение к боту)
from main_functions_handlers.noun_mode import noun_answer, noun_cyrillic_error_answer, noun_message_type_error_answer
from main_functions_handlers.verb_mode import verb_answer, verb_cyrillic_error_answer, verb_message_type_error_answer

#импорт роутера и хендлера для обработки колбека "prasens"
from callbacks_handlers.prasens import prasens_router
from callbacks_handlers.prasens import prasens_callback

#импорт роутера и хендлера для обработки колбека "präteritum"
from callbacks_handlers.prateritum import prateritum_router
from callbacks_handlers.prateritum import prateritum_callback

#импорт роутера команды добавления нового администратора
from admins_handlers.add_admin_cmd import add_admin_router
#импорт хендлеров цепочки сценария добавления нового администратора
from admins_handlers.add_admin_cmd import add_admin_cmd, get_new_admin_id, cancel_adding_cmd

#импорт роутера команды удаления администратора
from admins_handlers.delete_admin_cmd import delete_admin_router
#импорт хендлеров цепочки сценария удаления администратора
from admins_handlers.delete_admin_cmd import delete_admin_cmd, get_id_to_delete_admin, cancel_admin_deleting

#импорт роутера команды рассылки рекламного поста
from admins_handlers.ads_send_cmd import ads_send_router
#импорт хендлеров цепочки сценария создания рекламной рассылки
from admins_handlers.ads_send_cmd import (send_cmd, get_ads_text, get_confirm_callback, send_without_photo_callback,
                                          send_with_photo_callback, get_photo, confirm_photo, send_ads_without_button,
                                          add_button, get_btn_text, get_btn_link, confirm_button, cmd_cancel_ads_sending)


def on_startup(bot: Bot):
    "Функция on_startup выполняется сразу после запуска бота. Сообщает в консоль, что бот успешно запущен"
    print("Бот запущен!")


async def main() -> None:
    """
    Асинхронная функция main
    перед полингом выполняет регистрацию функции on_startup, миддлвари, роутеров
    удаляется стек обращений к боту, когда он был в режиме офлайн (выключен)
    :return: None
    """

    #регистрируется функция on_startup
    dp.startup.register(on_startup)

    #регистрация мидлвари на роутеры, испульзуемые хендлерами для обработки команд доступных только администратору бота
    add_admin_router.message.outer_middleware.register(AdminCheckMiddleware())
    delete_admin_router.message.outer_middleware.register(AdminCheckMiddleware())
    ads_send_router.message.outer_middleware.register(AdminCheckMiddleware())

    #регистрация всех роутеров бота в диспетчер
    dp.include_routers(start_router, verb_mode_router, noun_mode_router, prasens_router, prateritum_router,
                       add_admin_router, delete_admin_router, ads_send_router)

    #для удаления стека обращений к боту, пока бот был неактивен, открываем в асинхронном контекстном менеджере контекст
    #объекта бота
    async with my_bot.context():
        #удаляем вебхук и сбрасываем pending_updates
        await my_bot.delete_webhook(drop_pending_updates=True)
        try:
            #выполняем попытку ролинга бота
            await dp.start_polling(my_bot)
        except Exception as polling_error_text:
            #возникшие исключения при поллинге бота обрабатываются и выводятся в консоль с текстом ошибки
            print("При полинге бота возникла ошибка:", polling_error_text)
        finally:
            #при каждом завершении поллинга бота БД сохраняет изменения (commit) и закрывается (close)
            db_conn.commit()
            db_conn.close()


if __name__ == "__main__":
    try:
        #создается таблица в БД, если такой еще не существует
        Database.create_table(conn=db_conn)
        print("БД создана")

        #в БД добавляется информация о владельце бота, если такой строки еще нет
        Database.add_super_admin(conn=db_conn, date=str(datetime.now()))
    except Exception as db_error_text:
        #возникшие исключения обрабатываются и выводтся в консоль
        print(f"При создании БД или добавлении администратора возникла ошибка с текстом: {db_error_text}")

    #выполняется запуск асинхронной функции main
    asyncio.run(main())
