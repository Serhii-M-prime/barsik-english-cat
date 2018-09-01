from core.DB import Queries as Query
import core.config as c
from core.helper import *
from core.content import messages as msg
import telebot

bot = telebot.TeleBot(c.TOKEN)
query = Query()
# check inactive users
slipping_users = query.get_slipping_user()
for user in slipping_users:
    if user['carma'] < c.carma:
        question = get_new_exercise(user['id'])
        if question is False:
            pass
        else:
            query.change_carma(user['id'], False)
            if user['carma'] + 1 == c.carma:
                bot.send_message(user['id'], msg["mes13"][user['lang']],
                                 parse_mode="HTML")
            else:
                bot.send_message(user['id'], msg["mes12"][user['lang']].format(
                                 your_carma=user['carma'] + 1, carma=c.carma),
                                 parse_mode="HTML")

            # get translation and send message with questions
            translations = str_to_list(question['t_' + user['lang'].lower()])
            bot.send_message(user['id'],
                             get_random(msg["mes5"][user['lang']]).format(
                                 word=get_random(translations)),
                             parse_mode="HTML")
            # if hint exist send message with hint
            hint = question['hint_' + user['lang'].lower()]
            if hint is not None:
                bot.send_message(user['id'], get_random(
                    msg["mes11"][user['lang']]).format(hint=hint),
                                 parse_mode="HTML")
    else:
        query.change_user_status(user['id'], 0)

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
