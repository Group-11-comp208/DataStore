import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, path):
        database = path
        sql_create_chat_table = """ CREATE TABLE IF NOT EXISTS Chat (
                                            chatID integer PRIMARY KEY,
                                            blacklisted boolean NOT NULL,
                                            preferences String
                                        ); """
        sql_create_crypto_table = """CREATE TABLE IF NOT EXISTS CryptoCurrency (
                                        name string PRIMARY KEY,
                                        price float NOT NULL,
                                        time date NOT NULL,
                                        articleRanking String
                                    );"""
        # create a database connection
        conn = self.create_connection(database)

        # create tables
        if conn is not None:

            # create chat table
            self.create_table(conn, sql_create_chat_table)

            # create crypto table
            self.create_table(conn, sql_create_crypto_table)

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

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection objectpath"""
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def insertIntoChat(self, chatID, blacklisted, preferences):
        try:
            insertQuery = """INSERT INTO Chat (chatID,blacklisted,preferences)
                             VALUES({},{},{});""".format(chatID, blacklisted, preferences)
        except Error as e:
            print(e)

        return insertQuery

    def insertIntoCrypto(self, name, price, time, articleRanking):
        try:
            insertQuery = """INSERT INTO CryptoCurrency (name,price,time,articleRanking)
                             VALUES({},{},{},{});""".format(name, price, time, articleRanking)
        except Error as e:
            print(e)

        return insertQuery

    def insert(self, conn, insertQuery):
        cur = conn.cursor()
        cur.execute(insertQuery)
        conn.commit()
        return cur.lastrowid


database = Database("cryptoDB.db")
