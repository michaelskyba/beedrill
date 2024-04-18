from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3

# from database import cursor, connection

router = APIRouter()

@router.get("/decks/get/public")
def get_public_decks():
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        public_decks = cursor.execute(
            "SELECT * FROM decks WHERE public = 1"
        ).fetchall()

        json = []
        for deck in public_decks:
            deck_id = deck[0]
            user_id = deck[1]
            deck_name = deck[2]

            card_count = len(cursor.execute("SELECT * FROM cards WHERE deck_id = ?;", (deck_id,)).fetchall())
            author = cursor.execute("SELECT username FROM users WHERE user_id = ?;", (user_id,)).fetchone()[0]

            json.append({"author": author, "deck_name":deck_name, "card_count": card_count, "deck_id": deck_id })
        return json






# @router.post("/clone/{deck_id}")
# def clone(request: Request, deck_id: int):
#     with sqlite3.connect("database.db") as connection:
#         cursor = connection.cursor()

#         info = cursor.execute(
#             "SELECT * FROM users WHERE username = ?", (user.username,)
#         ).fetchone()