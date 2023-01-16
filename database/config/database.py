from domain.models import base_model
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from .dbconnection import DBConnection


class Database:
  def __init__(self, type : str = None):
    load_dotenv()
    
    self.type = type
    self.db_connection = DBConnection(self.type)
    self.engine = self.get_engine()
    self.session = None

  def get_engine(self):
    self.engine = None
    self.url = self.db_connection.get_url()
    self.connect_args = self.db_connection.get_connect_args()
    
    if self.connect_args is None:
      self.engine = create_engine(self.url)
    else:
      self.engine = create_engine(self.url, connect_args={"check_same_thread": False})

    if self.engine is not None:
      self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
      self.Base = base_model.Base
    else:
      raise Exception('Error creating engine for database type: [{}].'.format(self.db_connection.get_type()))

    return self.engine

  def get_session(self):
    if (self.session is None):
      Session = sessionmaker(bind=self.engine)
      self.session = Session()

    base_model.create_all(self.engine)
    return self.session
        
# define the current database 
def new_database(type : str = None):
  global current_database
  current_database = Database(type)
  return current_database

current_database = None
