import time
import traceback
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
]  # ip_addresses.append("192.168.122.103")


def print_version(host: str) -> str:
    if host.endswith("115"):
        raise ValueError("плохой хост")

    device = scrapli_template | {"host": host}
    if host.endswith("116"):
        device |= {"auth_username": "bad_user"}

    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")

    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    time.sleep(randint(10, 200) / 100)
    return result


with ThreadPoolExecutor(max_workers=5) as pool:
    futures: list[Future] = []
    for ip in ip_addresses:
        futures.append(pool.submit(print_version, ip))

    futures: dict[Future, str] = {}
    for ip in ip_addresses:
        f = pool.submit(print_version, ip)
        futures[f] = ip
    # futures: dict[Future, str] = {pool.submit(print_version, ip): ip for ip in ip_addresses}

    for f in as_completed(futures):
        ip = futures.get(f)
        exc = f.exception()

        if exc is not None:
            print(f"{ip}: результат: 'ошибка выполнения, {exc.__class__.__name__}: {str(exc)}'")
            # print("\n".join(traceback.format_exception(exc)))
        else:
            print(f"{ip}: результат: '{f.result()}'")
