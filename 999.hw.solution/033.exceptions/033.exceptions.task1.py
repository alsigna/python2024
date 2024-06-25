import pynetbox

nb = pynetbox.api(
    url="https://demo.netbox.dev",
    token="5626ee6bb2c95bfb4e727307847b36f189f629cb",
)

name = "dmi01-akron-rtr01"
device = nb.dcim.devices.get(name=name)


# if device is not None:
#     device.description = "some new description"
#     device.save()
# else:
#     print(f"устройства с именем {name} не существует")

try:
    device.description = "some new description"
except AttributeError as exc:
    print(f"устройства с именем {name} не существует")
else:
    device.save()
