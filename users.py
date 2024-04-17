from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3

from main import SECRET_KEY

# from database import cursor, connection

router = APIRouter()


class User(BaseModel):
    user_name: str
    password: str


@router.post("/register")
def register(request: Request, user: User):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?);",
        (user.user_name, user.password),
    )
    request.session["user_id"] = cursor.lastrowid
    connection.commit()
    connection.close()
    return {"user_id": request.session["user_id"]}
