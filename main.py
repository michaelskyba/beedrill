from config import OPENAI_API_KEY, SECRET_KEY

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

import users
import decks

import database

database.create_user_table()
database.create_deck_table()
database.create_card_table()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Avoid CORS errors for fetching
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route user sign up and login
app.include_router(users.router)
app.include_router(decks.router)

# Route static files

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/src", StaticFiles(directory="src"), name="src")
app.mount("/dist", StaticFiles(directory="dist"), name="dist")

# Route index.html


@app.get("/")
async def index():
    return FileResponse("index.html")


@app.get("/prod")
async def production():
    return FileResponse("dist/index.html")
