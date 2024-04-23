# Создать список `devices_list`, содержащий словари `device1` и `device2` из задания [Task1](017.dicts.md#task1-плоский-словарь)

# Структура: `[{}, {}]`

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

devices_list = [
    device1,
    device2,
]

# с использованием промежуточной переменной
device3 = dict(
    hostname="wlc.abcd.net",
    ip="192.168.1.3",
    username="wlc_admin",
    password="password",
    enable=False,
)

devices_list.append(device3)

# или без нее
devices_list.append(
    {
        "hostname": "wlc.abcd.net",
        "ip": "192.168.1.3",
        "username": "wlc_admin",
        "password": "password",
        "enable": True,
    }
)
