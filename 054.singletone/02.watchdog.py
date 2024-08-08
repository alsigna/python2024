import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from random import randint

from scrapli import Scrapli
from scrapli.exceptions import ScrapliAuthenticationFailed

scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd1",
    "auth_strict_key": False,
    "transport": "telnet",
}


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        # else: #! не удалять, иначе init будет вызываться каждый раз
        #     cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class Watchdog(metaclass=Singleton):
    def __init__(self, threshold: int = 5) -> None:
        self.fails = 0
        self.threshold = threshold

    def __repr__(self) -> str:
        return f"<WD: threshold={self.threshold}>"


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


def print_version(host: str) -> str:
    wd = Watchdog(threshold=3)
    thr_name = threading.current_thread().name
    print(f"[{thr_name}] поток запущен, число ошибок при старте потока {wd.fails}")
    if wd.fails >= wd.threshold:
        raise RuntimeError(f"превышен порог ошибок, {wd.fails=}, {wd.threshold=}")

    device = scrapli_template | {"host": host}

    try:
        with Scrapli(**device) as ssh:
            output = ssh.send_command("show version")
    except ScrapliAuthenticationFailed as exc:
        wd.fails += 1
        raise exc
    except OSError as exc:
        raise exc
    except Exception as exc:
        wd.fails += 1
        raise exc

    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    time.sleep(randint(10, 200) / 100)
    return result


with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thr") as pool:
    futures: dict[Future, str] = {pool.submit(print_version, ip): ip for ip in ip_addresses}

    for f in as_completed(futures):
        ip = futures.get(f)
        exc = f.exception()
        if exc is not None:
            print(f"{ip}: результат: 'ошибка выполнения, {exc.__class__.__name__}: {str(exc)}'")
        else:
            print(f"{ip}: результат: '{f.result()}'")
