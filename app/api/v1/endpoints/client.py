from fastapi import APIRouter, Depends
from app.schemas.client import ClientCreate
from app.db.session import get_db
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService
from sqlalchemy.orm import Session



router = APIRouter()

@router.post("/add_client", response_model=ClientCreate)
def add_client(client_create: ClientCreate, db: Session = Depends(get_db)):
    client_repo = ClientRepository(db)
    client_service = ClientService(client_repo)
    client_service.create_client(client_create)
    return client_create
