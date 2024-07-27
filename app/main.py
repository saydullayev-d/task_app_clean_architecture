from fastapi import FastAPI, Request, Depends
from app.api.v1.endpoints import user, order, auth
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.repositories.interfaces import IOrderRepository, IClientRepository
from app.dependencies import get_order_repository, get_client_repository
from app.utils.date_utils import format_datetime, format_time
import os

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.include_router(user.router, prefix="/api/v1")
app.include_router(order.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/admin/dashboard")
async def read_root(request: Request, order_repo: IOrderRepository = Depends(get_order_repository), client_repo: IClientRepository = Depends(get_client_repository)):
    orders = order_repo.get_orders()
    items = []
    items_in_work = []

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

    return templates.TemplateResponse("index.html", {"request": request, "items": items, "items_in_work": items_in_work})

@app.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/user/home", response_class=HTMLResponse)
async def user_home(request: Request):
    return templates.TemplateResponse("user_home.html", {"request": request})

@app.get("/unknown", response_class=HTMLResponse)
async def unknown_role(request: Request):
    return templates.TemplateResponse("unknown_role.html", {"request": request})



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
