import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from random import randint

from scrapli import Scrapli

scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}


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


def print_version(host: str) -> str:
    print(f"{host:>15}: подключение...")
    if host == "192.168.122.101":
        time.sleep(5)

    device = scrapli_template | {"host": host}

    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")

    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    time.sleep(randint(10, 200) / 100)
    print(f"{host:>15}: завершено")
    return result


with ThreadPoolExecutor(max_workers=5) as pool:
    futures: list[Future] = []
    for ip in ip_addresses:
        futures.append(pool.submit(print_version, ip))

    print("задачи поставлены в очередь")

    for f in futures:
        print(f.result())

    for f in as_completed(futures):
        print(f.result())

print("код за пределами with")


# with ThreadPoolExecutor(max_workers=5) as pool:
#     futures: list[Future] = [pool.submit(print_version, ip) for ip in ip_addresses]
#     print("задачи поставлены в очередь")

#     # for f in futures:
#     #     print(f.result())

#     for f in as_completed(futures):
#         print(f.result())
