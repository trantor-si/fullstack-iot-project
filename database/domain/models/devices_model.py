from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base_model import GenericBase


class DevicesModel(GenericBase):
    __tablename__ = "devices"

    id_device = Column(Integer(), primary_key=True, index=True)
    device_address = Column(String(100), unique=True)
    device_name = Column(String(100), default="messor")
    device_register = Column(String(100))
    device_unit = Column(String(100))
    device_range = Column(String(100))
    device_type = Column(String(100))
    device_dt_creation = Column(DateTime(), default=datetime.now)
    
    value = relationship("ValuesModel", back_populates="device")

class ValuesModel(GenericBase):
    __tablename__ = "devicevalues"

    id_device_value = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    id_device = Column(Integer(), ForeignKey("devices.id_device"))
    dt_creation = Column(DateTime(), default=datetime.now)
    value = Column(Float)

    device = relationship("DevicesModel", back_populates="value")
