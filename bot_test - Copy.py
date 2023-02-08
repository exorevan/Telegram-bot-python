import logging
import random

import numpy as np
from aiogram.types import InputFile

import SQLfunctions
import psycopg2 as psycopg2
from aiogram import Bot, Dispatcher, executor, types

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)



class question_object(object):
    def __init__(self, formul, number_of_answers, answers, rightanswer):
        self.formul = str(formul)
        self.number_of_answers = number_of_answers
        self.answers = answers
        self.rightanswer = rightanswer


class person_and_question(object):
    def __init__(self, nickname, question, count):
        self.nickname = nickname
        self.question = question
        self.count = count


questions_array = []
persons_array = {}
current_question = None


def pars_answers():
    global questions_array
    questions_array = []

    f1 = open("answers.txt", "r", encoding='utf-8')
    f = f1.readlines()

    for line in f:
        if '___' not in line:
            line = line.strip().split('\n')[0]
            current_string = line.strip().split('|')
            new_question = question_object(current_string[1], current_string[2], current_string[3], current_string[4])
            questions_array.append(new_question)

    return 0


@dp.message_handler(commands=['start'])
async def check_answer(message: types.Message):
    global connection, cursor

    try:
        #connection = psycopg2.connect(
        #    user=config.user, password=config.password, host=config.host, database=config.db_name
        #)

        #cursor = connection.cursor()
        pars_answers()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Добавить вопрос"))
        markup.add(types.KeyboardButton("Начать тест"))
        markup.add(types.KeyboardButton("Удалить вопрос"))

        await message.answer("Ну что ж, начнём", reply_markup=markup)


    except Exception as _ex:
        await message.answer("Error")


async def add_question(message):
    await message.answer("Добавьте вопрос:")
    #question = await get_question_formul()


async def test(message):
    global current_question

    current_person = message.from_user.mention

    if (current_person not in dict.fromkeys(persons_array)):
        persons_array[current_person] = None
        print(current_person)

    if message.text == 'Начать тест':
        persons_array[current_person] = None

    current_question = persons_array[current_person]

    if current_question:
        if current_question.rightanswer.lower() == message.text.lower():
            await message.answer("Чел, харош")
        else:
            await message.answer("Насрал, " + current_question.rightanswer)
        await message.answer("Следующий вопрос:")

    #number = random.randint(0, len(questions_array) - 1)
    #current_question = questions_array[number]
    current_question = random.choice(questions_array)
    answers = current_question.answers.split(', ')

    persons_array[current_person] = current_question

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    new_range = list(range(0, int(current_question.number_of_answers)))
    random.shuffle(new_range)

    if int(current_question.number_of_answers) == 0:
        markup = types.ReplyKeyboardRemove()

    #print(answers)

    for i in new_range:
        markup.add(types.KeyboardButton(answers[i]))

    await message.answer(current_question.formul, reply_markup=markup, parse_mode = 'HTML')


@dp.message_handler(content_types=['text'])
async def check_answer(message: types.Message):
    if 'Новый вопрос:' in message.text:
        strings = message.text.split('|')

        new_question = question_object(strings[1], strings[2], strings[3], strings[4])
        questions_array.append(new_question)
        await message.answer("Вопрос добавлен!")
    else:
        await test(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
