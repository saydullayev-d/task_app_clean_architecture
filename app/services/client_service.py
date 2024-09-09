from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate
from app.db.models.client import Client

class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    def get_client_id(self, username: str):
        client = self.client_repo.get_client_by_username(username)
        if client and client.id:
            print(f"id - {client.id}")
            return client.id
        else: 
            return "unknow"
        
    def create_client(self, client_create: ClientCreate) -> Client:
        user = self.client_repo.get_client_by_username(client_create.inn)
        if user and user.user_id:
            self.client_repo.add_client(client_create.name, client_create.org_name, client_create.inn, client_create.number, user.user_id)