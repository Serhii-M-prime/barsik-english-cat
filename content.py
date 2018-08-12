Messages = {
    "mes1" : {"UA": "Авторизація успішно завершена!", 'RU': "Авторизация успешно завершена!"},
    "mes2" : {"UA": "Привіт, {name}, я впізнав тебе!", "RU": "Привет, {name}, я узнал тебя!"},
    "mes3" : {"UA": "Ласкаво просиом {name}!", 'RU': "Добро пожаловать, {name}!"},
    "mes4" : {
        "UA": [
                "Я не надсилав тобі слів для перекладу.",
                "Зайнятися нічим?",
                "Перестань мене спамити! будь ласка..."
        ], 
        'RU': [
                "Я не присылал тебе слов для перевода.",
                "Заняться нечем??",
                "Перестань меня спамить! пожалуйста..."
        ]
            },
    "mes5" : {
        "UA": [
            "Будь ласка, надішли мені переклад слова: <b>{word}</b>.",
            "A слабо перекласти слово: <b>{word}</b>?",
            "Терміново потрібен переклад слова: <b>{word}</b>!",
            "Зможеш перекласти слово: <b>{word}</b>?",
            "Як перекладаэться - <b>{word}</b>?"
            ], 
        "RU": [
            "Пожалуйста, пришли мне перевод слова : <b>{word}</b>",
            "A слабо перевести слово: <b>{word}</b>?",
            "Срочно нужен перевод слова: <b>{word}</b>!",
            "Сможеш перевести слово: <b>{word}</b>?",
            "Как переводится - <b>{word}</b>?"
            ]
        },
    "mes6" : {"UA": "Нові слова в мене закінчилися, а час повторення вивчених ще не настав.", 'RU': "Новые слова у меня закончились, а время для повторения уже изученых слов еще не пришло."},
    "mes7" : {"UA": "Правильна відповідь: <b>{word}</b>.", "RU": "Правильный ответ: <b>{word}</b>"},
    "mes8" : {"UA": "Автоматичне надсилання слів зупинено.", "RU": "Автоматическая отправка слов остановлена."},
    "mes9" : {"UA": "Автоматичне надсилання слів відновлено.", "RU": "Автоматическая отправка слов возобновлена."},
    "mes10" : {"UA": "Мову змінено на - Українська (UA).", "RU": "Язык изменен на - Русский (RU)."},
}

Stikers = {
    "YES" : [
        "CAADAgADhgMAAj-VzAo8Ur__-tLSYgI",
        "CAADAgADNgEAAhhC7gjcYoKhc99L3wI",
        "CAADAgADTAAD-Aq8AuHximoRBM2XAg",
        "CAADAgADIwUAAmvEygo-j5mUmik0PwI",
        "CAADAgADpAADECECEGmJSvZcIbeQAg",
        "CAADAgADMAYAAnlc4gkI_1e-rxbbiAI",
        "CAADAgAD1gADeVziCeucH9_LmUM5Ag",
        "CAADBAADUQQAAv4zDQYszxgfRwSOmwI",
        "CAADAgADuwEAAo5EEQLiw0dW3krAZAI",
        "CAADAgADlQMAAj-VzArcHCfuuKddegI"
    ],
    "NO" : [
        "CAADAgADqgADECECEDKjn_RjTxUSAg",
        "CAADBAADxgMAAv4zDQY6bEeD67rtlAI",
        "CAADAgADJQEAAjbsGwX1CuOrgYRKAAEC",
        "CAADAgADCgMAAnlc4gnVUlRMXAeZZAI",
        "CAADAgADvwEAAo5EEQLHhmdDoeGHSgI",
        "CAADAgADmAMAAj-VzAoDIks1GjBghAI",
        "CAADAgADTgEAAhhC7giduMHmD4TX2wI",
        "CAADAgADQgAD-Aq8ArQZxZTephsVAg",
        "CAADAgADvwkAAvFCvwXG8S9ISr5BJAI",
        "CAADAgADTgEAAhhC7giduMHmD4TX2wICAADAgADIgIAAjbsGwXVUP0CFkcplgI",
        "CAADAgADuAEAAo5EEQJ_5tCJee1YugI"
    ]
}

desc = "\
<b>COMAND LIST:</b> \n\
/init - add new player \n\
/start - return commnad list \n\
/help - return command list \n\
/next - return next word to translation \n\
/score - return score table \n\
/freeze - stop automatic send word for translation \n\
/unfreeze - start automatic send word for translation \n\
/changelanguage - change chat language \n\
<b>GENERAL RULE:</b>\n\
Каждое правильно переведенное слово +1 бал, каждое пропущеное или не переведенное слов -1 бал.\
"