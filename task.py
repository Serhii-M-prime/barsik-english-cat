from DB import Queries as Q
import config_prod as c
from helper import *
from content import Messages as M, Stikers as S
from main import bot

query = Q()
user_list = query.getUsersList()
print(user_list)

for i in user_list:
    user = query.getUserById(i['id'])
    question =  getNewExercise(i['id'])
    print(question)
    if question is False:
            pass
    else:
        translations = strToList(question['t_' + user['lang'].lower()])
        bot.send_message(i['id'], getRandom(M["mes5"][user['lang']]).format(word=getRandom(translations)), parse_mode="HTML")

