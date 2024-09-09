from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .base import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    number = Column(String(15), nullable=True)
    inn = Column(String(100), nullable=True)
    organization_name = Column(String(150), nullable=True)
    tg_id = Column(Integer)

    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="clients")  # Используем строку "User"
    order = relationship("Order", back_populates="client")
