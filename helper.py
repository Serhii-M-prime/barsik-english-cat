import random
import time
from DB import Queries as Query


def get_random(data):
    """Get random item from list

    :param data: list with items
    :return: one random item from the received list
    """
    if len(data) == 0:
        return False
    else:
        return data[random.randint(0, len(data)-1)]


def extract_arg(arg):
    """Return second word from string

    :param arg: string
    :return: string word
    """
    return arg.split()[1:]


def extract_answer(text):
    """Return first word from string

    :param text: string
    :return: string word
    """
    return text.split()[0]


def get_new_exercise(user_id):
    """Return list with data for next question

    :param user_id: int
    :return: list
    """
    query = Query()
    next_question = get_random(query.get_words_list(user_id))
    if next_question:
        query.set_word_id(
            {
                "id": user_id,
                "w_id": next_question['id'],
                "time": time.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )
        if next_question['flag'] is None:
            query.set_user_word(
                user_id,
                next_question['id']
            )
        else:
            query.update_last_ask(user_id, next_question['id'])

    return next_question


def str_to_list(string):
    """Convert string to list by `;`

    :param string: string
    :return: list
    """
    return string.split(";")
