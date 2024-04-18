from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
from decks import new_deck
from cards import add_card
import time

router = APIRouter()


@router.get("/decks/get/public")
def get_public_decks():
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        public_decks = cursor.execute("SELECT * FROM decks WHERE public = 1").fetchall()

        json = []
        for deck in public_decks:
            deck_id = deck[0]
            user_id = deck[1]
            deck_name = deck[2]

            card_count = len(
                cursor.execute(
                    "SELECT * FROM cards WHERE deck_id = ?;", (deck_id,)
                ).fetchall()
            )
            author = cursor.execute(
                "SELECT username FROM users WHERE user_id = ?;", (user_id,)
            ).fetchone()[0]

            json.append(
                {
                    "author": author,
                    "deck_name": deck_name,
                    "card_count": card_count,
                    "deck_id": deck_id,
                }
            )
        return json


@router.post("/decks/{deck_id}/clone")
def clone(request: Request, deck_id: int):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        if not request.session.get("user_id"):
            return {"Not logged in eror "}

        user_id = request.session.get("user_id")

        deck_name = cursor.execute(
            "SELECT deck_name FROM decks WHERE deck_id = ?;", (deck_id,)
        ).fetchone()[0]

        cursor.execute(
            "INSERT INTO decks (user_id, deck_name, public) VALUES (?, ?, 0);",
            (
                user_id,
                deck_name,
            ),
        )

        cards = cursor.execute(
            "SELECT * FROM cards WHERE deck_id = ?;", (deck_id,)
        ).fetchall()

        for card in cards:
            front = card[2]
            back = card[3]
            current_time = int(time.time())
            cursor.execute(
                "INSERT INTO cards (deck_id, front, back, repetition_number, easiness_factor, repetition_interval, last_review) VALUES (?, ?, ?, ?, ?, ?, ?);",
                (
                    cursor.lastrowid,
                    front,
                    back,
                    0,
                    2.5,
                    0,
                    current_time,
                ),
            )
            connection.commit()
