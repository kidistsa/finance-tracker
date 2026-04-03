from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel, EmailStr
from app.core.config import settings
from app.core.db import db_client
from app.api.dependencies.auth import get_current_user
import bcrypt
import secrets

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(password: str, hashed: str) -> bool:
    password_bytes = password.encode('utf-8')[:72]
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    query = "SELECT email, hashed_password, role FROM users WHERE email = ?"
    result = db_client.fetch_one(query, (user.email,))
    
    if not result:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not verify_password(user.password, result['hashed_password']):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    query = "SELECT email, role FROM users WHERE email = ?"
    result = db_client.fetch_one(query, (current_user["email"],))
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "email": result["email"],
        "role": result["role"] if result["role"] else "user"
    }
