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

    qa_all: list[list[Question]] | None = None
    persons_array: list[PersonAndQuestion] | None = None

    def __init__(self) -> None:
        self.qa_all = []
        self.persons_array = []
        self.current_question = None
        self.pack_choose = None

    def parse_answers(self) -> None:
        """
        Parses the questions and answers from text files and stores them in the `qa_all` list.
        """
        self.qa_all = [[] for _ in range(NUM_ANSWERS)]

        for i in range(MAX_FILE_NUMBER):
            file_path: str = FILE_TEMPLATE % i

            if os.path.exists(path=file_path):
                with open(file=file_path, mode="r", encoding="utf-8") as f1:
                    lines: list[str] = f1.readlines()

                    for line in lines:
                        if "___" not in line:
                            line: str = line.rstrip("\n")
                            current_string: list[str] = line.split(sep="|")
                            new_question: Question = Question(
                                formul=current_string[1],
                                number_of_answers=current_string[2],
                                answers=current_string[3],
                                right_answer=current_string[4],
                            )
                            self.qa_all[i].append(new_question)

        pack_mapping: dict[str, int] = {}

        for i in range(len(self.qa_all)):
            pack_name: str = f"пак {i}"
            pack_mapping[pack_name] = i

        self.pack_choose = pack_mapping

    async def check_answer(self, message: types.Message) -> None:
        """
        Checks the user's answer and provides a user interface for starting the test.
        """
        try:
            self.parse_answers()

            markup: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )
            markup.add(types.KeyboardButton("Начать тест"))

            await message.answer(text="Ну что ж, начнём", reply_markup=markup)

        except Exception as ex:
            _ = await message.answer(text=f"Error: {ex}")

    async def add_question(self, message: types.Message):
        """
        Provides a user interface for adding a question.
        """
        _ = await message.answer(text="Добавьте вопрос:")

    async def test(self, message: types.Message) -> None:
        """
        Handles the user's test progress, including checking the answer,
        updating the current question, and providing a user interface for selecting answers.
        """
        current_person: types.User = message.from_user.mention
        key = -1

        for index, person in enumerate(self.persons_array):
            if person.nickname == current_person:
                key: int = index
                break

        if key == -1:
            key: int = len(self.persons_array)
            logging.info(msg=current_person)

            new_person: PersonAndQuestion = PersonAndQuestion(nickname=current_person)
            self.persons_array.append(new_person)

        if message.text in self.pack_choose:
            self.persons_array[key].question_pack_number = self.pack_choose[
                message.text
            ]
        else:
            self.current_question = self.persons_array[key].question

            if self.current_question:
                if self.current_question.is_answer_correct(answer=message.text):
                    await message.answer(text="Чел, харош")
                else:
                    await message.answer(
                        text="Насрал, " + self.current_question.right_answer
                    )
                await message.answer(text="Следующий вопрос:")

        try:
            self.current_question = random.choice(
                seq=self.qa_all[self.persons_array[key].question_pack_number]
            )
        except IndexError:
            self.current_question = None

        answers: list[str] = self.current_question.answers.split(", ")

        self.persons_array[key].question = self.current_question

        markup: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
            resize_keyboard=True
        )

        new_range: list[int] = list(range(int(self.current_question.number_of_answers)))
        random.shuffle(x=new_range)

        if int(self.current_question.number_of_answers) == 0:
            markup: types.ReplyKeyboardRemove = types.ReplyKeyboardRemove()

        for i in new_range:
            try:
                markup.add(types.KeyboardButton(answers[i]))
            except Exception:
                logging.error(msg=f"error {self.current_question.formul}")

        await message.answer(
            text=self.current_question.formul, reply_markup=markup, parse_mode="HTML"
        )
