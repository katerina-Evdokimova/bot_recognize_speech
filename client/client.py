import datetime
import os
from pathlib import Path

from aiogram import types, Dispatcher
from aiogram.types import ContentType, File

from create_bot import dp, bot, bot_log
from pydub import AudioSegment
import speech_recognition as sr


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'], state='*')


@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    await message.reply_sticker("CAACAgIAAxkBAAEDj8xhx3WJKEVjbr_spmZ85hDT86cFLQAChwIAAladvQpC7XQrQFfQkCME")
    await message.reply('...\tраспознаю только русский язык\t...')
    await message.delete()


@dp.message_handler()
async def command_dialog(message: types.Message):
    await message.reply('...\tя не понимаю...')
    # await message.delete()


async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f"{file_name}")


async def audio_to_text(dest_name: str, messages):
    # Функция для перевода аудио, в формате ".wav" в текст
    r = sr.Recognizer()
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)

    # используя возможности библиотеки распознаем текст, так же тут можно изменять язык распознавания.
    result = await r.recognize_google(messages, audio,
                                      language="ru_RU")
    return result


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    try:
        dirname = os.path.dirname(__file__)

        await message.answer('...5')
        voice = await message.voice.get_file()
        path = "file"
        # get and save the file

        filename = os.path.join(dirname, 'input.ogg')

        await handle_file(file=voice, file_name=filename, path=path)

        # convert .ogg in .wav
        ogg_version = AudioSegment.from_ogg(filename)
        filename_2 = os.path.join(dirname, 'new.wav')
        ogg_version.export(filename_2, format="wav")

        result = await audio_to_text(filename_2, message)
        await message.answer('...1')
        if result:
            await message.reply(result)
        else:
            await message.reply('Гс не распознано')
    except Exception as e:
        bot_log.error(f'voice_message_handler:{datetime.datetime.now()}\t{e}')
