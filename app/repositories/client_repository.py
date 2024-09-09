from typing import Optional
from sqlalchemy.orm import Session
from app.db.models.client import Client
from app.db.models.user import User
from app.repositories.interfaces import IClientRepository

class ClientRepository(IClientRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_client_by_tg_id(self, tg_id: str) -> Optional[Client]:
        return self.db.query(Client).filter(Client.tg_id == tg_id).first()
    
    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        return self.db.query(Client).filter(Client.id == client_id).first()
    
    def get_client_by_username(self, username: str) -> Optional[Client]:
        return self.db.query(Client).join(User).filter(User.username == username).first()
    
    def add_client(self, name: str, org_name: str, inn: str, number: str, user_id: int) -> Client:
        if not self.get_client_by_username(inn):
            db_client = Client(name=name, number=number, inn=inn, organization_name=org_name, user_id=user_id)
            self.db.add(db_client)
            self.db.commit()
            self.db.refresh(db_client)
            return db_client
        else:
            return self.get_client_by_username(inn)