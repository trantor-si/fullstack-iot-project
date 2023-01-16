import uuid

from domain.schemas.generic import GenericModel
from pydantic import Field


class Devices(GenericModel):
    id_device: uuid = Field(title='Device ID', example="123e4567-e89b-12d3-a456-426655440000")
    device_name: str = Field(title='Device Name', example="messor")
    address: str = Field(title='Device Address', example="66")
    register: str = Field(title='Device Register', example="FREQUENCIA")
    unit: str = Field(title='Device Unit', example="Hz")
    type: str = Field(title='Device Type', example="Read Input Register / 04")

    class Config:
        orm_mode = True
