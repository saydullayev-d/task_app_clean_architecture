from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.core.auth.manager import get_user_manager, UserManager

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager)
):
    user = await user_manager.authenticate(form_data)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    response_data = await user_manager.on_after_login(user)
    
    return JSONResponse(content=response_data)
