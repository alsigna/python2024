import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import yaml
from rich.logging import RichHandler
from scrapli import Scrapli

MAX_WORKERS = 2
COMMANDS = ["show version | i Software", "show ip arp", "show clock"]

log = logging.getLogger("hw_app")
log.setLevel(logging.DEBUG)
rh = RichHandler(
    level=logging.NOTSET,
    show_time=False,
)
rh.setFormatter(logging.Formatter(fmt="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)

scrapli_template = {
    "platform": "cisco_iosxe",
    "transport": "system",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport_options": {
        "open_cmd": [
            "-o",
            "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
            "-o",
            "HostKeyAlgorithms=+ssh-rsa",
        ]
    },
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
    def __init__(self, threshold: int = 2) -> None:
        self.fails = 0
        self.threshold = threshold

    def __repr__(self) -> str:
        return f"<WD: threshold={self.threshold}>"


def get_scrapli_devices(filename: str) -> list[dict[str, Any]]:
    with open(filename, "r") as f:
        data = yaml.safe_load(f)
    return [scrapli_template | device for device in data]


def collect_output(device: dict[str, Any], commands: list[str]) -> None:
    wd = Watchdog()
    if wd.fails >= wd.threshold:
        log.warning(f"{device.get('host')}: {wd.fails=}, {wd.threshold=}")
        raise RuntimeError(f"Failure count {wd.fails} riches threshold {wd.threshold}")
    else:
        log.debug(f"{device.get('host')}: {wd.fails=}, {wd.threshold=}")

    try:
        with Scrapli(**device) as cli:
            outputs = cli.send_commands(commands)
    except Exception as exc:
        wd.fails += 1
        raise exc
    folder = Path(Path.cwd(), "outputs", device.get("host"))
    Path.mkdir(folder, parents=True, exist_ok=True)
    for output in outputs:
        filename = output.channel_input.split("|")[0]
        filename = filename.strip().replace(" ", "_")
        with open(Path(folder, filename + ".txt"), "w") as f:
            f.write(output.result)


if __name__ == "__main__":
    devices = get_scrapli_devices("devices.yaml")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        tasks = {executor.submit(collect_output, device, COMMANDS): device.get("host") for device in devices}
        for task in as_completed(tasks):
            host = tasks.get(task)
            exc = task.exception()
            if exc is not None:
                log.warning(f"{host}: {exc.__class__.__name__}: {str(exc)}")
            else:
                result = task.result()
                log.info(f"{host}: OK")