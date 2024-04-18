from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
import time
from cards import populate_due_cards

from database import USER_ID, USERNAME, HASHED_PASSWORD

# from database import cursor, connection

router = APIRouter()


class Deck(BaseModel):
    name: str
    public: int


class DeckId(BaseModel):
    deck_id: int


class Card(BaseModel):
    front: str
    back: str


class DeckAdd(BaseModel):
    deck_id: int
    front: str
    back: str


class Grade(BaseModel):
    grade: int


@router.post("/decks/new")
def new_deck(request: Request, deck: Deck):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        user_id = 1
        if not user_id:
            return {"message": "Not logged in"}

        cursor.execute(
            "INSERT INTO decks (user_id, deck_name, public) VALUES (?, ?, ?);",
            (user_id, deck.name, deck.public),
        )
        connection.commit()

        return {"deck_id": cursor.lastrowid}


@router.get("/decks/get/mine")
def get_personal_deck(request: Request):
    print("Very initial", request.session.get("due_cards"))
    decks_due_cards = populate_due_cards(request)
    print("Final", decks_due_cards)

    # json = []
    # for deck_due_card in decks_due_cards:
    #     card_id = deck_due_card[0]
    #     front = deck_due_card[2]
    #     back = deck_due_card[3]
    #     return {
    #         "card_id": card_id,
    #         "front": front,
    #         "back": back,
    #         "due_card_count": len(deck_due_card),
    #     }

    # return json


@router.post("/decks/delete")
def delete_deck(deck_id: DeckId):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM cards WHERE deck_id = ?;", (deck_id.deck_id,))
        cursor.execute("DELETE FROM decks WHERE deck_id = ?;", (deck_id.deck_id,))
        connection.commit()

    return {"deck_id": deck_id.deck_id}
