import uuid
from datetime import date

from domain.schemas.generic import GenericModel
from pydantic import Field


class User(GenericModel):
    id_device_value: uuid = Field(title='Device Value ID', example="123e4567-e89b-12d3-a456-426655440000")
    id_device: uuid = Field(title='Device ID', example="123e4567-e89b-12d3-a456-426655440000")
    dt_creation: date = Field(default=date.today(), title='Device Value Creation Date', example="2021-01-01 00:00:00")
    value: float = Field(title='Device Value', example=1966.29)

    class Config:
        orm_mode = True
