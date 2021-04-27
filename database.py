import sqlite3
from sqlite3 import Error
import sys
sys.path.insert(1, '/home/ethanh/Desktop/twitter_rank')
import ranking_algorithm
import time
class Database:
    def __init__(self, path):
        database = path
        sql_create_chat_table = """CREATE TABLE IF NOT EXISTS Chat (
                                            chatID integer PRIMARY KEY,
                                            blacklisted boolean NOT NULL,
                                            preferences TEXT
                                        );"""
        sql_create_crypto_table = """CREATE TABLE IF NOT EXISTS CryptoCurrency (
                                        name TEXT PRIMARY KEY,
                                        price float NOT NULL,
                                        time date NOT NULL,
                                        articleRanking TEXT
                                    );"""

        # create a database connection
        self.conn = self.create_connection(database)

        # create tables
        if self.conn is not None:

            self.create_table(sql_create_chat_table)
            self.create_table(sql_create_crypto_table)

        else:
            print("Error! cannot create the database connection.")

    def create_connection(self, db_file):
        """create a database connection to the SQLite database
        specified by the db_file
        :param db_file: database file
        :return: Connection object or None"""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection objectpath"""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            c.close()
        except Error as e:
            print(e)

    def insert_chat(self, chatID, blacklisted, preferences=""):
        params = [chatID, blacklisted, preferences]
        try:
            insert_query = "INSERT INTO Chat (chatID,blacklisted,preferences) VALUES(?,?,?)"
            self._insert(insert_query, params)
        except Error as e:
            print(e)

    def _insert(self, insert_query, params):
        cur = self.conn.cursor()
        cur.execute(insert_query, params)
        self.conn.commit()
        cur.close()

    def _fetch(self, fetch_query, params=None):
        cur = self.conn.cursor()

        if params == None:
            cur.execute(fetch_query)
        else:
            cur.execute(fetch_query, params)

        rows = cur.fetchall()
        cur.close()
        return rows

    def _to_string(self, arr):
        return ",".join("'{}'".format(elem) for elem in arr)

    def _from_string(self, raw):
        return raw.split("','")

    def get_price(self, name):
        rows = self._fetch(
            "SELECT price FROM CryptoCurrency WHERE name=?", (name,))
        return rows[0][0]

    def get_article(self, name):
        rows = self._fetch(
            "SELECT articleRanking FROM CryptoCurrency WHERE name=?", (name,))
        return self._from_string(rows[0][0])

    def get_all_cyrpto_currencies(self):
        rows = self._fetch("SELECT name FROM CryptoCurrency")
        return rows

    def update_articles(self, name, articles_list):
        articles = self._to_string(articles_list)
        update_params = [articles, name]
        try:
            update_query = "UPDATE CryptoCurrency SET articleRanking = ? WHERE name=?"
            self._insert(update_query, update_params)
        except Error as e:
            print(e)

    def update_or_insert_crypto(self, name, price, time, articleRanking=""):
        data = self._fetch(
            "SELECT name FROM CryptoCurrency WHERE name=?", (name,))

        if len(data) == 0:
            params = [name, price, time, articleRanking]
            try:
                insert_query = "INSERT INTO CryptoCurrency (name,price,time,articleRanking) VALUES(?,?,?,?)"
                self._insert(insert_query, params)
            except Error as e:
                print(e)
        else:
            update_params = [price, name]
            try:
                update_query = "UPDATE CryptoCurrency SET price = ? WHERE name=?"
                self._insert(update_query, update_params)
            except Error as e:
                print(e)


"""database = Database("cryptoDB.db")
fetch = ranking_algorithm.NewsFetch()

coins = database.get_all_cyrpto_currencies()

for coin in coins:
    name = coin[0]
    articles = fetch.get_articles(name)
    database.update_articles(name, articles)
    print("Updating news for {}".format(name))
    time.sleep(1)"""