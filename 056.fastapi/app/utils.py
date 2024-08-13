from typing import Any

import aiohttp
from exceptions import CLIAuthenticationError, CLITimedOutError, NetboxDeviceAmbError, NetboxDeviceNotFoundError
from models import ABCDevice, NetboxDevice
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliAuthenticationFailed, ScrapliConnectionError
from scrapli.response import Response
from settings import settings


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        # else: #! не удалять, иначе init будет вызываться каждый раз
        #     cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class NetboxWalker(metaclass=Singleton):
    def __init__(self) -> None:
        self.connector = aiohttp.TCPConnector(limit=100, ssl=False)
        self.params = (("exclude", "config_context"),)
        self.session = aiohttp.ClientSession(
            connector=self.connector,
            base_url=str(settings.NETBOX_URL),
            raise_for_status=True,
            headers={
                "Authorization": f"Token {settings.NETBOX_TOKEN}",
                "Content-Type": "application/json",
                "Accept-Charset": "application/json",
                "User-Agent": settings.APP_NAME,
            },
        )

    async def close(self) -> None:
        await self.session.close()

    async def get_device_by_hostname(self, hostname: str) -> dict[Any, Any]:
        async with self.session.get(
            url="/api/dcim/devices/",
            params=self.params + (("name", hostname),),
        ) as response:
            response.raise_for_status()
            result = await response.json()
            return result


async def get_netbox_device(hostname: str) -> NetboxDevice:
    nb_walker = NetboxWalker()
    j = await nb_walker.get_device_by_hostname(hostname)

    if j.get("count") == 0:
        raise NetboxDeviceNotFoundError(f"{hostname} нет в Netbox")
    elif j.get("count") >= 2:
        raise NetboxDeviceAmbError(f"Множество устройств {hostname} в Netbox")

    device = j.get("results")[0]
    nb_device = NetboxDevice.model_validate(device)
    return nb_device


async def get_scrapli_output(device: ABCDevice, output_type: str) -> Response:
    cmd = getattr(device.commands, output_type)

    try:
        async with AsyncScrapli(**device.scrapli) as cli:
            output: Response = await cli.send_command(cmd)
    except ScrapliAuthenticationFailed:
        raise CLIAuthenticationError(f"Неправильные логин/пароль на устройство {device}")
    except (ScrapliConnectionError, OSError):
        raise CLITimedOutError(f"Устройство {device} недоступно")

    return output
