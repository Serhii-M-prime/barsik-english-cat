from DB import Queries as Query
import config as c
from helper import *
from content import messages as msg, stickers as stk, desc
import telebot

bot = telebot.TeleBot(c.TOKEN)


@bot.message_handler(commands=['init'])
def handle_init(message):
    """Add new user to db.

    :param message: telebot message object
    :return: void
    """
    chat_id = message.from_user.id
    query = Query()
    if query.check_user(chat_id):
        user = query.get_user_by_id(chat_id)
        name = user['nickname']
        bot.send_message(chat_id, msg['mes2'][user['lang']].format(name=name))
    else:
        bot.send_message(chat_id, "Начинаю сбор данных...")

        lang = extract_arg(message.text)
        if not lang:
            bot.send_message(chat_id, "Выберите оин из предложеных языков\
             переводов и установите как первый параметр после функции\
              `/init UA` или `/init RU`.")
        else:
            if lang[0].upper() in c.languages:
                language = lang[0].upper()
                name = message.from_user.first_name + ' ' \
                    + message.from_user.last_name
                query.add_user(
                    {
                        "nickname": name,
                        "id": chat_id,
                        "lang": lang[0].upper(),
                    }
                )
                bot.send_message(chat_id,
                                 msg["mes3"][language].format(name=name))
                bot.send_message(chat_id, msg["mes1"][language])
            else:
                bot.send_message(chat_id, "К сожелению введенный вами\
                 язык не поддерщивается")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send welcome message after add bot t0 chat.

    :param message: telebot message object
    :return: void
    """
    bot.send_message(message.from_user.id, "Hi, I'm very glad to see you!!!")
    bot.send_message(message.from_user.id, "Please set your language: \
     /init UA or /init RU")
    bot.send_message(message.from_user.id, desc, parse_mode="HTML")


@bot.message_handler(commands=['help'])
def send_help(message):
    """Send message with command list and short guideline.

    :param message: telebot message object
    :return: void
    """
    bot.send_message(message.from_user.id, desc, parse_mode="HTML")


@bot.message_handler(commands=['changelanguage'])
def change_language(message):
    """Change messages language UA or RU.

    :param message: telebot message object
    :return: void
    """
    chat_id = message.from_user.id
    query = Query()
    if query.check_user(chat_id):
        lang = extract_arg(message.text)
        if not lang:
            bot.send_message(chat_id, "Выберите оин из предложеных языков переводов \
            и установите как первый параметр после функции `/changelanguage \
            UA` или `/changelanguage RU`.")
        else:
            if lang[0].upper() in c.languages:
                language = lang[0].upper()
                query.change_user_lang(chat_id, language)
                bot.send_message(chat_id, msg["mes10"][language])


@bot.message_handler(commands=['freeze'])
def freeze(message):
    """Disable auto sending words for translation.

    :param message: telebot message object
    :return: void
    """
    chat_id = message.from_user.id
    query = Query()
    if query.check_user(chat_id):
        user = query.get_user_by_id(chat_id)
        query.change_user_status(chat_id, 0)
        bot.send_message(chat_id, msg["mes8"][user['lang']])


@bot.message_handler(commands=['unfreeze'])
def unfreeze(message):
    """Enable auto sending words for translation.

    :param message: telebot message object
    :return: void
    """
    chat_id = message.from_user.id
    query = Query()
    if query.check_user(chat_id):
        user = query.get_user_by_id(chat_id)
        query.change_user_status(chat_id, 1)
        query.change_carma(chat_id, True)
        bot.send_message(chat_id, msg["mes9"][user['lang']])


@bot.message_handler(commands=['next'])
def handle_next(message):
    """Trigger sending words for translation.

    :param message: telebot message object
    :return: void
    """
    chat_id = message.from_user.id
    query = Query()
    if query.check_user(chat_id):
        user = query.get_user_by_id(chat_id)
        if user['w_id'] is not None:
            query.update_user_word(
                user['w_id'],
                chat_id,
                False
            )
            query.set_word_id(
                {
                    "w_id": None,
                    "id": chat_id,
                    "time": user['send_time']
                }
            )
        result = get_new_exercise(chat_id)
        if result is False:
            bot.send_message(chat_id, msg["mes6"][user['lang']])
        else:
            translations = str_to_list(result['t_' + user['lang'].lower()])
            bot.send_message(chat_id, get_random(
                msg["mes5"][user['lang']]).format(
                    word=get_random(translations)), parse_mode="HTML")
            hint = result['hint_' + user['lang'].lower()]
            if hint is not None:
                bot.send_message(chat_id, get_random(
                    msg["mes11"][user['lang']]).format(
                        hint=hint), parse_mode="HTML")


@bot.message_handler(commands=['score'])
def handle_score(message):
    """Return score table.

    :param message: telebot message object
    :return: void
    """
    chat_id = message.from_user.id
    query = Query()
    if query.check_user(chat_id):
        result = query.get_score()
        table = "<b> SCORE LIST: </b> \n"
        for i in result:
            table += "<b>" + i['nickname'] + "</b>" + " : "\
             + "<i>" + str(i['score']) + "</i>" + "\n"
        bot.send_message(chat_id, table, parse_mode="HTML")
    else:
        pass


@bot.message_handler(content_types=['text'])
def handle_message(message):
    """Check get words and send answer.

    :param message: telebot message object
    :return: void
    """
    chat_id = message.from_user.id
    query = Query()
    if query.check_user(chat_id):
        user = query.get_user_by_id(chat_id)
        result = query.get_answer(chat_id)
        if result['answer'] is None:
            bot.reply_to(message, get_random(msg["mes4"][user['lang']]))
        else:
            get_answer = extract_answer(message.text)
            if not get_answer:
                pass
            else:
                if get_answer.lower() == result['answer'].lower():
                    query.update_user_word(
                        user['w_id'],
                        chat_id,
                        True
                    )
                    query.set_word_id(
                        {
                            "w_id": None,
                            "id": chat_id,
                            "time": user['send_time']
                        }
                    )
                    bot.send_sticker(
                        message.from_user.id, get_random(stk["YES"]))
                else:
                    query.update_user_word(
                        user['w_id'],
                        chat_id,
                        False
                    )
                    query.set_word_id(
                        {
                            "w_id": None,
                            "id": chat_id,
                            "time": user['send_time']
                        }
                    )
                    bot.send_sticker(
                        message.from_user.id, get_random(stk["NO"]))
                    bot.send_message(chat_id, msg["mes7"][user['lang']].format(
                        word=result['answer']), parse_mode="HTML")
    else:
        pass


"""
@bot.message_handler(content_types=['sticker'])
def handle_sticers(message):
    print(message.sticker.file_id)
"""
bot.polling(none_stop=True, timeout=60)
