from random import Random

from config.database import Database
from domain.models.devices_model import DevicesModel, ValuesModel

database = Database('postgresql')
session = database.get_session()

num = Random().randint(1, 100000)
device = DevicesModel(
    id_device=num,
    device_address=str(num),
    device_name="messor",
    device_register="FREQUENCIA",
    device_unit="0.01 * Hz",
    device_range="0 a 500",
    device_type="Read Input Register / 04",
)

session.add(device)
session.commit()

value = ValuesModel(
    id_device=num,
    value=100.0 + num,
)

session.add(value)
session.commit()

