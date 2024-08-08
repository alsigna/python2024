from netmiko import ConnectHandler

device_netmiko = {
    "device_type": "cisco_ios",
    "username": "admin",
    "password": "P@ssw0rd",
}


def get_output(ip_addresses: list[str], cmd: str) -> dict[str, str]:
    result = {}
    for ip in ip_addresses:
        result[ip] = get_output_netmiko(ip, cmd)
    return result


def get_output_netmiko(ip: str, cmd: str) -> str:
    print(f"{ip:>15}: connecting ...")
    device = device_netmiko | {"host": ip}
    with ConnectHandler(**device) as ssh:
        output = ssh.send_command(cmd)
    print(f"{ip:>15}: done")
    return output


ip_addresses = [
    "192.168.122.109",
    "192.168.122.110",
    "192.168.122.111",
    "192.168.122.112",
    "192.168.122.113",
    "192.168.122.114",
    "192.168.122.115",
    "192.168.122.116",
    "192.168.122.117",
    "192.168.122.118",
]


if __name__ == "__main__":
    # python 21.async.netmiko.py  1.28s user 0.09s system 6% cpu 20.319 total
    get_output(ip_addresses, "show version")
