from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routes import auth, chatbots
from app.models import init_db
from app.database import Base, engine, SessionLocal
from app.models import User 


# Initialize database tables
Base.metadata.create_all(bind=engine)

# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatbots.router, prefix="/chatbots", tags=["Chatbots"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Multi-Chatbot Creation Platform"}

if __name__ == "__main__":
    init_db()
