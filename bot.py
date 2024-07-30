import logging
import random

from aiogram.types import InputFile

import SQLfunctions
import psycopg2 as psycopg2
import aiogram
from aiogram import executor

import config

logging.basicConfig(level=logging.INFO)

bot: aiogram.Bot = aiogram.Bot(token=config.TOKEN)
dp: aiogram.Dispatcher = aiogram.Dispatcher(bot)
connection: psycopg2.extensions.connection | None
cursor: psycopg2.extensions.cursor | None
language_name = ""


@dp.message_handler(commands=["start"])
async def check_answer(message: aiogram.types.Message) -> None:
    global connection, cursor

    try:
        connection: psycopg2.extensions.connection = psycopg2.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            database=config.db_name,
        )

        cursor: psycopg2.extensions.cursor = connection.cursor()

        await message.answer(text="Hi")

        await new_question(message)
    except Exception as _ex:
        await message.answer(text="Error")


async def new_question(message) -> None:
    global language_name

    image_number: int = SQLfunctions.return_random_image(cursor)
    image_name: str = SQLfunctions.return_image_name(cursor, image_number)
    language_name: str = SQLfunctions.return_image_language(cursor, image_number)

    await message.answer("New question")

    random_button: int = random.randint(a=1, b=4)
    markup: aiogram.types.ReplyKeyboardMarkup = aiogram.types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    for i in range(4):
        if i == random_button:
            markup.add(aiogram.types.KeyboardButton(language_name))
        else:
            markup.add(
                SQLfunctions.return_language(
                    cursor, number=SQLfunctions.return_random_language(cursor)
                )
            )

    new_photo: InputFile = InputFile(filename=f"images/{image_name}.jpg")

    await message.answer_photo(photo=new_photo, reply_markup=markup)


@dp.message_handler(content_types=["text"])
async def check_answer(message: aiogram.types.Message) -> None:
    global language_name

    await message.answer(text=language_name)
    await new_question(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
