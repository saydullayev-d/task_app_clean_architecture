from typing import Optional
from sqlalchemy.orm import Session
from app.db.models.user import User, Role

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, username: str, hashed_password: str, role_id: int) -> User:
        db_user = User(username=username, hashed_password=hashed_password, role_id=role_id)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_role(self, role: str) -> Role | None:
        return self.db.query(Role).filter(Role.role == role).first()

    def create_role(self, role: str) -> Role:
        db_role = Role(role=role)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_role(self, username: str) -> str:
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            role = self.db.query(Role).filter(Role.id == user.role_id).first()
            return role.role if role else None
        return None