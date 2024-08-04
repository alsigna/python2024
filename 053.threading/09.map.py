from concurrent.futures import ThreadPoolExecutor

from scrapli import Scrapli

scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}


def print_version(host: str) -> str:
    print(f"{host:>15}: подключение...")
    device = scrapli_template | {"host": host}

    if host == "192.168.122.115":
        raise ValueError("неизвестный хост")

    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")

    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    print(f"{host:>15}: завершено")
    return result


ip_addresses = [
    "192.168.122.102",
    "192.168.122.109",
    "192.168.122.110",
    "192.168.122.111",
    "192.168.122.112",
    "192.168.122.113",
    "192.168.122.114",
    "192.168.122.115",
    "192.168.122.116",
    "192.168.122.117",
    "192.168.122.101",
    "192.168.122.118",
]

with ThreadPoolExecutor(max_workers=5) as pool:
    results = pool.map(print_version, ip_addresses)
    print("задачи поставлены в пул")
    print("еще одна задача")

print("код за пределами контекстного менеджера ThreadPoolExecutor'a")

for r in results:
    print(r)
