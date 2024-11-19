from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, User
import bcrypt
import jwt

router = APIRouter()

SECRET_KEY = "jeras-secret-key"  # Replace with a strong, unique secret key
ALGORITHM = "HS256"

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility to hash passwords using bcrypt
def hash_password(password: str):
    # Encode the password and salt, then hash
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

# Register a user
@router.post("/register")
async def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Create new user
    new_user = User(
        username=username, 
        email=email, 
        hashed_password=hashed_password
    )
    
    # Add and commit to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user_id": new_user.id}

# Login a user
@router.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    # Find user by username
    user = db.query(User).filter(User.username == username).first()
    
    # Verify credentials
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    token = jwt.encode(
        {"sub": user.username}, 
        SECRET_KEY, 
        algorithm=ALGORITHM
    )
    
    return {"access_token": token, "token_type": "bearer"}
