from DB import Queries as Q
import config_prod as c
from helper import *
from content import Messages as M, Stikers as S
import sys
import telebot

bot = telebot.TeleBot(c.TOKEN)
query = Q()
user_list = query.getUsersList()

for i in user_list:
    user = query.getUserById(i['id'])
    question =  getNewExercise(i['id'])
    if question is False:
            pass
    else:
        translations = strToList(question['t_' + user['lang'].lower()])
        bot.send_message(i['id'], getRandom(M["mes5"][user['lang']]).format(word=getRandom(translations)), parse_mode="HTML")
