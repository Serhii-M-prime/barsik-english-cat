import os


# telegram API bot token
TOKEN = os.environ.get('TOKEN', None)

# db connections

DB_USERNAME = os.environ.get('DB_USERNAME', None)
DB_PASSWORD = os.environ.get('DB_PASSWORD', None)
DB_HOST = os.environ.get('DB_HOST', None)
DB_NAME = os.environ.get('DB_NAME', None)

# bot configuration

# time to repeat word in hours
resend_time = 60
# Word learned score constant
word_score = 5
# Time after freeze in days
carma = 5

# supported languages
languages = ['UA', 'RU']