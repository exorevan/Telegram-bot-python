import logging
import random

import numpy as np
from aiogram.types import InputFile
import datetime

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
    def __init__(self, nickname, count=0, question=None, pack=0):
        self.nickname = nickname
        self.count = count
        self.question = question
        self.pack = pack


"""questions_array0 = []
questions_array1 = []
questions_array2 = []
questions_array3 = []"""

qa_all = [[] for i in range(0, 4)]

persons_array = []
current_question = None


def pars_answers():
    global qa_all
    qa_all = [[] for i in range(0, 4)]

    for i in range(0, 4):
        f1 = open(f"answers {i}.txt", "r", encoding='utf-8')
        f1 = f1.readlines()

        for line in f1:
            if '___' not in line:
                line = line.strip().split('\n')[0]
                current_string = line.strip().split('|')
                new_question = question_object(current_string[1], current_string[2], current_string[3],
                                               current_string[4])
                for j in range(0, 4):
                    qa_all[j].append(new_question)


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
    global persons_array

    if message.text == 'Начать тест':
        persons_array = []

        print(f'--------------------------{datetime.datetime.now().time()}')

    current_person = message.from_user.mention

    key = 0

    for i in range(len(persons_array)):
        if persons_array[i].nickname == current_person:
            key = i

    if key == 0:
        key = len(persons_array)
        print(current_person)

        new_person = person_and_question(current_person, 0)
        persons_array.append(new_person)

    if message.text == 'пак 0':
        persons_array[key].pack = 0
    elif message.text == 'пак 1':
        persons_array[key].pack = 1
    elif message.text == 'пак 2':
        persons_array[key].pack = 2
    elif message.text == 'пак 3':
        persons_array[key].pack = 3

    current_question = persons_array[key].question

    if current_question:
        if current_question.rightanswer.lower() == message.text.lower():
            await message.answer("Чел, харош")
        else:
            await message.answer("Насрал, " + current_question.rightanswer)
        await message.answer("Следующий вопрос:")

    #number = random.randint(0, len(questions_array) - 1)
    #current_question = questions_array[number]


    current_question = random.choice(qa_all[persons_array[key].pack])
        
    answers = current_question.answers.split(', ')

    persons_array[key].question = current_question

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    new_range = list(range(0, int(current_question.number_of_answers)))
    random.shuffle(new_range)

    if int(current_question.number_of_answers) == 0:
        markup = types.ReplyKeyboardRemove()

    #print(answers)

    for i in new_range:
        try:
            markup.add(types.KeyboardButton(answers[i]))
        except Exception:
            print(f"error {current_question.formul}")


    await message.answer(current_question.formul, reply_markup=markup, parse_mode = 'HTML')


@dp.message_handler(content_types=['text'])
async def check_answer(message: types.Message):
    if 'Новый вопрос:' in message.text:
        strings = message.text.split('|')

        new_question = question_object(strings[1], strings[2], strings[3], strings[4])
        #questions_array.append(new_question)
        await message.answer("Вопрос добавлен!")
    else:
        await test(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
