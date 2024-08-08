import asyncio
from traceback import TracebackException
from types import TracebackType
from typing import Type, TypeVar

import aiohttp
from exceptions import NetboxDeviceAmbiguousError, NetboxDeviceNotFoundError
from models import ABCDevice, NetboxDevice
from scrapli import AsyncScrapli
from scrapli.response import Response

# class Singleton(type):
#     _instances = {}

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
#         # else: #! не удалять, иначе init будет вызываться каждый раз
#         #     cls._instances[cls].__init__(*args, **kwargs)
#         return cls._instances[cls]


# class NetboxWalker:
#     def __init__(self) -> None:
#         headers = {
#             "Authorization": "Token 00b0e2f38b09638e610382c2d32a25ab6016bb41",
#             "Accept": "application/json",
#             "Content-Transfer-Encoding": "application/json",
#         }
#         nb_base_url = "http://89.169.172.172"
#         self._session = aiohttp.ClientSession(base_url=baheaders=headers)

#     async def __aenter__(self) -> "NetboxWalker":
#         return self

#     async def __aexit__(
#         self,
#         exc_type: Exception,
#         exc_val: TracebackException,
#         traceback: TracebackType,
#     ) -> None:
#         await self.close()

#     async def close(self) -> None:
#         await self._session.close()

#     async def make_http_get_request(self, url: str) -> str:
#         async with self._session.get(url) as response:
#             response.raise_for_status()
#             return await response.text()


async def get_netbox_device(hostname: str) -> NetboxDevice:
    nb_base_url = "http://89.169.172.172"
    connector = aiohttp.TCPConnector(limit=500, ssl=False)
    params = [
        ("name", hostname),
        ("exclude", "config_context"),
    ]
    headers = {
        "Authorization": "Token 00b0e2f38b09638e610382c2d32a25ab6016bb41",
        "Accept": "application/json",
        "Content-Transfer-Encoding": "application/json",
    }

    async with aiohttp.ClientSession(connector=connector, base_url=nb_base_url) as session:
        async with session.get("/api/dcim/devices/", params=params, headers=headers) as response:
            nb_response = await response.json()
    if nb_response["count"] == 0:
        raise NetboxDeviceNotFoundError(f"device {hostname} not found in netbox")
    elif nb_response["count"] != 1:
        raise NetboxDeviceAmbiguousError(f"device {hostname} not a single")
    else:
        nb_device = NetboxDevice.model_validate(nb_response["results"][0])
    return nb_device


async def get_scrapli_output(device: ABCDevice, output: str) -> Response:
    cmd = getattr(device.commands, output)
    async with AsyncScrapli(**device.scrapli) as cli:
        output = await cli.send_command(cmd)
    return output
