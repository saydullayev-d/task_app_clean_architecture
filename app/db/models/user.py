from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base
from .role import Role

class User(Base):
    __tablename__ = "user"  # Проверьте, если это название соответствует в базе данных
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"))  # Убедитесь, что это имя правильно
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email = Column(String, nullable=False)

    role = relationship("Role", back_populates="user")
    clients = relationship("Client", back_populates="user")
    orders = relationship("Order", back_populates="user")  # Исправлено с "order" на "orders"
