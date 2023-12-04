import logging
import os
import random

import psycopg2 as psycopg2
from aiogram import types
from config import FILE_TEMPLATE, MAX_FILE_NUMBER, NUM_ANSWERS

from loc_types.person_and_question import PersonAndQuestion
from loc_types.question import Question


class TestModule:
    """
    The `TestModule` class is a module that allows users to take a test by answering questions.
    It reads the questions and answers from text files, keeps track of the user's progress,
    and provides a user interface for adding, starting, and deleting questions.
    """

    def __init__(self):
        self.qa_all = []
        self.persons_array = []
        self.current_question = None
        self.pack_choose = None

    def parse_answers(self):
        """
        Parses the questions and answers from text files and stores them in the `qa_all` list.
        """
        self.qa_all = [[] for _ in range(NUM_ANSWERS)]

        for i in range(MAX_FILE_NUMBER):
            file_path = FILE_TEMPLATE % i

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f1:
                    lines = f1.readlines()

                    for line in lines:
                        if "___" not in line:
                            line = line.rstrip("\n")
                            current_string = line.split("|")
                            new_question = Question(
                                current_string[1],
                                current_string[2],
                                current_string[3],
                                current_string[4],
                            )
                            self.qa_all[i].append(new_question)

        pack_mapping = {}

        for i in range(len(self.qa_all)):
            pack_name = f"пак {i}"
            pack_mapping[pack_name] = i

        self.pack_choose = pack_mapping

    async def check_answer(self, message: types.Message):
        """
        Checks the user's answer and provides a user interface for starting the test.
        """
        try:
            self.parse_answers()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Начать тест"))

            await message.answer("Ну что ж, начнём", reply_markup=markup)

        except Exception as ex:
            await message.answer("Error")

    async def add_question(self, message):
        """
        Provides a user interface for adding a question.
        """
        await message.answer("Добавьте вопрос:")

    async def test(self, message):
        """
        Handles the user's test progress, including checking the answer,
        updating the current question, and providing a user interface for selecting answers.
        """
        current_person = message.from_user.mention
        key = -1

        for index, person in enumerate(self.persons_array):
            if person.nickname == current_person:
                key = index
                break

        if key == -1:
            key = len(self.persons_array)
            logging.info(current_person)

            new_person = PersonAndQuestion(current_person)
            self.persons_array.append(new_person)

        if message.text in self.pack_choose:
            self.persons_array[key].question_pack_number = self.pack_choose[
                message.text
            ]
        else:
            self.current_question = self.persons_array[key].question

            if self.current_question:
                if self.current_question.is_answer_correct(message.text):
                    await message.answer("Чел, харош")
                else:
                    await message.answer(
                        "Насрал, " + self.current_question.right_answer
                    )
                await message.answer("Следующий вопрос:")

        try:
            self.current_question = random.choice(
                self.qa_all[self.persons_array[key].question_pack_number]
            )
        except IndexError:
            self.current_question = None

        answers = self.current_question.answers.split(", ")

        self.persons_array[key].question = self.current_question

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        new_range = list(range(int(self.current_question.number_of_answers)))
        random.shuffle(new_range)

        if int(self.current_question.number_of_answers) == 0:
            markup = types.ReplyKeyboardRemove()

        for i in new_range:
            try:
                markup.add(types.KeyboardButton(answers[i]))
            except Exception:
                logging.error(f"error {self.current_question.formul}")

        await message.answer(
            self.current_question.formul, reply_markup=markup, parse_mode="HTML"
        )
