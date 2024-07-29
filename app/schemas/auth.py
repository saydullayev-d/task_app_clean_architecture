# app/api/v1/schemas/auth.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class RoleCreate(BaseModel):
    role: str
