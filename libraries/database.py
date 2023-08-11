"""
Author: Kent
Name:   database.py
Function
    Class for database transaction handling
    Supported database
        1. PostgreSQL
        2. SQLite3
"""
import os.path
import psycopg2
import sqlite3

# response codes
SUCCESS = 1
FAILURE = 0

# Class for handling DB transactions to a PostgreSQL
class PostgreSQL:

    def __init__(self, db_config):
        self.__dbconfig = db_config

    def __connect(self):
        try:
            conn = psycopg2.connect(**self.__dbconfig)

            return conn
        except ConnectionError as e:
            return FAILURE

    def execute_query(self, sql, return_one=False):
        conn = self.__connect()
        if conn == FAILURE:
            ret = [FAILURE, ()]
        else:
            cur = conn.cursor()
            cur.execute(sql)

            if return_one:
                ret = [SUCCESS, cur.fetchone()]
            else:
                ret = [SUCCESS, cur.fetchall()]
            conn.close()
        return ret

    def execute_dml(self, sql):
        conn = self.__connect()
        if conn == FAILURE:
            return FAILURE
        else:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
            return SUCCESS


# Class for handling DB transactions to a SQLite3
class SQLite:
    def __init__(self, db_file, db_init_script=""):
        self.__database = db_file
        self.__db_init_script = db_init_script


    def __create_or_open_db(self, db_file):
        if not os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            conn.execute(self.__db_init_script)
        else:
            conn = sqlite3.connect(db_file)

        return conn


    def execute_query(self, sql, return_one=False):
        conn = self.__create_or_open_db(self.__database)
        cur = conn.cursor()
        cur.execute(sql)

        if return_one:
            return [SUCCESS, cur.fetchone()]
        else:
            return [SUCCESS, cur.fetchall()]


    def execute_dml(self, sql):
        conn = self.__create_or_open_db(self.__database)
        conn.execute(sql)
        conn.commit()
        return SUCCESS


if __name__ == "__main__":
    print("database.py version 1.0.0")
