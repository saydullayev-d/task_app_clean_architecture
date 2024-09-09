from typing import Optional
from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .database import User, get_user_db
from .config import settings

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    def create_access_token(self, user: User, expires_delta: Optional[timedelta] = None):
        to_encode = {"sub": str(user.id)}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    async def on_after_login(self, user: User, request: Optional[Request] = None):
        role = user.role_id
        redirect_url = ""

        if role == 1:
            redirect_url = "/admin/dashboard"
        elif role == 2:
            redirect_url = f"/user/home/{user.id}"
        else:
            redirect_url = "/error"

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(user, expires_delta=access_token_expires)


        return {
            "access_token": access_token,
            "token_type": "bearer",
            "redirect_url": redirect_url
        }

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
