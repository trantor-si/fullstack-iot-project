import sys

from config.database import Database
from domain.models.devices_model import DevicesModel, ValuesModel

sys.path.insert(0, '../broker/')

import pandas as pd
from consumer import run_kafka_consumer


def prepare_database():
  database = Database('postgresql')
  session = database.get_session()
  return session

def store_device(session, device_address, device_name, device_register, 
                 device_unit, device_range, device_type, value):
  device = session.query(DevicesModel)\
        .filter(DevicesModel.id_device == int(device_address)).all()
  
  if device is None:
    device = DevicesModel(
        id_device=int(device_address),
        device_address=device_address,
        device_name=device_name,
        device_register=device_register,
        device_unit=device_unit,
        device_range=device_range,
        device_type=device_type,
    )
    session.add(device)
    session.commit()
  
  value = ValuesModel(
      id_device=int(device_address),
      value=value,
  )
  session.add(value)
  session.commit()

def run_database():
    data_dict = run_kafka_consumer(silent=True)
    session = prepare_database()
    
    for data in data_dict.values():
      for sensor_data in data:
        device_address = sensor_data['Endereco']
        device_name = sensor_data['device']
        device_register = sensor_data['Registrador']
        device_unit = sensor_data['Unidade']
        device_range = sensor_data['Range']
        device_type = sensor_data['Tipo / Função']
        
        value = sensor_data['Valor']
        
        store_device(session, device_address, device_name, device_register,
                      device_unit, device_range, device_type, value)


if __name__ == '__main__':
    run_database()
