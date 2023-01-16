from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GenericBase(Base):
  __abstract__ = True
  
  
def create_all(engine):
  Base.metadata.create_all(bind=engine)
