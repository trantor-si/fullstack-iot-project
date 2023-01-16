import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

DBENV = {
  'sqlite': {
    'type': "sqlite",
    'prefix': "sqlite",
    'user': None,
    'password': None,
    'host': None,
    'port': None,
    'database': os.getenv('SQLITE_DATABASE', 'sqlite.db'),
    'connect_args': os.getenv('SQLITE_CONNECT_ARGS', {"check_same_thread": False}),
  },
  'postgresql': {
    'type': "postgresql",
    'prefix': "postgresql",
    'user': os.getenv('POSTGRESQL_USER', 'postgres'),
    'password': os.getenv('POSTGRESQL_PASSWD', ''),
    'host': os.getenv('POSTGRESQL_HOST', 'localhost'),
    'port': os.getenv('POSTGRESQL_PORT', '5432'),
    'database': os.getenv('POSTGRESQL_INSTANCE', 'postgres'),
    'connect_args': None,
  },
  'mysql': {
    'type': "mysql",
    'prefix': "mysql+pymysql",
    'user': os.getenv('MYSQLDB_USER', 'root'),
    'password': os.getenv('MYSQLDB_PASSWD', ''),
    'host': os.getenv('MYSQLDB_HOST', '127.0.0.1'),
    'port': os.getenv('MYSQLDB_PORT', '3306'),
    'database': os.getenv('MYSQLDB_INSTANCE', 'sys'),
    'connect_args': None,
  },
  'mariadb': {
    'type': "mariadb",
    'prefix': "mysql+pymysql",
    'user': os.getenv('MARIADB_USER', 'root'),
    'password': os.getenv('MARIADB_PASSWD', ''),
    'host': os.getenv('MARIADB_HOST', '127.0.0.1'),
    'port': os.getenv('MARIADB_PORT', '12354'),
    'database': os.getenv('MARIADB_INSTANCE', 'sys'),
    'connect_args': None,
  },
}

class ExtendedEnum(Enum):
  @classmethod
  def list(cls):
      return list(map(lambda c: c.value, cls))

class DBTYPES (ExtendedEnum):
  POSTGRESQL = 'postgresql'
  SQLITE = 'sqlite'
  MYSQL = 'mysql'
  MARIADB = 'mariadb'    

VALID_DATABASES = DBTYPES.list()

class DBConnection:
  def __init__(self, type : str = None):
    if type is None:
      self.type = os.getenv('CURRENT_DATABASE_TYPE', 'sqlite')
    else:
      self.type = type
    
    self.env = DBENV[self.type] if self.type in DBENV else None
  
  def get_connect_args(self):
    return self.env['connect_args']

  def get_connect_format(self):  
    self.connect_format = None
    if self.type == 'sqlite':
      self.connect_format = "{}:///{}"
    elif self.type == "postgresql":
      self.connect_format = '{}://{}:{}@{}:{}/{}'
    elif self.type == "mysql":
      self.connect_format = '{}://{}:{}@{}:{}/{}'
    elif self.type == "mariadb":
      self.connect_format = '{}://{}:{}@{}:{}/{}'
    return self.connect_format

  def get_url(self):
    url = None
    if self.env is not None:
      self.connect_format = self.get_connect_format()
      if self.type == 'sqlite':
        url = self.connect_format.format( \
          self.env['prefix'], self.env['database'])
      elif self.type == "postgresql":
        url = self.connect_format.format ( \
            self.env['prefix'], self.env['user'], \
            self.env['password'], self.env['host'], \
            self.env['port'], self.env['database'])
      elif self.type == "mysql":
        url = self.connect_format.format ( \
            self.env['prefix'], self.env['user'], \
            self.env['password'], self.env['host'], \
            self.env['port'], self.env['database'])
      elif self.type == "mariadb":
        url = self.connect_format.format ( \
            self.env['prefix'], self.env['user'], \
            self.env['password'], self.env['host'], \
            self.env['port'], self.env['database'])
    else:
      raise Exception('Invalid database type: [{}].'.format(self.type))

    return url
