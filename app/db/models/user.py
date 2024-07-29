# app/db/models/user.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey("role.id"))

    role = relationship("Role", back_populates="users")



class Role(Base):
    __tablename__ = 'role'
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="role")

    def __str__(self):
        return self.role
