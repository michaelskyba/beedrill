from config import OPENAI_API_KEY, SECRET_KEY

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware

import users

import database

database.create_user_table()

app = FastAPI()

app.add_middleware(
    SessionMiddleware, secret_key=SECRET_KEY
)

# Route user sign up and login
app.include_router(users.router)

# Route static files

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/src", StaticFiles(directory="src"), name="src")

# Route index.html


@app.get("/")
def index_html():
    return FileResponse("index.html")
