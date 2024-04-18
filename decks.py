from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
import time

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
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        user_id = request.session.get("user_id")
        if not user_id:
            return {"message": "Not logged in"}

        cursor.execute("SELECT * FROM decks WHERE user_id = ?;", (user_id,))
        decks = cursor.fetchall()

        json = []
        deck_due_cards = dict()
        for deck in decks:
            deck_id = deck[0]
            deck_name = deck[2]

            cursor.execute("SELECT * FROM cards WHERE deck_id = ?;", (deck_id,))

            cards = cursor.fetchall()

            due_cards = []
            for card in cards:
                current_time = int(time.time())
                repetition_interval = card[6]
                last_review = card[7]
                if repetition_interval < (current_time - last_review) / (60 * 60 * 24):
                    due_cards.append(card)

            deck_due_cards[deck_id] = due_cards

            due_card_count = len(due_cards)
            card_count = len(cards)

            json.append(
                {
                    "deck_id": deck_id,
                    "deck_name": deck_name,
                    "card_count": card_count,
                    "due_card_count": due_card_count,
                }
            )

        request.session["due_cards"] = deck_due_cards

        connection.commit()

        return json


@router.post("/decks/delete")
def delete_deck(deck_id: DeckId):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM cards WHERE deck_id = ?;", (deck_id.deck_id,))
        cursor.execute("DELETE FROM decks WHERE deck_id = ?;", (deck_id.deck_id,))
        connection.commit()

    return {"deck_id": deck_id.deck_id}
