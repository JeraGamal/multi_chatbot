from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Chatbot, SessionLocal
from app.routes.auth import get_db

router = APIRouter()

@router.post("/")
async def create_chatbot(name: str, description: str, owner_id: int, db: Session = Depends(get_db)):
    chatbot = Chatbot(name=name, description=description, owner_id=owner_id)
    db.add(chatbot)
    db.commit()
    return {"message": "Chatbot created successfully"}

@router.get("/")
async def list_chatbots(owner_id: int, db: Session = Depends(get_db)):
    chatbots = db.query(Chatbot).filter(Chatbot.owner_id == owner_id).all()
    return chatbots

