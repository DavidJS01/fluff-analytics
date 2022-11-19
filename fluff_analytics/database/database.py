import sqlite3
from sqlite3 import Error
from database.queries import CREATE_TABLES, INSERT_MATCH_HISTORY, INSERT_MATCH_DATA


def create_connection(db_file):
    """create a database connection to a SQLite database"""
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        raise e


def setup_tables(conn: sqlite3.Connection):
    try:
        cursor = conn.cursor()
        cursor.executescript(CREATE_TABLES)
    except Exception as e:
        raise e


def get_registered_summoners_puuid(conn: sqlite3.Connection) -> list:
    try:
        cursor = conn.cursor()
        summoners = cursor.execute("SELECT puuid FROM summoners").fetchall()
        return summoners
    except Exception as e:
        raise e


def get_registered_summoners_name(conn: sqlite3.Connection) -> list:
    try:
        cursor = conn.cursor()
        summoners = cursor.execute("SELECT name FROM summoners").fetchall()
        return summoners
    except Exception as e:
        raise e


def insert_game_data(data: tuple, conn: sqlite3.Connection) -> None:
    try:
        cursor = conn.cursor()
        print(data)
        cursor.executemany(INSERT_MATCH_DATA, (data,))
        conn.commit()
    except Exception as e:
        raise e
