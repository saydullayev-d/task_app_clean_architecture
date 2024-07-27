from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.db.models.user import User  # Import User model
from app.repositories.interfaces import IUserRepository
from app.dependencies import get_user_repository

router = APIRouter()

# Define the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str
    role: int

@router.post("/users/")
async def create_new_user(user: UserCreate, user_repo: IUserRepository = Depends(get_user_repository)):
    db_user = user_repo.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password, role_id=user.role)
    return user_repo.create_user(new_user)
