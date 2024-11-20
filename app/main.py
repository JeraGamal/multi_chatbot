from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
from app.routes import auth, chatbots
from app.database import Base, SessionLocal, engine, create_tables
from app.models import init_db, User, Chatbot, Document
from app.utils import embedding, response

# Create tables
create_tables(engine)

app = FastAPI(title="AI Chatbot Creation Platform")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Document and Embedding Processor
doc_processor = embedding.DocumentProcessor()
response_generator = response.ChatbotResponseGenerator()

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatbots.router, prefix="/chatbots", tags=["Chatbots"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Multi-Chatbot Creation Platform",
        "endpoints": [
            "/auth/register",
            "/auth/login",
            "/chatbots/"
        ]
    }


@app.post("/chatbots/create")
def create_chatbot(
    name: str, 
    description: str, 
    owner_id: int, 
    personality_config: dict = None,
    db: Session = Depends(get_db)
):
    # Create chatbot with optional personality configuration
    chatbot = Chatbot(
        name=name, 
        description=description, 
        owner_id=owner_id,
        personality_config=personality_config or {}
    )
    db.add(chatbot)
    db.commit()
    db.refresh(chatbot)
    return {"message": "Chatbot created", "chatbot_id": chatbot.id}

@app.post("/chatbots/{chatbot_id}/upload-document")
async def upload_document(
    chatbot_id: int, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file size (max 5MB)
    if file.size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max 5MB.")
    
    # Save temporary file
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        # Process document
        text = doc_processor.preprocess_document(temp_path)
        chunks = doc_processor.chunk_text(text)
        embeddings = doc_processor.generate_embeddings(chunks)
        
        # Store document and embeddings
        doc_processor.store_embeddings(chatbot_id, chunks, embeddings)
        
        # Save document metadata
        document = Document(
            filename=file.filename,
            content=text,
            chatbot_id=chatbot_id,
            embeddings={"chunks": chunks}
        )
        db.add(document)
        db.commit()
        
        return {"message": "Document uploaded and processed"}
    
    finally:
        # Clean up temporary file
        os.remove(temp_path)

@app.post("/chatbots/{chatbot_id}/chat")
def chat_with_chatbot(
    chatbot_id: int, 
    query: str,
    db: Session = Depends(get_db)
):
    # Retrieve chatbot
    chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Perform semantic search
    context = doc_processor.semantic_search(chatbot_id, query)
    
    # Generate response
    response = response_generator.generate_response(
        query, 
        ' '.join(context), 
        chatbot.personality_config
    )
    
    # Adjust response tone
    final_response = response_generator.adjust_tone(
        response, 
        chatbot.personality_config
    )
    
    return {"response": final_response}

@app.get("/dashboard")
def user_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Get user's chatbots
    chatbots = db.query(Chatbot).filter(Chatbot.owner_id == user_id).all()
    
    return {
        "total_chatbots": len(chatbots),
        "chatbots": [
            {
                "id": bot.id,
                "name": bot.name,
                "created_at": bot.created_at,
                "total_documents": len(bot.documents)
            } for bot in chatbots
        ]
    }

    
if __name__ == "__main__":
    init_db()
