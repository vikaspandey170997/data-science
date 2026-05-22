from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db

router = APIRouter()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return {"user": "vikas"}