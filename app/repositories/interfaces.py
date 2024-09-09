from typing import List, Optional
from abc import ABC, abstractmethod
from app.db.models.user import User
from app.db.models.order import Order
from app.db.models.client import Client

class IUserRepository(ABC):

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_users(self) -> List[User]:
        pass

class IOrderRepository(ABC):

    @abstractmethod
    def get_orders(self) -> List[Order]:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def update_order_status(self, order_id: int, status: str) -> Optional[Order]:
        pass

    def get_client_by_tg_id(self, tg_id: str) -> Client:
        raise NotImplementedError
    
    @abstractmethod
    def get_client_order(self, client: Client) -> Optional[Order]:
        pass

    @abstractmethod
    def update_order_executor(self, order_id:int, user_id:int) -> Optional[Order]:
        pass

    @abstractmethod
    def get_uer_order(self, user_id: int) -> List[Order]:
        pass

class IClientRepository(ABC):

    @abstractmethod
    def get_client_by_tg_id(self, name: str) -> Client:
        pass

    @abstractmethod 
    def get_client_by_id(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def add_client(self, client: Client) -> Client:
        pass
