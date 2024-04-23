# Создать два словаря c параметрами оборудования (ниже перечисление в виде "ключ = значение")

# - первый словарь (`device1`):
#   - hostname = r1.abcd.net
#   - ip = 192.168.1.1
#   - username = cisco
#   - password = secret
#   - platform = cisco_ios
#   - enable = True
# - второй словарь (`device2`):
#   - hostname = sw1.abcd.net
#   - ip = 192.168.1.2
#   - username = admin
#   - password = secret
#   - platform = huawei_vrp
#   - enable = False

device1 = {
    "hostname": "r1.abcd.net",
    "ip": "192.168.1.1",
    "username": "cisco",
    "password": "secret",
    "platform": "cisco_ios",
    "enable": True,
}

device2 = dict(
    hostname="sw1.abcd.net",
    ip="192.168.1.2",
    username="admin",
    password="secret",
    platform="huawei_vrp",
    enable=False,
)
