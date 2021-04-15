import sqlite3
from sqlite3 import Error


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

    def insert_chat(self, chatID, blacklisted, preferences):
        params = [chatID, blacklisted, preferences]
        try:
            insertQuery = "INSERT INTO Chat (chatID,blacklisted,preferences) VALUES(?,?,?)"
            self._insert(insertQuery, params)
        except Error as e:
            print(e)

    def insert_crypto_currency(self, name, price, time, articleRanking):
        params = [name, price, time, articleRanking]
        try:
            insertQuery = "INSERT INTO CryptoCurrency (name,price,time,articleRanking) VALUES(?,?,?,?)"
            self._insert(insertQuery, params)
        except Error as e:
            print(e)

    def _insert(self, insertQuery, params):
        cur = self.conn.cursor()
        cur.execute(insertQuery, params)
        self.conn.commit()
        cur.close()

    def get_price(self, name):
        cur = self.conn.cursor()
        cur.execute("SELECT price FROM CryptoCurrency WHERE name=?", (name,))
        rows = cur.fetchall()
        return rows[0][0]

    def get_all_cyrpto_currencies(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM CryptoCurrency")
        rows = cur.fetchall()

        for row in rows:
            print(row[0])


database = Database("cryptoDB.db")
#database.insertIntoChat(103, False, 'ethan')
#database.insertIntoCrypto("Bitcoin", 10.0, 2021-5-15, "ranking")
#database.insertIntoCrypto("Etherium", 20.0, 2021-6-16, "ranking")
print(database.get_price("Bitcoin"))
database.get_all_cyrpto_currencies()
