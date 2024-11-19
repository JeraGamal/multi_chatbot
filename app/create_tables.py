from app.database import Base, engine
from app.models import User  # Ensure you import all models here

# Create tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")

