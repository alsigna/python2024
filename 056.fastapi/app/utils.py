import asyncio
import logging
from typing import Any

import aiohttp
import settings
from async_lru import alru_cache
from exceptions import (
    CLIAuthenticationFailed,
    CLIError,
    CLITimeoutError,
    NetboxDeviceAmbiguousError,
    NetboxDeviceNotFoundError,
    NetboxDeviceValidationError,
    NetboxRequestError,
)
from models import ABCDevice, NetboxDevice
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliAuthenticationFailed, ScrapliConnectionError
from scrapli.response import Response

log = logging.getLogger("uvicorn")
sem = asyncio.Semaphore(settings.CLI_MAX_CONNECTIONS)


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
        self._session = aiohttp.ClientSession(
            base_url=settings.NETBOX_URL,
            connector=aiohttp.TCPConnector(
                limit=settings.NETBOX_MAX_CONNECTIONS,
                ssl=False,
            ),
            headers={
                "Authorization": f"Token {settings.NETBOX_TOKEN}",
                "Accept": "application/json",
                "Content-Transfer-Encoding": "application/json",
            },
        )
        self.params = (("exclude", "config_context"),)
        self.api_device = "/api/dcim/devices/"

    async def close(self) -> None:
        await self._session.close()

    async def get_netbox_device(self, hostname: str) -> dict[str, Any]:
        params = self.params + (("name", hostname),)
        async with self._session.get(
            url=self.api_device,
            params=params,
        ) as response:
            response.raise_for_status()
            return await response.json()


@alru_cache(maxsize=256)
async def get_netbox_device(hostname: str) -> NetboxDevice:
    api = NetboxWalker()
    try:
        nb_response = await api.get_netbox_device(hostname)
    except Exception as exc:
        raise NetboxRequestError(f"Ошибка в Netbox запросе. {exc.__class__.__name__}: {str(exc)}")

    if nb_response["count"] == 0:
        raise NetboxDeviceNotFoundError(f"устройство {hostname} не найдено в Netbox")
    elif nb_response["count"] != 1:
        raise NetboxDeviceAmbiguousError(f"в Netbox найдено больше одного {hostname}")
    else:
        try:
            nb_device = NetboxDevice.model_validate(nb_response["results"][0])
        except Exception as exc:
            raise NetboxDeviceValidationError(f"Ошибка валидации модели. {exc.__class__.__name__}: {str(exc)}")
    return nb_device


async def get_scrapli_output(device: ABCDevice, output: str) -> Response:
    log_id = f"{device}/{output}:"
    cmd = getattr(device.commands, output)
    try:
        async with sem:
            log.debug(f"{log_id} подключение к устройству...")
            async with AsyncScrapli(**device.scrapli) as cli:
                output = await cli.send_command(cmd)
    except (ScrapliConnectionError, OSError) as exc:
        raise CLITimeoutError("Невозможно подключиться к устройству")
    except ScrapliAuthenticationFailed as exc:
        raise CLIAuthenticationFailed("Некорректные параметры доступа")
    except Exception as exc:
        raise CLIError(f"Ошибка сбора вывода. {exc.__class__.__name__}: {str(exc)}")
    else:
        log.debug(f"{log_id} сбор с устройства завершен")
    return output
