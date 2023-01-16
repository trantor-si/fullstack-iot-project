# import sys

# from domain.models.generic import create_all

# sys.path.append("..")

# from config import database
# from fastapi import APIRouter, Depends, Form, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session
# from starlette import status
# from starlette.responses import RedirectResponse

# import repositories.fullstack.domain.models.devices as models

# from .auth import get_current_user

# router = APIRouter(
#     prefix="/devices",
#     tags=["devices"],
#     responses={404: {"description": "Not found"}}
# )

# # models.Base.metadata.create_all(bind=engine)
# create_all()

# templates = Jinja2Templates(directory="templates")

# @router.get("/", response_class=HTMLResponse)
# async def read_all_by_user(request: Request, db: Session = Depends(database.get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todos = db.query(models.Devices).filter(models.Devices.owner_id == user.get("id")).all()

#     return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user})


# @router.get("/add-todo", response_class=HTMLResponse)
# async def add_new_todo(request: Request):
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


# @router.post("/add-todo", response_class=HTMLResponse)
# async def create_todo(request: Request, title: str = Form(...), description: str = Form(...),
#                       priority: int = Form(...), db: Session = Depends(database.get_session)):
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo_model = models.Devices()
#     todo_model.title = title
#     todo_model.description = description
#     todo_model.priority = priority
#     todo_model.complete = False
#     todo_model.owner_id = user.get("id")

#     db.add(todo_model)
#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# @router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
# async def edit_todo(request: Request, todo_id: int, db: Session = Depends(database.get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo = db.query(models.Devices).filter(models.Devices.id == todo_id).first()

#     return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})


# @router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
# async def edit_todo_commit(request: Request, todo_id: int, title: str = Form(...),
#                            description: str = Form(...), priority: int = Form(...),
#                            db: Session = Depends(database.get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo_model = db.query(models.Devices).filter(models.Devices.id == todo_id).first()

#     todo_model.title = title
#     todo_model.description = description
#     todo_model.priority = priority

#     db.add(todo_model)
#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# @router.get("/delete/{todo_id}")
# async def delete_todo(request: Request, todo_id: int, db: Session = Depends(database.get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo_model = db.query(models.Devices).filter(models.Devices.id == todo_id)\
#         .filter(models.Devices.owner_id == user.get("id")).first()

#     if todo_model is None:
#         return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

#     db.query(models.Devices).filter(models.Devices.id == todo_id).delete()

#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# @router.get("/complete/{todo_id}", response_class=HTMLResponse)
# async def complete_todo(request: Request, todo_id: int, db: Session = Depends(database.get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo = db.query(models.Devices).filter(models.Devices.id == todo_id).first()

#     todo.complete = not todo.complete

#     db.add(todo)
#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
