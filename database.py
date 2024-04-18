import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()


USER_ID = 0
USERNAME = 1
HASHED_PASSWORD = 2


def create_user_table():
    cursor.execute(
        """
                  CREATE TABLE IF NOT EXISTS users (
                  user_id INTEGER PRIMARY KEY,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL
    )"""
    )
    connection.commit()


def create_deck_table():
    cursor.execute(
        """
                  CREATE TABLE IF NOT EXISTS decks (
                  deck_id INTEGER PRIMARY KEY,
                  user_id INTEGER NOT NULL,
                  deck_name TEXT NOT NULL,
                  public INTEGER NOT NULL
    )"""
    )
    connection.commit()


def create_card_table():
    cursor.execute(
        """
                  CREATE TABLE IF NOT EXISTS decks (
                  card_id INTEGER PRIMARY KEY,
                  deck_id TEXT NOT NULL,
                  front TEXT NOT NULL,
                  back TEXT NOT NULL,
                  repetition_number INTEGER NOT NULL,
                  easiness_factor FLOAT NOT NULL,
                  repetition_interval INTEGER NOT NULL,
                  last_review INTEGER
    )"""
    )
    connection.commit()
