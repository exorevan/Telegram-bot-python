import random

import psycopg2 as psycopg2


def return_random_image(cursor):
    cursor.execute(
        """select count(*)
        from images"""
    )

    new_random = random.randint(1, cursor.fetchone()[0])

    return new_random


def return_image_name(cursor, image_number):
    cursor.execute(
        """select name_of_image
        from images
        where id = """ + str(image_number)
    )

    new_image = cursor.fetchone()[0]

    return new_image


def return_image_language(cursor, image_number):
    cursor.execute(
        """select lan.language_name
        from images im
        inner join languages lan on im.language_id = lan.id
        where im.id = """ + str(image_number)
    )

    new_language = cursor.fetchone()[0]

    return new_language


def return_random_language(cursor):
    cursor.execute(
        """select count(*)
        from languages"""
    )

    new_random = random.randint(1, cursor.fetchone()[0])

    return new_random


def return_language(cursor, number):
    cursor.execute(
        """select language_name
        from languages
        where id = """ + str(number)
    )

    new_language = cursor.fetchone()[0]

    return new_language
