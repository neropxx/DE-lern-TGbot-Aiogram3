from aiogram import Bot
from config_reader import config

# получаем экземпляр бота в переменную
my_bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
