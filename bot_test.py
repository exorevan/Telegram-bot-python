import logging

import psycopg2 as psycopg2
from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN
from loc_types.test_module import TestModule

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

game = TestModule()


@dp.message_handler(commands=["start"])
async def check_answer(message: types.Message):
    await game.check_answer(message)


@dp.message_handler(content_types=["text"])
async def check_answer(message: types.Message):
    await game.test(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
