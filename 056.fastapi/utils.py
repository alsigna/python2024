import aiohttp
import settings
from exceptions import NetboxDeviceAmbError, NetboxDeviceNotFoundError
from models import ABCDevice, NetboxDevice
from scrapli import AsyncScrapli
from scrapli.response import Response


async def get_netbox_device(hostname: str) -> NetboxDevice:
    connector = aiohttp.TCPConnector(limit=100, ssl=False)
    params = (
        ("exclude", "config_context"),
        ("name", hostname),
    )
    async with aiohttp.ClientSession(
        connector=connector,
        base_url=settings.NETBOX_URL,
        raise_for_status=True,
        headers={
            "Authorization": f"Token {settings.NETBOX_TOKEN}",
            "Content-Type": "application/json",
            "Accept-Charset": "application/json",
            "User-Agent": settings.APP_NAME,
        },
    ) as session:
        async with session.get(url="/api/dcim/devices/", params=params) as response:
            j = await response.json()

    if j.get("count") == 0:
        raise NetboxDeviceNotFoundError(f"{hostname} нет в Netbox")
    elif j.get("count") >= 2:
        raise NetboxDeviceAmbError(f"Множество устройств {hostname} в Netbox")

    device = j.get("results")[0]
    nb_device = NetboxDevice.model_validate(device)
    return nb_device


async def save_scrapli(device: ABCDevice) -> Response:
    pass


async def get_scrapli_output(device: ABCDevice, output_type: str) -> Response:
    cmd = getattr(device.commands, output_type)

    async with AsyncScrapli(**device.scrapli) as cli:
        if output_type == "save":
            output = await save_scrapli(device)
        else:
            output: Response = await cli.send_command(cmd)

    return output
