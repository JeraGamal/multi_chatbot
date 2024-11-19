from fastapi import FastAPI
from app.routes import auth, chatbots
from app.models import init_db


app = FastAPI()

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatbots.router, prefix="/chatbots", tags=["Chatbots"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Multi-Chatbot Creation Platform"}

if __name__ == "__main__":
    init_db()

