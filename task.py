from core.DB import Queries as Query
import core.config as c
from core.helper import *
from core.content import messages as msg
import telebot

bot = telebot.TeleBot(c.TOKEN)
query = Query()
# get list with users for sending messages
user_list = query.get_users_list()
for i in user_list:
    user = query.get_user_by_id(i['id'])
    question = get_new_exercise(i['id'])
    if question is False:
            pass
    else:
        # get translation and send message with questions
        translations = str_to_list(question['t_' + user['lang'].lower()])
        bot.send_message(i['id'], get_random(msg["mes5"][user['lang']]).format(
            word=get_random(translations)), parse_mode="HTML")
        # if hint exist send message with hint
        hint = question['hint_' + user['lang'].lower()]
        if hint is not None:
            bot.send_message(i['id'], get_random(
                msg["mes11"][user['lang']]).format(hint=hint),
                             parse_mode="HTML")
