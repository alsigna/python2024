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


ids = [1, 2]
ids.extend(range(9, 19))
ip_addresses = [f"192.168.122.1{i:02}" for i in ids]
# ip_addresses.append("192.168.122.103")


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
    futures: dict[Future, str] = {pool.submit(print_version, ip): ip for ip in ip_addresses}

    for f in as_completed(futures):
        ip = futures.get(f)
        exc = f.exception()
        if exc is not None:
            print(f"{ip}: результат: 'ошибка выполнения, {exc.__class__.__name__}: {str(exc)}'")
            # print("\n".join(traceback.format_exception(exc)))
        else:
            print(f"{ip}: результат: '{f.result()}'")
