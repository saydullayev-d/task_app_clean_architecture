from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth import AuthService
from app.schemas.auth import UserCreate, Token

router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    role = auth_service.get_user_role(form_data.username)
    
    access_token = user.username  # Для примера используется username как токен, замените на реальный токен

    if role == "admin":
        return {"access_token": access_token, "token_type": "bearer", "redirect_url": "/admin/dashboard"}
    elif role == "user":
        return {"access_token": access_token, "token_type": "bearer", "redirect_url": "/user/home"}
    else:
        return {"access_token": access_token, "token_type": "bearer", "redirect_url": "/unknown"}



@router.post("/users/", response_model=UserCreate)
async def create_user(user_create: UserCreate, role: str, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    db_user = auth_service.create_user(user_create, role)
    return db_user
