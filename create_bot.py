# импорт токена
import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import TOKEN
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # хранение в оперативке

storage = MemoryStorage()
# инициализация бота
bot_log = logging.getLogger("bot_log")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
