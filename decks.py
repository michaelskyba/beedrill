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


@router.post("/new_deck")
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
