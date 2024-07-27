from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    number = Column(String(15), nullable=True)
    inn = Column(String(100), nullable=True)
    organization_name = Column(String(150), nullable=True)
    tg_id = Column(Integer)
