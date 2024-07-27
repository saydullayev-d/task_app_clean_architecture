from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, Sequence('orders_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=True)
    count = Column(BigInteger)
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    files = relationship("OrdersFiles", back_populates="order")

class OrdersFiles(Base):
    __tablename__ = 'orders_files'

    id = Column(Integer, Sequence('orders_files_id_seq'), primary_key=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=True)
    path = Column(String(255), nullable=True)

    order = relationship("Order", back_populates="files")
