from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, Chatbot, User

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def create_chatbot(
    name: str, 
    description: str, 
    owner_id: int, 
    db: Session = Depends(get_db)
):
    # Verify the owner exists
    user = db.query(User).filter(User.id == owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Owner user not found")
    
    # Create new chatbot
    chatbot = Chatbot(
        name=name, 
        description=description, 
        owner_id=owner_id
    )
    
    try:
        db.add(chatbot)
        db.commit()
        db.refresh(chatbot)
        return {
            "message": "Chatbot created successfully", 
            "chatbot_id": chatbot.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating chatbot: {str(e)}")

@router.get("/")
async def list_chatbots(
    owner_id: int, 
    db: Session = Depends(get_db)
):
    # Verify the owner exists
    user = db.query(User).filter(User.id == owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Owner user not found")
    
    # Fetch chatbots for the owner
    chatbots = db.query(Chatbot).filter(Chatbot.owner_id == owner_id).all()
    return chatbots
