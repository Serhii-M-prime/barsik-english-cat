"""Module with all needed for works with db.

Class:
SQL - contain methods for db connections and send base queries.
Queries - contain all sql request for telegram bot.
"""
import time
import core.config as c
import mysql.connector as mysql


class SQL:
    """MySQL connector.

    Class for initialize and close data base connection and get methods for
    insert and select data to data base.

    Methods:
        select: Create read query.
        insert: Create write query.

    """

    def __init__(self):
        """Set connection parameters."""
        self.db = mysql.connect(
            host=c.DB_HOST,
            user=c.DB_USERNAME,
            passwd=c.DB_PASSWORD,
            database=c.DB_NAME
            )

    def __del__(self):
        """Close MySql connection anter deleting exemplar."""
        self.db.close()

    def select(self, sql, bind):
        """Create read query.

        :param sql: sql query.
        :param bind: parameters for bind to sql query.
        :return: array with query result.
        """
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(sql, bind)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert(self, sql, bind):
        """Create write query.

        :param sql: sql query.
        :param bind: parameters for bind to sql query.
        :return: array with query result.
        """
        cursor = self.db.cursor()
        cursor.execute(sql, bind)
        self.db.commit()
        cursor.close()
        return


class Queries(SQL):
    """Queries for telegram bot.

        Class with all queries for telegram bot.

        Methods:
            get_users_list: Get list with active users.
            set_word_id: Set asked word id to user.
            get_words_list: Return list with user's words.
            get_answer: Return info about word by id.
            change_user_status: Set user active status.
            add_user: Set new user to db.
            set_user_word: Set asked word id to user row.
            update_user_word: Set new word id to user without answer.
            update_last_ask: Update asked word state.
            change_carma: Set carma value to user.
            check_user: Check user exist in table.
            get_user_by_id: Return user data by id.
            get_score: Get users score table.
            change_user_lang: Set user's language.
        """

    def get_users_list(self):
        """Get list with active users.

        Get list with all active users with good carma
        and which answered to previous question.
        :return: array with list with results
        """
        sql = """
            SELECT
            id,
            lang
            FROM users
            WHERE is_active = %(id)s
            AND w_id IS NULL
            AND carma <= %(carma)s
            """
        bind = {
            'id': 1,
            'carma': c.carma
            }
        result = self.select(sql, bind)
        return result

    def set_word_id(self, data):
        """Set asked word id to user.

        :param data: int
        :return: void
        """
        sql = """
            UPDATE users
            SET w_id = %(w_id)s, send_time = %(time)s
            WHERE id = %(id)s
            """
        self.insert(sql, data)

    def get_words_list(self, user_id):
        """Return list with user's words.

        :param user_id: int
        :return: list
        """
        sql = """
        SELECT
        words.id,
        words.t_ua,
        words.t_ru,
        words.hint_ua,
        words.hint_ru,
        users.id as flag
        FROM words
        LEFT JOIN (SELECT * FROM users_worlds where user_id = %(user_id)s)
        as one_user ON one_user.world_id = words.id
        LEFT JOIN users ON one_user.user_id = users.id
        WHERE (user_id = %(user_id)s AND one_user.score < %(word_score)s
        AND (date_add(last_ask, INTERVAL 24 HOUR) < current_timestamp()
        OR last_ask is null ))
        OR (user_id is null)
        """
        data = dict()
        data['word_score'] = c.word_score
        data['user_id'] = user_id
        result = self.select(sql, data)
        return result 
    
    def get_answer(self, word_id):
        """Return info about word by id.

        :param word_id: int
        :return: dict
        """
        sql = """
        SELECT
        words.en as answer,
        users.w_id as w_id 
        FROM users
        LEFT JOIN words ON users.w_id = words.id
        WHERE users.id = %(id)s
        """
        bind = {'id': word_id}
        result = self.select(sql, bind)
        return result[0]

    def change_user_status(self, user_id, status):
        """Set user active status.

        :param user_id: int
        :param status: int (1||0)
        :return: void
        """
        sql = """
        UPDATE users
        SET is_active = %(status)s
        WHERE id = %(id)s
        """
        bind = {
            "status": status,
            "id": user_id
        }
        self.insert(sql, bind)

    def add_user(self, data):
        """Set new user to db.

        :param data: dict
        :return: void
        """
        sql = """
        INSERT INTO users (id, nickname, lang, is_active, carma)
        VALUES (%(id)s, %(nickname)s, %(lang)s, %(is_active)s, %(carma)s);
        """
        bind = {
            "nickname": data['nickname'],
            "id": data['id'],
            "lang": data['lang'],
            "is_active": 1,
            "carma": 0,
        }
        self.insert(sql, bind)

    def set_user_word(self, user_id, world_id):
        """Set asked word id to user row.

        :param user_id:
        :param world_id:
        :return: void
        """
        sql = """
        INSERT INTO users_worlds (user_id, world_id, score, last_ask)
        VALUES (%(user_id)s, %(world_id)s, %(score)s, %(last_ask)s);
        """
        bind = {
            "user_id": user_id,
            "world_id": world_id,
            "score": 0,
            "last_ask": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.insert(sql, bind)
    
    def update_user_word(self, world_id, user_id, score: bool):
        """Set new word id to user without answer.

        :param world_id: int
        :param user_id: int
        :param score: bool
        :return: void
        """
        if score:
            condition = "SET score = score + 1"
        else:
            condition = "SET score = score - 1"

        sql = "UPDATE users_worlds " + condition + "\
        WHERE world_id = %(world_id)s AND user_id = %(user_id)s"
        bind = {
            "world_id": world_id,
            "user_id": user_id
        }
        self.insert(sql, bind)

    def update_last_ask(self, user_id, world_id):
        """Update asked word state.

        :param user_id: int
        :param world_id: int
        :return: void
        """
        sql = """
            UPDATE users_worlds
            SET last_ask = %(last_ask)s
            WHERE world_id = %(world_id)s 
            AND user_id = %(user_id)s
            """
        bind = {
            "world_id": world_id,
            "user_id": user_id,
            "last_ask": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.insert(sql, bind)
    
    def change_carma(self, user_id: int, carma: bool):
        """Set carma value to user.

        :param user_id: int
        :param carma: bool
        :return: void
        """
        if carma is True:
            condition = "SET carma = 0"
        else:
            condition = "SET carma = carma + 1"

        sql = "UPDATE users " + condition + " WHERE id = %(id)s"
        bind = {
            "id": user_id
        }
        self.insert(sql, bind)
    
    def check_user(self, user_id):
        """Check user exist in table.

        :param user_id: int
        :return: bool
        """
        sql = """
        SELECT
        *
        FROM users
        WHERE id = %(id)s
        """
        bind = {
            'id': user_id
        }
        result = self.select(sql, bind)

        if not result:
            response = False
        else:
            response = True

        return response

    def get_user_by_id(self, user_id):
        """Return user data by id.

        :param user_id: int
        :return: dict
        """
        sql = """
            SELECT
            *
            FROM users
            WHERE id = %(id)s
            """
        bind = {
            'id': user_id
            }
        result = self.select(sql, bind)
        return result[0]

    def get_score(self):
        """Get users score table.

        :return: list
        """
        sql = """
        SELECT users.nickname, SUM(users_worlds.score) as score FROM users_worlds
        LEFT JOIN users ON users_worlds.user_id = users.id
        GROUP BY users_worlds.user_id
        ORDER BY score DESC
        """
        bind = {}
        result = self.select(sql, bind)
        return result

    def change_user_lang(self, user_id, lang):
        """Set user's language.

        :param user_id:
        :param lang:
        :return: void
        """
        sql = """
        UPDATE users
        SET lang = %(lang)s
        WHERE id = %(id)s
        """
        bind = {
            "lang": lang,
            "id": user_id
        }
        self.insert(sql, bind)
