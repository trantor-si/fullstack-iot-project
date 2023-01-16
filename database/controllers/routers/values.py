# import sys

# from controllers.routers.auth import (authenticate_user, get_current_user,
#                                       get_password_hash, logout)
# from domain.models.generic import create_all

# sys.path.append("..")

# from datetime import datetime, timedelta
# from typing import Optional

# from config import database
# from fastapi import (APIRouter, Depends, Form, HTTPException, Request,
#                      Response, status)
# from fastapi.responses import HTMLResponse
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi.templating import Jinja2Templates
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
# from starlette.responses import RedirectResponse

# import repositories.fullstack.domain.models.devices as todosmodels
# import repositories.fullstack.domain.models.values as usermodels

# router = APIRouter(
#     prefix="/values",
#     tags=["values"],
#     responses={401: {"user": "Not authorized"}}
# )

# templates = Jinja2Templates(directory="templates")
# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# @router.get("/change-password", response_class=HTMLResponse)
# async def change_password(request: Request):
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     return templates.TemplateResponse("change-password.html", {"request": request, "user": user})

# @router.post("/change-password", response_class=HTMLResponse)
# async def change_password(request: Request, old_password: str = Form(...),
#                         new_password: str = Form(...), confirm_password: str = Form(...),
#                         db: Session = Depends(database.get_session)):
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     if not authenticate_user(user.get("username"), old_password, db):
#         return templates.TemplateResponse("change-password.html", {"request": request, "user": user, "errmsg": "Old Password incorrect!"})

#     user_model = db.query(usermodels.Values).filter(usermodels.Values.id == user.get("id")).first()
#     todos_model = db.query(todosmodels.Devices).filter(todosmodels.Devices.owner_id == user.get("id")).all()

#     new_hashed_password = get_password_hash(new_password)
#     user_model.hashed_password = new_hashed_password

#     db.add(user_model)
#     db.commit()

#     logout(request)

#     msg = "User password successfully changed"
#     return templates.TemplateResponse("login.html", 
#         {"request": request, "todos": todos_model, "msg": msg, "username": user_model.username})
