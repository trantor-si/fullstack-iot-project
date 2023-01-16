# from datetime import datetime, timedelta

# from sqlalchemy.orm import Session

# from domain.models.todos import TodosModel
# from domain.models.users import UsersModel


# def db_get_users(db: Session):
#     return db.query(UsersModel).all()

# def db_get_user(db: Session, user_id: int):
#     return db.query(UsersModel).filter(UsersModel.id == user_id).first()


# def db_get_user_by_email(db: Session, email: str):
#     return db.query(UsersModel).filter(UsersModel.email == email).first()

# def db_create_user(db: Session, user: UsersModel):
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# def db_create_user_todo(db: Session, todo_model: TodosModel):
#     db.add(todo_model)
#     db.commit()
#     db.refresh(todo_model)
#     return todo_model

# def db_exist_user(username: str, email: str, db : Session) -> bool:
#     exist_username = db.query(UsersModel).filter(UsersModel.username == username).first()
#     exist_email = db.query(UsersModel).filter(UsersModel.email == email).first()

#     return exist_username is not None or exist_email is not None

# def db_register_user(email: str, username: str, firstname: str, 
#                   lastname: str, hash_password: str, db: Session):
#     user_model = UsersModel()
#     user_model.username = username
#     user_model.email = email
#     user_model.first_name = firstname
#     user_model.last_name = lastname

#     user_model.hashed_password = hash_password
#     user_model.is_active = True

#     db.add(user_model)
#     db.commit()
