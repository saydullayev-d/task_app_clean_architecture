from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str
    org_name: str
    inn: str
    number: str
    password: str
    user_id: int