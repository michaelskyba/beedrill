from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
import time

from database import USER_ID, USERNAME, HASHED_PASSWORD

# from database import cursor, connection

router = APIRouter()


class Card(BaseModel):
    deck_id: int
    front: str
    back: str


class DeckId(BaseModel):
    deck_id: int


class Grade(BaseModel):
    grade: int


class Review(BaseModel):
    deck_id: int
    card_id: int
    grade: int


@router.post("/cards/add")
def add_card(request: Request, deck_id: Card):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        current_time = int(time.time()) - 60 * 60 * 24

        cursor.execute(
            "INSERT INTO cards (deck_id, front, back, repetition_number, easiness_factor, repetition_interval, last_review) VALUES (?, ?, ?, ?, ?, ?, ?);",
            (
                deck_id.deck_id,
                deck_id.front,
                deck_id.back,
                0,
                2.5,
                0,
                current_time,
            ),
        )

        connection.commit()

        return {"card_id": cursor.lastrowid}


@router.get("/cards/get_next")
def get_next(request: Request, deck_id: DeckId):
    due_cards = request.session.get("due_cards")[str(deck_id.deck_id)]
    if len(due_cards) != 0:
        due_card = due_cards[0]
        card_id = due_card[0]
        front = due_card[2]
        back = due_card[3]
        return {
            "card_id": card_id,
            "front": front,
            "back": back,
            "due_card_count": len(due_cards),
        }
    else:
        return {"due_card_count": 0}


@router.get("/cards/review")
def review_card(request: Request, review: Review):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        card_id = review.card_id
        cursor.execute("SELECT * FROM cards WHERE card_id = ?;", (card_id,))
        connection.commit()
        card = cursor.fetchone()
        print(card)


def SM2(grade, repetition_number, easiness_factor, repetition_interval):
    if grade >= 3:
        if repetition_number == 0:
            repetition_interval = 1
        elif repetition_number == 1:
            repetition_interval = 6
        else:
            repetition_interval = round(repetition_interval * easiness_factor)
        repetition_number += 1
    else:
        repetition_number = 0
        repetition_interval = 1
    easiness_factor = easiness_factor + (
        0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02)
    )
    if easiness_factor < 1.3:
        easiness_factor = 1.3

    return (repetition_number, easiness_factor, repetition_interval)
