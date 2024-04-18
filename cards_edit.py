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
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM cards WHERE deck_id = ?;",
            (deck_id,),
        )
        connection.commit()

        json = []
        for card in cursor.fetchall():
            front = card[2]
            back = card[3]
            card_id = card[0]
            json.append({"front": front, "back": back, "card_id": card_id})

        return json


@router.delete("/cards/{card_id}/delete")
def delete_card(request: Request, card_id: int):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM cards WHERE card_id = ?;",
            (card_id,),
        )
        connection.commit()
        return {"card_id": card_id}
