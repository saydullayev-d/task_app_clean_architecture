from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from app.repositories.interfaces import IOrderRepository
from app.repositories.client_repository import ClientRepository
from app.dependencies import get_order_repository, get_client_repository
from fastapi.responses import HTMLResponse
from app.services.order_service import OrderService
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository   
from app.db.session import get_db
from app.schemas.order import StatusUpdate, OrderResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_order_service(db: Session = Depends(SessionLocal)) -> OrderService:
    repository = OrderRepository(db)
    return OrderService(repository)

@router.get("/orders/")
async def read_orders(order_repo: IOrderRepository = Depends(get_order_repository)):
    return order_repo.get_orders()

@router.get("/orders/{order_id}")
async def read_order(order_id: int, order_repo: IOrderRepository = Depends(get_order_repository)):
    order = order_repo.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: int, status: StatusUpdate, order_repo: IOrderRepository = Depends(get_order_repository)):
    updated_order = order_repo.update_order_status(order_id, status.status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.get("/order_detail/{task_id}", response_class=HTMLResponse, name="task_detail")
async def read_order_detail(
    request: Request, 
    task_id: int, 
    order_repo: OrderRepository = Depends(get_order_repository),
    client_repo: ClientRepository = Depends(get_client_repository)
):
    service = OrderService(order_repo, client_repo)
    try:
        details = service.get_order_detail(task_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")

    return templates.TemplateResponse(
        "order_card.html",
        {"request": request, **details}
    )
