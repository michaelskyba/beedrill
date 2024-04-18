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

        user_id = request.session.get("user_id")
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
    user_id = request.session.get("user_id")
    if not user_id:
        return {"message": "Not logged in"}

    due_cards = populate_due_cards(request)

    json = []

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        decks = cursor.execute(
            "SELECT * FROM decks WHERE user_id = ?;", (user_id,)
        ).fetchall()

        for deck in decks:
            deck_id = deck[0]
            deck_name = deck[2]
            due_card_count = len(due_cards[str(deck_id)])

            json.append(
                {
                    "deck_id": deck_id,
                    "deck_name": deck_name,
                    "due_card_count": due_card_count,
                }
            )

    return json


@router.post("/decks/delete")
def delete_deck(deck_id: DeckId):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM cards WHERE deck_id = ?;", (deck_id.deck_id,))
        cursor.execute("DELETE FROM decks WHERE deck_id = ?;", (deck_id.deck_id,))
        connection.commit()

    return {"deck_id": deck_id.deck_id}
