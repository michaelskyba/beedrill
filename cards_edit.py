from openai import OpenAI
from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
import time
import json

from config import OPENAI_API_KEY

from database import USER_ID, USERNAME, HASHED_PASSWORD

# from database import cursor, connection

router = APIRouter()

oai_client = OpenAI(api_key=OPENAI_API_KEY)


class Deck(BaseModel):
    deck_id: int


class Topic(BaseModel):
    deck_id: int
    topic: str


class Card(BaseModel):
    front: str
    back: str


def get_cards(topic):
    response = oai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": 'You are a helpful flashcard creator designed to output flashcards in JSON. Output cards in the format {"flashcards": [{"front": "front of flashcard", "back": "back of flashcard"}]}',
            },
            {"role": "user", "content": f"Create 5-10 flashcards about {topic}."},
        ],
    )
    cards = json.loads(response.choices[0].message.content).get("flashcards")

    if not cards:
        return [{"front": "Error", "back": ""}]

    return cards


@router.get("/decks/{deck_id}/get_all")
def get_all_cards(request: Request, deck_id: int):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM cards WHERE deck_id = ?;",
            (deck_id,),
        )
        connection.commit()

        json = []
        for card in cursor.fetchall():
            front = card[2]
            back = card[3]
            card_id = card[0]
            json.append({"front": front, "back": back, "card_id": card_id})

        return json


@router.delete("/cards/{card_id}/delete")
def delete_card(request: Request, card_id: int):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM cards WHERE card_id = ?;",
            (card_id,),
        )
        connection.commit()
        return {"card_id": card_id}


@router.post("/cards/generate")
def generate_cards(request: Request, topic: Topic):
    deck_id = topic.deck_id
    cards = get_cards(topic.topic)

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        current_time = int(time.time()) - 60 * 60 * 24

        for card in cards:
            cursor.execute(
                "INSERT INTO cards (deck_id, front, back, repetition_number, easiness_factor, repetition_interval, last_review) VALUES (?, ?, ?, ?, ?, ?, ?);",
                (
                    deck_id,
                    card["front"],
                    card["back"],
                    0,
                    2.5,
                    0,
                    current_time,
                ),
            )

        connection.commit()

    return {"topic": topic.topic}
