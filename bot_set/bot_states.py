from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    """Класс описывающий состояния бота

    ОСНОВНОЙ ФУНКЦИОНАЛ БОТА
    verb - режим работы "глаголы"
    noun - режим работы "существительное"

    РАБОТА С ПРАВАМИ ПОЛЬЗОВАТЕЛЕЙ
    wait_id_to_add_admin - ожидается айди пользователя, которого нужно назначить администратором
    wait_id_to_delete_admin - ожидается айди пользователя, которого нужно разжаловать из статуса администратора

    РЕКЛАМНЫЕ ВОЗМОЖНОСТИ БОТА
    wait_text_to_send - ожидает рекламный текст
    choose_photo_regim - ожидает выбор типа рекламного поста (с фото или без)
    wait_photo_to_send - ожидает рекламное фото (баннер)
    confirm_with_photo - подтверждение выбранного фото
    choose_btn_regim - ожидает выбор типа рекламного поста (с кнопкой или без)
    wait_btn_text - ожидает текст для кнопки
    wait_btn_link - ожидает ссылку для кнопки
    """

    verb = State()
    noun = State()

    wait_id_to_add_admin = State()
    wait_id_to_delete_admin = State()

    wait_text_to_send = State()
    choose_photo_regim = State()
    wait_photo_to_send = State()
    confirm_with_photo = State()
    choose_btn_regim = State()
    wait_btn_text = State()
    wait_btn_link = State()
