import asyncio
from aiogram import Bot
from datetime import datetime

from bot_set.my_bot import my_bot
from bot_set.my_dispatcher import dp
from database.db_class import Database
from bot_set.db_connection import db_conn

from main_functions_handlers.start import start_router
from main_functions_handlers.start import start_cmd

from main_functions_handlers.regims_switcher import verb_mode_router, noun_mode_router
from main_functions_handlers.regims_switcher import verb_mode, noun_mode, verb_mode_ready, noun_mode_ready
from main_functions_handlers.noun_mode import noun_answer, noun_cyrillic_error_answer, noun_message_type_error_answer
from main_functions_handlers.verb_mode import verb_answer, verb_cyrillic_error_answer, verb_message_type_error_answer

from callbacks_handlers.prasens import prasens_router
from callbacks_handlers.prasens import prasens_callback

from callbacks_handlers.prateritum import prateritum_router
from callbacks_handlers.prateritum import prateritum_callback

from admins_handlers.add_admin_cmd import add_admin_router
from admins_handlers.add_admin_cmd import add_admin_cmd, get_new_admin_id, cancel_adding_cmd

from admins_handlers.delete_admin_cmd import delete_admin_router
from admins_handlers.delete_admin_cmd import delete_admin_cmd, get_id_to_delete_admin, cancel_admin_deleting

from admins_handlers.ads_send_cmd import ads_send_router
from admins_handlers.ads_send_cmd import (send_cmd, get_ads_text, get_confirm_callback, send_without_photo_callback,
                                          send_with_photo_callback, get_photo, confirm_photo, send_ads_without_button,
                                          add_button, get_btn_text, get_btn_link, confirm_button, cmd_cancel_ads_sending)


def on_startup(bot: Bot):
    print("Бот запущен!")


async def main() -> None:
    dp.startup.register(on_startup)
    dp.include_routers(start_router, verb_mode_router, noun_mode_router, prasens_router, prateritum_router,
                       add_admin_router, delete_admin_router, ads_send_router)

    async with my_bot.context():
        await my_bot.delete_webhook(drop_pending_updates=True)
        try:
            await dp.start_polling(my_bot)
        except Exception as polling_error_text:
            print("При полинге бота возникла ошибка:", polling_error_text)
        finally:
            db_conn.commit()
            db_conn.close()


if __name__ == "__main__":
    try:
        Database.create_table(conn=db_conn)
        print("БД создана")

        Database.add_super_admin(conn=db_conn, date=str(datetime.now()))
    except Exception as db_error_text:
        print(f"При создании БД или добавлении администратора возникла ошибка с текстом: {db_error_text}")

    asyncio.run(main())
