from config import OPENAI_API_KEY, SECRET_KEY

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/src", StaticFiles(directory="src"), name="src")

@app.get("/")
async def index_html():
  return FileResponse('index.html')