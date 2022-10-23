import logging
import random

from aiogram.types import InputFile

import SQLfunctions
import psycopg2 as psycopg2
from aiogram import Bot, Dispatcher, executor, types

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
connection = None
cursor = None
language_name = ""


@dp.message_handler(commands=['start'])
async def check_answer(message: types.Message):
    global connection, cursor

    try:
        connection = psycopg2.connect(
            user=config.user, password=config.password, host=config.host, database=config.db_name
        )

        cursor = connection.cursor()

        await message.answer("Hi")

        await new_question(message)
    except Exception as _ex:
        await message.answer("Error")


async def new_question(message):
    global language_name

    image_number = SQLfunctions.return_random_image(cursor)
    image_name = SQLfunctions.return_image_name(cursor, image_number)
    language_name = SQLfunctions.return_image_language(cursor, image_number)

    await message.answer("New question")

    random_button = random.randint(1, 4)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(4):
        if i == random_button:
            markup.add(types.KeyboardButton(language_name))
        else:
            markup.add(SQLfunctions.return_language(cursor, SQLfunctions.return_random_language(cursor)))

    new_photo = InputFile("images/" + image_name + ".jpg")

    await message.answer_photo(photo=new_photo, reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def check_answer(message: types.Message):
    global language_name

    await message.answer(language_name)
    await new_question(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
