"""Module with all needed for works with db.

Class:
SQL - contain methods for db connections and send base queries.
Queries - contain all sql request for telegram bot.
"""
import time
import config_dev as c
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

    def getUsersList(self):
        """Get list with active users

        ldfm
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

    def setWorldId(self, data):
        sql = """
            UPDATE users
            SET w_id = %(w_id)s, send_time = %(time)s
            WHERE id = %(id)s
            """
        self.insert(sql, data)

    def getWordsList(self, user_id):
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
        data = {}
        data['word_score'] = c.word_score
        data['user_id'] = user_id
        result = self.select(sql, data)
        return result 
    
    def getAnswer(self, id):
        sql = """
        SELECT
        words.en as answer,
        users.w_id as w_id 
        FROM users
        LEFT JOIN words ON users.w_id = words.id
        WHERE users.id = %(id)s
        """
        bind = {'id': id}
        result = self.select(sql, bind)
        return result[0]

    def changeUserStatus(self, id, status):
        sql = """
        UPDATE users
        SET is_active = %(status)s
        WHERE id = %(id)s
        """
        bind = {
            "status": status,
            "id": id
        }
        self.insert(sql, bind)

    def addUser(self, data):
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

    def setUserWord(self, user_id, world_id):
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
    
    def updateUserWord(self, world_id, user_id, score: bool):
        
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

    def updateLastAsk(self, user_id, world_id):
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
    
    def changeCarma(self, id: int, carma: bool):

        if carma is True:
            condition = "SET carma = 0"
        else:
            condition = "SET carma = carma + 1"

        sql = "UPDATE users " + condition + " WHERE id = %(id)s"
        bind = {
            "id": id
        }
        self.insert(sql, bind)
    
    def checkUser(self, user_id):
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

    def getUserById(self, id):
        sql = """
            SELECT
            *
            FROM users
            WHERE id = %(id)s
            """
        bind = {
            'id': id
            }
        result = self.select(sql, bind)
        return result[0]

    def getScore(self):
        sql = """
        SELECT users.nickname, SUM(users_worlds.score) as score FROM users_worlds
        LEFT JOIN users ON users_worlds.user_id = users.id
        GROUP BY users_worlds.user_id
        ORDER BY score DESC
        """
        bind = {}
        result = self.select(sql, bind)
        return result

    def changeUserLang(self, id, lang):
        sql = """
        UPDATE users
        SET lang = %(lang)s
        WHERE id = %(id)s
        """
        bind = {
            "lang": lang,
            "id": id
        }
        self.insert(sql, bind)
