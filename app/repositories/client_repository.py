from typing import Optional
from sqlalchemy.orm import Session
from app.db.models.client import Client
from app.repositories.interfaces import IClientRepository

class ClientRepository(IClientRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_client_by_tg_id(self, tg_id: str) -> Optional[Client]:
        return self.db.query(Client).filter(Client.tg_id == tg_id).first()