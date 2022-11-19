# импорт необходимых модулей для работы
import datetime
import logging

from aiogram.utils import executor

from create_bot import dp, bot_log


async def on_startup(_):
    logging.basicConfig(filename="bot_log.log")
    bot_log.warning(f'on_startup:{datetime.datetime.now()}\tBot online. OK!')


# импорт хендлеров
from client import client

client.register_handlers_client(dp)

# start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# bf0af31866cc8c79a79abf14eccab8f75e2db468