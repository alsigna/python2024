from concurrent.futures import ThreadPoolExecutor
from getpass import getpass
from pprint import pprint
from typing import Any

import yaml
from scrapli import Scrapli


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


def check_flag(d: dict) -> bool:
    return d.get("flag")


def send_show(device_dict, command) -> str:
    wd = Watchdog(threshold=1)
    if wd.fails >= wd.threshold:
        raise RuntimeError("превышен порог")
    try:
        with Scrapli(**device_dict) as ssh:
            output = ssh.send_command(command)
    except Exception as exc:
        device_dict["transport"] = "system"
        try:
            with Scrapli(**device_dict) as ssh:
                output = ssh.send_command(command)
        except Exception as exc:
            wd.fails += 1
            raise exc
        else:
            return output.result
    else:
        return output.result


def send_command_to_devices(creds: dict, command: str, max_workers: int = 2) -> str:
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for device in devices:
        device.update(creds)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_show, device, command) for device in devices]
        results = []
        hosts = [device["host"] for device in devices]

        for f in futures:
            exc = f.exception()
            if exc is not None:
                print(f"ошибка {exc.__class__.__name__} {str(exc)}")
                results.append(f"{exc.__class__.__name__} {str(exc)}")
            else:
                results.append(f.result())

    return dict(zip(hosts, results))


if __name__ == "__main__":
    username = input("Username: ")
    password = getpass("Password: ")
    command = input("Input command: ")
    creds = {"auth_username": username, "auth_password": password}
    pprint(send_command_to_devices(creds, command), width=512)
