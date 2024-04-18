from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
import bcrypt

from database import USER_ID, USERNAME, HASHED_PASSWORD

from main import SECRET_KEY

# from database import cursor, connection

router = APIRouter()


class User(BaseModel):
    username: str
    password: str


def hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


@router.post("/register")
def register(request: Request, user: User):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    info = cursor.execute(
        "SELECT * FROM users WHERE username = ?", (user.username,)
    ).fetchone()

    if info is not None:
        return {"Failed to create account" : "Username already in use"}

    hashed_password = hash(user.password)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?);",
        (user.username, hashed_password),
    )
    connection.commit()
    request.session["user_id"] = cursor.lastrowid
    connection.close()
    return {"user_id": request.session["user_id"]}


@router.post("/login")
def login(request: Request, user: User):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    info = cursor.execute(
        "SELECT * FROM users WHERE username = ?", (user.username,)
    ).fetchone()
    connection.commit()

    if info is None:
        return {"Incorrect Credentials": "Wrong password or username"}

    hashed_password = info[HASHED_PASSWORD]

    user_id = None
    if bcrypt.checkpw(user.password.encode("utf-8"), hashed_password.encode("utf-8")):
        user_id = info[USER_ID]
    else:
        return {"Incorrect Credentials": "Wrong password or username"}

    request.session["user_id"] = user_id
    connection.close()
    return {"user_id": request.session["user_id"]}
