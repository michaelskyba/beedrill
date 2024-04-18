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
    card_id: int
    deck_id: int
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


def populate_due_cards(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return

    # We're storing session["due_cards"] as
    # (str) deck id --> [list of card ids (ints)]
    # FastAPI sessions can't hold int keys or tuples I think

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        decks = cursor.execute(
            "SELECT * FROM decks WHERE user_id = ?;", (user_id,)
        ).fetchall()

        decks_due_cards = request.session.get("due_cards")

        if decks_due_cards is None:
            decks_due_cards = dict()

        for deck in decks:
            deck_id = deck[0]

            if decks_due_cards.get(deck_id):
                continue

            cards = cursor.execute(
                "SELECT * FROM cards WHERE deck_id = ?;", (deck_id,)
            ).fetchall()

            due_cards = []

            for card in cards:
                card_id = card[0]

                current_time = int(time.time())
                repetition_interval = card[6]
                last_review = card[7]
                if repetition_interval < (current_time - last_review) / (60 * 60 * 24):
                    due_cards.append(card_id)

            decks_due_cards[str(deck_id)] = due_cards

        request.session["due_cards"] = decks_due_cards
        return decks_due_cards


@router.get("/decks/{deck_id}/get_next")
def get_next(request: Request, deck_id: int):
    due_cards = request.session.get("due_cards")

    if not due_cards:
        due_cards = populate_due_cards(request)

    if not due_cards:
        return {"due_card_count": 0}

    due_cards = due_cards.get(str(deck_id))
    if not due_cards:
        return {"due_card_count": 0}

    due_card_id = due_cards[0]

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        due_card = cursor.execute(
            "SELECT * FROM cards WHERE card_id= ?;", (due_card_id,)
        ).fetchone()

    return {
        "card_id": due_card_id,
        "front": due_card[2],
        "back": due_card[3],
        "due_card_count": len(due_cards),
    }


@router.post("/cards/review")
def review_card(request: Request, review: Review):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        card_id = review.card_id
        deck_id = review.deck_id
        cursor.execute("SELECT * FROM cards WHERE card_id = ?;", (card_id,))
        connection.commit()
        card = cursor.fetchone()

        correct = review.grade >= 4
        repetition_number = card[4]
        easiness_factor = card[5]
        last_review = card[7]

        due_cards = request.session.get("due_cards")
        deck = due_cards[str(deck_id)]

        if correct:
            deck.pop(0)
        else:
            deck.append(deck.pop(0))

        current_time = int(time.time())
        

        (new_repetition_number, new_easiness_factor, new_repetition_interval) = SM2(
            review.grade, repetition_number, easiness_factor, last_review
        )

        cursor.execute(
            "UPDATE cards SET repetition_number = ?, easiness_factor = ?, repetition_interval = ?, last_review = ?;",
            (
                new_repetition_number,
                new_easiness_factor,
                new_repetition_interval,
                current_time,
            ),
        )

        return {"card_id" : card_id}


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
