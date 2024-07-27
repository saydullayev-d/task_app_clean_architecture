# app/services/order_service.py
from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.repositories.client_repository import ClientRepository
from app.utils.date_utils import format_datetime, format_time
import os

class OrderService:
    def __init__(self, order_repository: OrderRepository, client_repository: ClientRepository):
        self.order_repository = order_repository
        self.client_repository = client_repository

    def get_order_detail(self, order_id: int) -> dict:
        orders = self.order_repository.get_orders()
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        order_num = orders.index(order) + 1
        client_name = self.client_repository.get_client_by_tg_id(order.name)
        folder_path = f"./{order.name}/{order.count}"
        files = []
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

        return {
            "order": order,
            "client_name": client_name,
            "files": files,
            "order_num": order_num,
            "date": format_datetime(order.date),
            "time": format_time(order.date),
        }
