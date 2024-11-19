from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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
    
    # Optional: Relationship with Chatbots
    chatbots = relationship("Chatbot", back_populates="owner")

# Chatbot Model
class Chatbot(Base):
    __tablename__ = "chatbots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Optional: Relationship with User
    owner = relationship("User", back_populates="chatbots")

# Function to create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

# Execute table creation
if __name__ == "__main__":
    create_tables()
