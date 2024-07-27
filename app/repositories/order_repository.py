from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Client
from app.db.models.order import Order
from app.repositories.interfaces import IOrderRepository

class OrderRepository(IOrderRepository):
    
    def __init__(self, db: Session):
        self.db = db

    def get_orders(self) -> List[Order]:
        return self.db.query(Order).all()

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_order_status(self, order_id: int, status: str) -> Optional[Order]:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            self.db.commit()
            self.db.refresh(order)
        return order
    
    def get_client_by_tg_id(self, tg_id: str) -> Client:
        return self.db.query(Client).filter(Client.tg_id == tg_id).first()
