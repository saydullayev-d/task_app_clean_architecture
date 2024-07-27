from pydantic import BaseSettings
from fastapi.security import OAuth2PasswordBearer

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
