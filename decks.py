from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
import bcrypt

from database import USER_ID, USERNAME, HASHED_PASSWORD

# from database import cursor, connection

router = APIRouter()


class Deck(BaseModel):
    name: str
    public: int


class DeckId(BaseModel):
    deck_id: int


@router.post("/decks/new")
def new_deck(request: Request, deck: Deck):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    user_id = request.session.get("user_id")

    cursor.execute(
        "INSERT INTO decks (user_id, deck_name, public) VALUES (?, ?, ?);",
        (user_id, deck.name, deck.public),
    )
    connection.commit()

    connection.close()

    return {"deck_id": cursor.lastrowid}


@router.get("/decks/get/mine")
def get_personal_deck(request: Request):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    user_id = request.session.get("user_id")

    cursor.execute("SELECT * FROM decks WHERE user_id = ?;", (user_id,))
    decks = cursor.fetchall()

    json = []
    for deck in decks:
        deck_id = deck[0]
        deck_name = deck[2]
        json.append({"deck_id": deck_id, "deck_name": deck_name})

    connection.commit()

    connection.close()

    return json


@router.post("/decks/delate")
def delete_deck(deck_id: DeckId):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM cards WHERE deck_id = ?;", (deck_id.deck_id,))
    cursor.execute("DELETE FROM decks WHERE deck_id = ?;", (deck_id.deck_id,))
    connection.commit()

    connection.close()

    return {"deck_id": deck_id.deck_id}
