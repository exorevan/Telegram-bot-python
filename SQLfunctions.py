import random

import psycopg2 as psycopg2


def return_random_image(cursor: psycopg2.extensions.cursor) -> int:
    cursor.execute(query="select count(*) from images")

    new_random: int = random.randint(a=1, b=cursor.fetchone()[0])

    return new_random


def return_image_name(cursor: psycopg2.extensions.cursor, image_number: int) -> str:
    cursor.execute(query=f"select name_of_image from images where id = {image_number}")

    new_image: str = cursor.fetchone()[0]

    return new_image


def return_image_language(cursor: psycopg2.extensions.cursor, image_number: int) -> str:
    cursor.execute(
        query=f"select lan.language_name from images im inner join languages lan on im.language_id = lan.id where im.id = {image_number}"
    )

    new_language: str = cursor.fetchone()[0]

    return new_language


def return_random_language(cursor: psycopg2.extensions.cursor) -> int:
    cursor.execute(query="select count(*) from languages")

    new_random: int = random.randint(a=1, b=cursor.fetchone()[0])

    return new_random


def return_language(cursor: psycopg2.extensions.cursor, number: int) -> str:
    cursor.execute(query=f"select language_name from languages where id = {number}")

    new_language: str = cursor.fetchone()[0]

    return new_language
