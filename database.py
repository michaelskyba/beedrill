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
                  id INTEGER PRIMARY KEY,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL
  )"""
    )

    connection.commit()
