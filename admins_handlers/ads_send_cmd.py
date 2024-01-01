import asyncio

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest, TelegramAPIError

from database.db_class import Database
from bot_set.db_connection import db_conn
from bot_set.bot_states import BotStates
from bot_set.texts import INSTRUCTION_SEND, NOT_ADMIN_SEND, CONFIRM_INSTRUCTION
from keyboards.cofirm_ikb import get_confirm_ikb
from bot_set.my_bot import my_bot
from keyboards.choose_photo_regim import get_choose_photo_regim_ikb
from processing.ads_sending_without_photo import sending_without_photo
from keyboards.choose_btn_ikb import get_choose_button_regim_ikb
from processing.ads_sending_with_photo import sending_with_photo
from keyboards.ads_ikb import get_ads_ikb
from processing.ads_sending_with_btn import sending_with_btn

ads_send_router = Router()


@ads_send_router.message(Command("send"))
async def send_cmd(message: Message, state: FSMContext) -> None:
    """
    Хендлер команды отправки рекламного поста
    пропускает выполнение сценария далее только если команду вызывает администратор бота, иначе выполнение
    прерывается middlware
    состояние меняется если пользователь администор: ожидает рекламный текст от пользователя

    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    await state.set_state(BotStates.wait_text_to_send)
    await message.reply(text=INSTRUCTION_SEND)

    # if Database.is_admin(user_id=int(message.from_user.id), conn=db_conn):
    #     await state.set_state(BotStates.wait_text_to_send)
    #     await message.reply(text=INSTRUCTION_SEND)
    # else:
    #     await message.reply(text=NOT_ADMIN_SEND)


@ads_send_router.message(F.text, ~F.text.startswith("/"), StateFilter(BotStates.wait_text_to_send))
async def get_ads_text(message: Message, state: FSMContext) -> None:
    """
    Хендлер принимает текстовое содержание рекламного поста
    записывает рекламный текст в память состояния
    отправляет пример, как будет выглядеть рекламный пост

    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    await state.update_data(ads_text=message.text)
    ads_data = await state.get_data()

    await message.reply(text=CONFIRM_INSTRUCTION)
    await message.answer(text=ads_data["ads_text"], reply_markup=get_confirm_ikb())


@ads_send_router.callback_query(F.data == "CONFIRM", StateFilter(BotStates.wait_text_to_send))
async def get_confirm_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер колбека, подтверждающего содержание рекламного текста
    пользователю предлагается добавить фото к посту либо отправить пост без фото (только текст)
    состояние меняется: пользователь выбирает отправить пост без фото либо добавить фото

    :param callback_data: объект колбека
    :param state: объект состояния
    :return: None
    """
    await callback_data.answer(text="Текст сохранен! 📎")
    await my_bot.send_message(chat_id=callback_data.from_user.id,
                              text="Хотите добавить фото? 🌄",
                              reply_markup=get_choose_photo_regim_ikb())
    await state.set_state(BotStates.choose_photo_regim)


@ads_send_router.callback_query(StateFilter(BotStates.choose_photo_regim), F.data == "WITHOUT PHOTO")
async def send_without_photo_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер колбека, подтверждающего выбор отправки рекламного поста только с текстовым содержанием
    выполняется рассылка
    состояние сбрасывается

    :param callback_data: объект колбека
    :param state: объект состояния
    :return: None
    """
    await callback_data.answer(text="Вы выбрали рассылку без фото! 📜 Рассылка начнется через 2 секунды! 🤖",
                               show_alert=True)

    await asyncio.sleep(2)

    ads_data = await state.get_data()
    await sending_without_photo(author_id=callback_data.from_user.id,
                                text=ads_data["ads_text"],
                                regim="activ")
    await state.clear()


@ads_send_router.callback_query(StateFilter(BotStates.choose_photo_regim),
                                F.data == "WITH PHOTO")
async def send_with_photo_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер колбека, подтверждающего желание администратора добавить фото к рекламному посту
    приглашает администратора отправить фото
    состояние меняется: ожидание фото

    :param callback_data: объект колбека
    :param state: объект состояния
    :return: None
    """
    await callback_data.answer(text="Вы выбрали рассылку с фото! 🌄")
    await my_bot.send_message(chat_id=callback_data.from_user.id, text="Теперь пришлите мне фото! 🌇")

    await state.set_state(BotStates.wait_photo_to_send)


@ads_send_router.message(StateFilter(BotStates.wait_photo_to_send), F.photo)
async def get_photo(message: Message, state: FSMContext) -> None:
    """
    Хендлер сообщения, принимающий фото для рекламного поста
    записывает id фото в память состояния
    отправляет пример, как будет выглядеть рекламный пост

    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    await state.update_data(ads_photo=message.photo[0].file_id)

    await message.answer(text="Фото сохранено! 🌇 Теперь нужно подтвердить корректность поста. Если вы хотите изменить "
                              "фото, пришлите новое фото"
                              "\nВаша рассылка будет выглядеть так:")
    ads_data = await state.get_data()
    await my_bot.send_photo(chat_id=message.from_user.id,
                            photo=ads_data["ads_photo"],
                            caption=ads_data["ads_text"],
                            reply_markup=get_confirm_ikb())


@ads_send_router.callback_query(StateFilter(BotStates.wait_photo_to_send), F.data == "CONFIRM")
async def confirm_photo(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер колбека принимает подтверждение содержания рекламного поста текст+фото
    пользователю предлагается добавить кнопку к посту
    состояние меняется: ожидает выбор типа рекламного поста –– с кнопкой или без

    :param callback_data: объект колбека
    :param state: объект состояния
    :return: None
    """

    await callback_data.answer(text="👍")
    await my_bot.send_message(chat_id=callback_data.from_user.id, text="Рекламный пост сохранен! "
                                                                       "Хотите добавить кнопку с ссылкой?",
                              reply_markup=get_choose_button_regim_ikb())
    await state.set_state(BotStates.choose_btn_regim)


@ads_send_router.callback_query(StateFilter(BotStates.choose_btn_regim), F.data == "WITHOUT BUTTON")
async def send_ads_without_button(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер колбека, подтверждающего отправку рекламного поста без кнопки
    выполняется рассылка
    состояние сбрасывается

    :param callback_data: объект колбека
    :param state: объект состояния
    :return: None
    """
    await callback_data.answer(text="Вы выбрали рассылку без кнопки! 🟥 Рассылка начнется через 2 секунды! 🤖",
                               show_alert=True)

    await asyncio.sleep(2)

    ads_data = await state.get_data()
    await sending_with_photo(author_id=callback_data.from_user.id,
                             photo_id=ads_data["ads_photo"],
                             text=ads_data["ads_text"],
                             regim="activ")
    await state.clear()


@ads_send_router.callback_query(StateFilter(BotStates), F.data == "WITH BUTTON")
async def add_button(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер колбека, подтверждающий желание пользователя добавить кнопку к рекламному посту
    пользователб приглашается отправить текст кнопки
    состояние обновляется: ожидается текст для кнопки в рекламном посту

    :param callback_data: объект колбека
    :param state: объект состояния
    :return: None
    """
    await callback_data.answer(text="Теперь добавим текст и ссылку для кнопки")
    await my_bot.send_message(chat_id=callback_data.from_user.id, text="Пришлите текст для кнопки 🤖")

    await state.set_state(BotStates.wait_btn_text)


@ads_send_router.message(StateFilter(BotStates.wait_btn_text), F.text, ~F.text.startswith("/"))
async def get_btn_text(message: Message, state: FSMContext) -> None:
    """
    Хендлер сообщения, получабщего текст кнопки для рекламного поста
    текст записывается в память состояния
    пользователь приглашается отправить ссылку для рекламной кнопки
    состояние обновляется: ожидается ссылка для кнопки к рекламному посту

    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    await state.update_data(ads_button_text=message.text)

    await message.answer(text="Текст кнопки сохранен, теперь пришлите ссылку для этой кнопки")
    await state.set_state(BotStates.wait_btn_link)


@ads_send_router.message(StateFilter(BotStates.wait_btn_link), F.text, ~F.text.startswith("/"))
async def get_btn_link(message: Message, state: FSMContext) -> None:
    """
    Хендлер сообщения, получающий ссылку для кнопки к рекламному посту
    ссылка записывается в память состояния
    производится попытка отправить тестового рекламного сообщения автору рассылки
    пользователь приглашается подтвердить корректность рекламного поста

    при возникновении ошибки, пользователь приглашается изменить ссылку для кнопки

    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    await state.update_data(ads_button_link=message.text)

    ads_data = await state.get_data()

    try:
        await my_bot.send_photo(chat_id=message.from_user.id,
                                photo=ads_data["ads_photo"],
                                caption=ads_data["ads_text"],
                                reply_markup=(get_ads_ikb(ads_btn_text=ads_data["ads_button_text"],
                                                          ads_btn_link=ads_data["ads_button_link"])))

        await message.answer(text="Публикация сохранена! Вот так она будет выглядеть для пользователей ☝️")

        await my_bot.send_message(chat_id=message.from_user.id,
                                  text="Если вы хотите изменить текст, фотографию или текст кнопки, отмените создание "
                                       "рассылки и начните заново /cancel 🔴"
                                       "\n\nЕсли вы хотите изменить ссылку кнопки, просто пришлите ee еще раз ➿"
                                       "\n\nЕсли пост не требует правок и вы хотите его разослать, подтвердите это ⬇️🟢",
                                  reply_markup=get_confirm_ikb())

    except TelegramBadRequest and TelegramAPIError as error_text:
        await message.reply(text=f"Это не корректная ссылка, вызвающая ошибку: {error_text}\nПришлите другую ссылку! 🔴")


@ads_send_router.callback_query(StateFilter(BotStates.wait_btn_link), F.data == "CONFIRM")
async def confirm_button(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер колбекаЮ подтверждающего корректность рекламного поста текст+фото+кнопка(текст, ссылка)
    выполняется рассылка
    состояние сбрасывается

    :param callback_data: объект колбека
    :param state: объект состояния
    :return: None
    """
    await callback_data.answer(text="Рекламный пост готов! 🟩 Рассылка начнется через 2 секунды! 🤖",
                               show_alert=True)

    await asyncio.sleep(2)

    ads_data = await state.get_data()
    await sending_with_btn(author_id=callback_data.from_user.id,
                           text=ads_data["ads_text"],
                           photo_id=ads_data["ads_photo"],
                           ikb_to_send=get_ads_ikb(ads_btn_text=ads_data["ads_button_text"],
                                                   ads_btn_link=ads_data["ads_button_link"]),
                           regim="activ")
    await state.clear()


@ads_send_router.message(Command("cancel"), StateFilter(BotStates.wait_text_to_send,
                                                        BotStates.choose_photo_regim,
                                                        BotStates.wait_photo_to_send,
                                                        BotStates.confirm_with_photo,
                                                        BotStates.choose_btn_regim,
                                                        BotStates.wait_btn_text,
                                                        BotStates.wait_btn_link))
async def cmd_cancel_ads_sending(message: Message, state: FSMContext) -> None:
    """
    Хендлер команды отмены рассылки
    срабатывает в любом состоянии машины состояний
    состояние сбрасывается

    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    await message.reply(text="Вы отменили рассылку! 🔴")
    await state.clear()
