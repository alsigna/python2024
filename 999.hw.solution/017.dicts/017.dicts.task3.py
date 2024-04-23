# На основе списка из Task2 создать словарь `devices_dict` в котором в качестве ключей будут выступать `hostname` устройств,
# а в качестве значений - соответсвующие элементы списка `devices_list`.

# Структура: `{<key>:{}, <key>:{}, <key>:{}}`

devices_list = []
devices_list.append(
    dict(
        hostname="r1.abcd.net",
        ip="192.168.1.1",
        username="cisco",
        password="secret",
        platform="cisco_ios",
        enable=True,
    )
)
devices_list.append(
    dict(
        hostname="sw1.abcd.net",
        ip="192.168.1.2",
        username="admin",
        password="secret",
        platform="huawei_vrp",
        enable=False,
    )
)
devices_list.append(
    dict(
        hostname="wlc.abcd.net",
        ip="192.168.1.3",
        username="wlc_admin",
        password="password",
        enable=False,
    )
)

hostnames = devices_list[0].get("hostname"), devices_list[1].get("hostname"), devices_list[2].get("hostname")

devices_dict = dict.fromkeys(hostnames, {})

devices_dict[hostnames[0]] = devices_list[0]
devices_dict[hostnames[1]] = devices_list[1]
devices_dict[hostnames[2]] = devices_list[2]

# либо с использованием функции `zip`

devices_dict = dict(zip(hostnames, devices_list))
