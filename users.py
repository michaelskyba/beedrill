from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
import bcrypt

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
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt()
    ).decode()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?);",
        (user.user_name, hashed_password),
    )
    request.session["user_id"] = cursor.lastrowid
    connection.commit()
    connection.close()
    return {"password": hashed_password, "user_id": request.session["user_id"]}
