import sqlite3

connection  = sqlite3.connect('database.db')

cursor = connection.cursor()

def create_user_table():
  cursor.execute('''
                  CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL
  )''')

  connection.commit()




