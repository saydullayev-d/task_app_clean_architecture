from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from app.repositories.interfaces import IOrderRepository, IUserRepository
from app.repositories.client_repository import ClientRepository
from app.repositories.user_repository import UserRepository
from app.dependencies import get_order_repository, get_client_repository, get_user_repository
from fastapi.responses import HTMLResponse
from app.services.order_service import OrderService
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.db.session import get_db
from app.schemas.order import StatusUpdate, OrderResponse
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy
from app.core.auth.manager import get_user_manager
from app.db.models.user import User
from app.core.auth.auth import auth_backend



# Инициализация FastAPI Users
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Определяем зависимость для текущего авторизованного пользователя
current_active_user = fastapi_users.current_user(active=True)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_order_service(db: Session = Depends(SessionLocal)) -> OrderService:
    repository = OrderRepository(db)
    return OrderService(repository)

# Защищённый эндпоинт для чтения всех заказов
@router.get("/orders/")
async def read_orders(order_repo: IOrderRepository = Depends(get_order_repository), user: User = Depends(current_active_user)):
    return order_repo.get_orders()

# Защищённый эндпоинт для чтения одного заказа по ID
@router.get("/orders/{order_id}")
async def read_order(order_id: int, order_repo: IOrderRepository = Depends(get_order_repository), user: User = Depends(current_active_user)):
    order = order_repo.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Защищённый эндпоинт для обновления статуса заказа
@router.put("/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: int, status: StatusUpdate, order_repo: IOrderRepository = Depends(get_order_repository), user: User = Depends(current_active_user)):
    updated_order = order_repo.update_order_status(order_id, status.status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

# Защищённый эндпоинт для обновления исполнителя заказа
@router.put("/order/{order_id}/{user_id}")
async def update_order_executor(order_id: int, user_id: int, order_repo: IOrderRepository = Depends(get_order_repository), user: User = Depends(current_active_user)):
    updated_order = order_repo.update_order_executor(order_id, user_id)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

# Защищённый эндпоинт для чтения деталей заказа
@router.get("/order_detail/{task_id}", response_class=HTMLResponse, name="task_detail")
async def read_order_detail(
    request: Request, 
    task_id: int, 
    order_repo: OrderRepository = Depends(get_order_repository),
    client_repo: ClientRepository = Depends(get_client_repository),
    user_repo: IUserRepository = Depends(get_user_repository),
    user: User = Depends(current_active_user)  # Проверка авторизации
):
    service = OrderService(order_repo, client_repo, user_repo)
    try:
        details = service.get_order_detail(task_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")

    return templates.TemplateResponse(
        "order_card.html",
        {"request": request,  **details}
    )

# Защищённый эндпоинт для чтения деталей заказа клиента
@router.get("/client_order_detail/{task_id}", response_class=HTMLResponse, name="task_detail_client")
async def read_order_detail(
    request: Request, 
    task_id: int, 
    order_repo: OrderRepository = Depends(get_order_repository),
    client_repo: ClientRepository = Depends(get_client_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    user: User = Depends(current_active_user)  # Проверка авторизации
):
    service = OrderService(order_repo, client_repo, user_repo)
    try:
        details = service.get_order_detail(task_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")

    return templates.TemplateResponse(
        "client_order_card.html",
        {"request": request, **details}
    )
