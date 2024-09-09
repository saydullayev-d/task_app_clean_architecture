from fastapi import FastAPI, Request, Depends
import fastapi_users
from fastapi_users import FastAPIUsers
from app.api.v1.endpoints import user, order, auth, registration, client
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.repositories.interfaces import IOrderRepository, IClientRepository, IUserRepository
from app.dependencies import get_order_repository, get_client_repository, get_user_repository
from app.utils.date_utils import format_datetime, format_time
from app.core.auth.auth import auth_backend
from app.core.auth.schemas import UserCreate, UserRead
from app.core.auth.database import User
from app.core.auth.manager import get_user_manager

from fastapi_users.authentication import AuthenticationBackend, BearerTransport, CookieTransport, JWTStrategy
import os

app = FastAPI()
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
cookie_transport = CookieTransport(cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

jwt_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
cookie_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

current_active_user = fastapi_users.current_user()
templates = Jinja2Templates(directory="app/templates")
app.include_router(user.router, prefix="/api/v1")
app.include_router(order.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/auth/jwt", tags=["auth"])
app.include_router(client.router, prefix="/api/v1")
app.include_router(registration.router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/admin/dashboard")
async def read_root(request: Request, 
                    order_repo: IOrderRepository = Depends(get_order_repository), 
                    client_repo: IClientRepository = Depends(get_client_repository),
                    user: User = Depends(current_active_user)
                    ):
    orders = order_repo.get_orders()
    items = []
    items_in_work = []
    items_done = []



    for order in orders:
        client = client_repo.get_client_by_tg_id(order.name) # Предположим, у вас есть метод для получения клиента

        folder_path = f"./{order.name}/{order.count}"
        files = []
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

        order_data = {
            "id": order.id,
            "name": client.name if client else "Unknown",
            'description': order.description,
            'user_id': order.name,
            'order_num': order.count,
            'inn': client.inn if client else "",
            'org_name': client.organization_name if client else "",
            'order_id': order.id,
            "files": len(files),
            'date': format_datetime(order.date),
            "time": format_time(order.date)
        }

        if order.status == "В работе":
            items_in_work.append(order_data)
        elif order.status == "В обработке":
            items.append(order_data)
        elif order.status == "Завершено":
            items_done.append(order_data)

    return templates.TemplateResponse("index.html", {"request": request, "items": items, "items_in_work": items_in_work, "items_done": items_done})

@app.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/user/home/{user_id}", response_class=HTMLResponse)
async def user_home(request: Request, user_id: int, order_repo: IOrderRepository = Depends(get_order_repository), 
client_repo: IClientRepository = Depends(get_client_repository),):
    orders = order_repo.get_uer_order(user_id)
    items = []
    items_in_work = []
    items_done = []



    for order in orders:
        client = client_repo.get_client_by_tg_id(order.name) # Предположим, у вас есть метод для получения клиента

        folder_path = f"./{order.name}/{order.count}"
        files = []
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

        order_data = {
            "id": order.id,
            "name": client.name if client else "Unknown",
            'description': order.description,
            'user_id': order.name,
            'order_num': order.count,
            'inn': client.inn if client else "",
            'org_name': client.organization_name if client else "",
            'order_id': order.id,
            "files": len(files),
            'date': format_datetime(order.date),
            "time": format_time(order.date)
        }

        if order.status == "В работе":
            items_in_work.append(order_data)
        elif order.status == "В обработке":
            items.append(order_data)
        elif order.status == "Завершено":
            items_done.append(order_data)

    return templates.TemplateResponse("user_home.html", {"request": request, "items": items, "items_in_work": items_in_work, "items_done": items_done})

@app.get("/client/{client_id}", response_class=HTMLResponse)
async def unknown_role(
    request: Request, 
    client_id: int, 
    order_repo: IOrderRepository = Depends(get_order_repository), 
    client_repo: IClientRepository = Depends(get_client_repository)):
    client = client_repo.get_client_by_id(client_id)
    orders = order_repo.get_client_order(client)
    items = []
    items_in_work = []

    for order in orders:
        folder_path = f"./{order.name}/{order.count}"
        files = []
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

        order_data = {
            "id": order.id,
            "name": client.name if client else "Unknown",
            'description': order.description,
            'user_id': order.name,
            'order_num': order.count,
            'inn': client.inn if client else "",
            'org_name': client.organization_name if client else "",
            'order_id': order.id,
            "files": len(files),
            'date': format_datetime(order.date),
            "time": format_time(order.date)
        }

        if order.status == "В работе":
            items_in_work.append(order_data)
        elif order.status == "В обработке":
            items.append(order_data)

    return templates.TemplateResponse("client.html", {"request": request, "items": items, "items_in_work": items_in_work, "client_id": client_id})



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
