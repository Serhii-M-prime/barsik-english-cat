from DB import Queries as Q
import config_prod as c
from helper import *
from content import Messages as M, Stikers as S, desc
import telebot

bot = telebot.TeleBot(c.TOKEN)

@bot.message_handler(commands=['init'])
def handle_init(message):
    id = message.from_user.id
    query = Q()
    if query.checkUser(id):
        user = query.getUserById(id)
        name = user['nickname']
        bot.send_message(id, M['mes2'][user['lang']].format(name=name))
    else:
        bot.send_message(id, "Начинаю сбор данных...")

        lang = extract_arg(message.text)
        if not lang : 
            bot.send_message(id, "Выберите оин из предложеных языков переводов и установите как первый параметр после функции `/inin UA` или `/init RU`.")
        else:
            if lang[0].upper() in c.languages:
                LN = lang[0].upper()
                name = message.from_user.first_name + ' ' + message.from_user.last_name
                query.addUser(
                    {
                    "nickname": name,
                    "id": id,
                    "lang": lang[0].upper(),
                    }
                )
                bot.send_message(id, M["mes3"][LN].format(name=name))
                bot.send_message(id, M["mes1"][LN])
            else :
                bot.send_message(id, "К сожелению введенный вами язык не поддерщивается")
        
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Hi, I'm very glad to see you!!!")
    bot.send_message(message.from_user.id, "Please set your language:  /init UA or /init RU")
    bot.send_message(message.from_user.id, desc, parse_mode="HTML")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, desc, parse_mode="HTML")

@bot.message_handler(commands=['changelanguage'])
def changeLanguage(message):
    id = message.from_user.id
    query = Q()
    if query.checkUser(id):
        lang = extract_arg(message.text)
        if not lang : 
            bot.send_message(id, "Выберите оин из предложеных языков переводов и установите как первый параметр после функции `/changelanguage UA` или `/changelanguage RU`.")
        else:
            if lang[0].upper() in c.languages:
                LN = lang[0].upper()
                query.changeUserLang(id, LN)
                bot.send_message(id, M["mes10"][LN])

@bot.message_handler(commands=['freeze'])
def freeze(message):
    id = message.from_user.id
    query = Q()
    if query.checkUser(id):
        user = query.getUserById(id)
        query.changeUserStatus(id, 0)
        bot.send_message(id, M["mes8"][user['lang']])

@bot.message_handler(commands=['unfreeze'])
def unfreeze(message):
    id = message.from_user.id
    query = Q()
    if query.checkUser(id):
        user = query.getUserById(id)
        query.changeUserStatus(id, 1)
        query.changeCarma(id, True)
        bot.send_message(id, M["mes9"][user['lang']])

@bot.message_handler(commands=['next'])
def handle_next(message):
    id = message.from_user.id
    query = Q()
    if query.checkUser(id):
        user = query.getUserById(id)
        if user['w_id'] is not None:
            query.updateUserWord(
                user['w_id'],
                id,
                False
            )
            query.setWorldId(
                {
                    "w_id": None,
                    "id": id,
                    "time": user['send_time']
                }
            )
    
        result = getNewExercise(id)
        if result is False:
            bot.send_message(id, M["mes6"][user['lang']])
        else:
            translations = strToList(result['t_' + user['lang'].lower()])
            bot.send_message(id, getRandom(M["mes5"][user['lang']]).format(word=getRandom(translations)), parse_mode="HTML")
            hint = question['hint_' + user['lang'].lower()]
            if hint is not None:
                bot.send_message(i['id'], getRandom(M["mes11"][user['lang']]).format(hint=hint), parse_mode="HTML")

@bot.message_handler(commands=['score'])
def handle_score(message):
    id = message.from_user.id
    query = Q()
    if query.checkUser(id):
        result = query.getScore()
        table = "<b> SCORE LIST: </b> \n"
        for i in result:
            table += "<b>" + i['nickname'] + "</b>" + " : " + "<i>" + str(i['score'])+ "</i>" + "\n"
        bot.send_message(id, table, parse_mode="HTML")
    else :
        pass

@bot.message_handler(content_types=['text'])
def handle_message(message):
    id = message.from_user.id
    query = Q()
    if query.checkUser(id):
        user = query.getUserById(id)
        result = query.getAnswer(id)
        if result['answer'] is None:
            bot.reply_to(message, getRandom(M["mes4"][user['lang']]))
        else :
            geted_answer = extract_ansver(message.text)
            if not geted_answer:
                pass
            else: 
                if geted_answer == result['answer'] :
                    query.updateUserWord(
                        user['w_id'],
                        id,
                        True
                    )
                    query.setWorldId(
                        {
                            "w_id": None,
                            "id": id,
                            "time": user['send_time']
                        }
                    )
                    bot.send_sticker(message.from_user.id, getRandom(S["YES"]))
                else:
                    query.updateUserWord(
                        user['w_id'],
                        id,
                        False
                    )
                    query.setWorldId(
                        {
                            "w_id": None,
                            "id": id,
                            "time": user['send_time']
                        }
                    )
                    bot.send_sticker(message.from_user.id, getRandom(S["NO"]))
                    bot.send_message(id, M["mes7"][user['lang']].format(word=result['answer']), parse_mode="HTML")
    else:
        pass
"""
@bot.message_handler(content_types=['sticker'])
def handle_sticers(message):
    print(message.sticker.file_id)
"""
bot.polling(none_stop=True, timeout=60)
