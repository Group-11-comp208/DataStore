#Chat(chatID*, blackListed, userID);
#User(userID*, preferences, blocked);
#Crypto(name*, price, time, articleRanking);

#"cryptoDB.db"

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
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
    
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def main():
    database = r"C:\Users\Ollye\OneDrive\Desktop\sqlite\db\cryptoDB.db"
    
    sql_create_user_table = """CREATE TABLE IF NOT EXISTS user (
                                    userID integer PRIMARY KEY,
                                    preferences String,
                                    blocked boolean NOT NULL
                                );"""
                                
    sql_create_chat_table = """ CREATE TABLE IF NOT EXISTS chat (
                                        chatID integer PRIMARY KEY,
                                        blacklisted boolean NOT NULL,
                                        userID integer NOT NULL,
                                        FOREIGN KEY (userID) REFERENCES user (userID)
                                    ); """
    
    sql_create_crypto_table = """CREATE TABLE IF NOT EXISTS crypto (
                                    name string PRIMARY KEY,
                                    price float NOT NULL,
                                    time date NOT NULL,
                                    articleRanking [String]
                                );"""
    
    #create a database connection    
    conn = create_connection(database)
    
    #create tables
    if conn is not None:
        #create user table
        create_table(conn, sql_create_user_table)
        
        #create chat table
        create_table(conn, sql_create_chat_table)
        
        #create crypto table
        create_table(conn, sql_create_crypto_table)
    else:
        print("Error! cannot create the database connection.")   

if __name__ == '__main__':
    main()