import asyncio
import logging
from pathlib import Path
from typing import Any

import yaml
from rich.logging import RichHandler
from scrapli import AsyncScrapli

sem = asyncio.Semaphore(4)
COMMANDS = ["show version | i Software", "show ip arp", "show clock"]

log = logging.getLogger("hw_app")
log.setLevel(logging.DEBUG)
rh = RichHandler(
    level=logging.NOTSET,
    show_time=False,
)
rh.setFormatter(logging.Formatter(fmt="%(asctime)s.%(msecs)03d %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


scrapli_template = {
    "transport": "asyncssh",
    "platform": "cisco_iosxe",
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


async def collect_output(device: dict[str, Any], commands: list[str]) -> None:
    host = device.get("host")
    async with sem:
        log.debug(f"{host}: connecting to host...")
        try:
            async with AsyncScrapli(**device) as cli:
                log.debug(f"{host}: connection done")
                outputs = await cli.send_commands(commands)
        except Exception as exc:
            log.warning(f"{host}: connection failed")
            raise exc
        else:
            log.debug(f"{host}: outputs collected")

    folder = Path(Path.cwd(), "outputs", device.get("host"))
    Path.mkdir(folder, parents=True, exist_ok=True)
    for output in outputs:
        filename = output.channel_input.split("|")[0]
        filename = filename.strip().replace(" ", "_")
        with open(Path(folder, filename + ".txt"), "w") as f:
            f.write(output.result)
    log.info(f"{host}: outputs were saved")


def get_scrapli_devices(filename: str) -> list[dict[str, Any]]:
    with open(filename, "r") as f:
        data = yaml.safe_load(f)
    return [scrapli_template | device for device in data]


async def main() -> None:
    result = {}
    devices = get_scrapli_devices("devices.yaml")
    coros = await asyncio.gather(
        *[asyncio.create_task(collect_output(device, COMMANDS)) for device in devices],
        return_exceptions=True,
    )
    hosts = [device.get("host") for device in devices]

    for host, result in zip(hosts, coros):
        if isinstance(result, Exception):
            log.warning(f"{host}: {result.__class__.__name__}: {str(result)}")
        else:
            log.info(f"{host}: OK")


if __name__ == "__main__":
    asyncio.run(main())
