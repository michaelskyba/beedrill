from config import OPENAI_API_KEY, SECRET_KEY

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import users

import database
database.create_user_table()

app = FastAPI()

# Route user sign up and login
app.include_router(users.router)

# Route static files

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/src", StaticFiles(directory="src"), name="src")

# Route index.html

@app.get("/")
async def index_html():
  return FileResponse('index.html')
