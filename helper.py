import random
import time
from DB import Queries as Q

def getRandom(data):
    if len(data) == 0:
        return False
    else:
        return data[random.randint(0, len(data)-1)]

def extract_arg(arg):
    return arg.split()[1:]

def extract_ansver(text):
    return text.split()[0]

def getNewExercise(id):
    query = Q()
    next_question = getRandom(query.getWordsList(id))
    if next_question :
        query.setWorldId(
            {
                "id": id,
                "w_id": next_question['id'],
                "time": time.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )
        if next_question['flag'] is None:
            query.setUserWord(
                id,
                next_question['id']
            )
        else:
            query.updateLastAsk(id, next_question['id'])

    return next_question

def strToList(string):
    return string.split(";")