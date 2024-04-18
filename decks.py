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


@router.post("/new")
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

@router.post("/delate")
def delate_deck(deck_id: DeckId):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()


    cursor.execute("DELETE FROM cards WHERE deck_id = ?;", (deck_id.deck_id,))
    cursor.execute("DELETE FROM decks WHERE deck_id = ?;", (deck_id.deck_id,))
    connection.commit()

    connection.close()

    return {"deck_id": deck_id.deck_id}
