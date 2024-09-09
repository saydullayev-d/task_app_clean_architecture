from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Role(Base):
    __tablename__ = 'role'  # Название таблицы должно совпадать

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="role")  # Должно соответствовать полю в User
    
    def __str__(self):
        return self.role
