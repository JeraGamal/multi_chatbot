from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON, Text, Boolean, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timedelta
import uuid

# Database Configuration
DATABASE_URL = "sqlite:///./multi_chatbot.db"
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    chatbots = relationship("Chatbot", back_populates="owner")
    documents = relationship("Document", back_populates="owner")

# Chatbot Model
class Chatbot(Base):
    __tablename__ = "chatbots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Personality configuration
    personality_config = Column(JSON, default={
        "friendliness": 0.5,  # 0-1 scale for dynamic personality
        "formality": 0.5,
        "creativity": 0.5
    })
    
    # Relationships
    owner = relationship("User", back_populates="chatbots")
    documents = relationship("Document", back_populates="chatbot")
    interactions = relationship("ChatbotInteraction", back_populates="chatbot")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(Text)  # Store preprocessed text
    embeddings = Column(JSON)  # Store vector embeddings
    owner_id = Column(Integer, ForeignKey("users.id"))
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"))
    created_at = Column(DateTime, default=func.now())
    version = Column(Integer, default=1)
    
    # Version control attributes
    is_latest = Column(Boolean, default=True)
    previous_version_id = Column(Integer, ForeignKey('documents.id'), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    chatbot = relationship("Chatbot", back_populates="documents")

class ChatbotInteraction(Base):
    __tablename__ = "chatbot_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"))
    user_input = Column(String)
    bot_response = Column(String)
    interaction_timestamp = Column(DateTime, default=func.now())
    
    # Relationship
    chatbot = relationship("Chatbot", back_populates="interactions")

# Utility function for table creation
def create_tables(engine):
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")



# Execute table creation
if __name__ == "__main__":
    create_tables()




