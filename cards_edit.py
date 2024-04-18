from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
import time

from database import USER_ID, USERNAME, HASHED_PASSWORD

# from database import cursor, connection

router = APIRouter()


class Deck(BaseModel):
    deck_id: int


@router.get("/decks/{deck_id}/get_all")
def get_all_cards(request: Request, deck_id: int):
    print("Trying", deck_id)

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM cards WHERE deck_id = ?;",
            (deck_id,),
        )
        connection.commit()

        cards = []

        for card in cursor.fetchall():
            cards.append({})
            print(card)

    return
