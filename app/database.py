from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite Database URL
DATABASE_URL = "sqlite:///./test.db"  # You can change the name of the database file if needed

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # Required for SQLite
)

# Create a SessionLocal class to create sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for SQLAlchemy models
Base = declarative_base()

