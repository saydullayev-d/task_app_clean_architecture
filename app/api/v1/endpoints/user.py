from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.db.models.user import User  # Import User model
from app.repositories.interfaces import IUserRepository
from app.repositories.user_repository import UserRepository
from app.services.auth import AuthService
from app.db.session import get_db
from app.dependencies import get_user_repository
from app.schemas.auth import UserCreate

router = APIRouter()

# Define the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/users/", response_model=UserCreate)
async def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    db_user = auth_service.create_user(user_create)
    return UserCreate(username=db_user.username, password=user_create.password, role_id=db_user.role_id)

