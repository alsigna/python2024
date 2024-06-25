import os

import pynetbox

url = os.environ.get("NB_URL")
token = os.environ.get("NB_TOKEN")

if not all([url, token]):
    raise ValueError("Отсутствуют параметры подключения к серверу")

nb = pynetbox.api(url=url, token=token)

name = "dmi01-akron-rtr01"
device = nb.dcim.devices.get(name=name)

try:
    device.description = "test"
except AttributeError as exc:
    print(f"устройства с именем {name} не существует")
else:
    device.save()
