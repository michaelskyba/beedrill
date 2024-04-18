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

# def is_due(repetition_number, easiness_factor, repetition_interval, last_review):



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

        cursor.execute("SELECT * FROM cards WHERE deck_ud = ?;" (deck_id,))
        cards = cursor.fetchall()

        due_cards = list(filter(is_due,cards))


        json.append({"deck_id": deck_id, "deck_name": deck_name})

    connection.commit()

    connection.close()

    return json


@router.post("/decks/delate")
def delate_deck(deck_id: DeckId):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM cards WHERE deck_id = ?;", (deck_id.deck_id,))
    cursor.execute("DELETE FROM decks WHERE deck_id = ?;", (deck_id.deck_id,))
    connection.commit()

    connection.close()

    return {"deck_id": deck_id.deck_id}


@router.post("/cards/add")
def add_card(request: Request, deck_id: DeckId, card: Card):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    current_time = int(time.time())

    cursor.execute(
        "INSERT INTO cards (deck_id, front, back, repetition_number, easiness_factor, repetition_interval, last_review) VALUES (?, ?, ?, ?, ?, ?);",
        deck_id.deck_id,
        card.front,
        card.back,
        0,
        2.5,
        0,
        current_time,
    )

    connection.commit()

    connection.close()

# @router.get("/cards/review")
# def review_card(request: Request, deck_id: DeckId, grade: Grade):
#     pass


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
    easiness_factor = easiness_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
    if easiness_factor < 1.3:
        easiness_factor = 1.3

    return (repetition_number, easiness_factor, repetition_interval)
        
            


