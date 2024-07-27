from pydantic import BaseModel

class StatusUpdate(BaseModel):
    status: str

class OrderResponse(BaseModel):
    id: int
    status: str

    class Config:
        orm_mode: True