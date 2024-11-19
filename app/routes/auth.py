from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, SessionLocal
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secret-key"  # Change this in production
ALGORITHM = "HS256"

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)

# Register a user
@router.post("/register")
async def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = hash_password(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

# Login a user
@router.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

