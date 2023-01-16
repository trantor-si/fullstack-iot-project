import os
import sys
import uuid

from config.database import current_database, new_database
from domain.models.devices_model import DevicesModel
from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

def get_dbsession():
  print('****** get_session: ENTER !')
  try:
    current_database.session = current_database.SessionLocal()
    print('****** get_session: {}'.format(current_database.session))
    yield current_database.session
  
  finally:
      current_database.session.close()

new_database(os.getenv('CURRENT_DATABASE_TYPE', 'postgresql'))

def db_get_device(id_device: int):
    print('Getting DB session...')        
    db = current_database.SessionLocal()
    print (db)
    print('Session DB created.')
    
    device_model = db.query(DevicesModel) \
            .filter(DevicesModel.id_device == id_device) \
            .first()
            
    return device_model

def db_create_device(device_address: str, device_name: str, device_register: str, 
                     device_unit: str, device_range: str, device_type: str):
    print('Getting session...')        
    db = get_dbsession()
    print('Session created.')
    
    device_model = DevicesModel()
    
    device_model.id_device = int(device_address)
    device_model.device_address = device_address
    device_model.device_name = device_name
    device_model.device_register = device_register
    device_model.device_unit = device_unit
    device_model.device_range = device_range
    device_model.device_type = device_type

    db.add(device_model)
    db.commit()
    db.refresh()

# def db_get_todos(user_id : int, db: Session, skip: int = 0, limit: int = None):
#     if limit is None:
#         todos = db.query(TodosModel) \
#             .filter(TodosModel.owner_id == user_id) \
#             .offset(skip).limit(limit) \
#             .all()
#     else:
#         todos = db.query(TodosModel) \
#             .filter(TodosModel.owner_id == user_id) \
#             .offset(skip) \
#             .all()

#     return todos

# def db_get_todo(todo_id: int, db: Session):
#     todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id).first()
#     return todo_model

# def db_edit_todo_commit(todo_id: int, title: str, description: str, 
#                         priority: int, db: Session):

#     todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id).first()

#     todo_model.title = title
#     todo_model.description = description
#     todo_model.priority = priority

#     db.add(todo_model)
#     db.commit()
#     db.refresh()

# def db_delete_todo(todo_id: int, db: Session):
#     db.query(TodosModel).filter(TodosModel.id == todo_id).delete()
#     db.commit()
#     db.refresh()

# def db_complete_todo(todo_id: int, db: Session):
#     todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id).first()
#     todo_model.complete = not todo_model.complete
#     db.add(todo_model)
#     db.commit()
#     db.refresh()
