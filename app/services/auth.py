from passlib.context import CryptContext
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate
from app.db.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.user_repo.get_user(username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def create_user(self, user_create: UserCreate) -> User:
        hashed_password = self.get_password_hash(user_create.password)
        return self.user_repo.create_user(user_create.username, hashed_password, user_create.role_id)
    
    def get_user_role(self, username: str) -> str:
        user = self.user_repo.get_user_by_username(username)
        if user and user.role:
            return user.role.role
        return "unknown"
    

