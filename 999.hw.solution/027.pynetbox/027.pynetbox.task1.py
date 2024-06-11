import os

import pynetbox

nb = pynetbox.api(
    url=os.environ.get("NB_URL"),
    token=os.environ.get("NB_TOKEN"),
)

devices = nb.dcim.devices.filter(role="router")
for device in devices:
    print(f"name: {device.name}, model: {device.device_type.model}")
