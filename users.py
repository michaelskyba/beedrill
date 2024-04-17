from fastapi import APIRouter

from main import SECRET_KEY 
from database import cursor, connection

router = APIRouter()

@router.post("/register")
async def register():
  pass



