from app.database import Base, engine
from app.models import User  # Ensure you import all models here


def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")


if __name__ == "__main__":
    create_tables()
