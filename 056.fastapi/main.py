import asyncio

from exceptions import DeviceWalkerError
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import CiscoXE, DeviceWalkerResponse, HuaweiVRP, NetboxDevice
from utils import get_netbox_device, get_scrapli_output

app = FastAPI()


@app.get("/api/v1/{hostname}/{output_type}")
async def get_output(hostname: str, output_type: str):
    def return_error(msg) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=DeviceWalkerResponse(
                hostname=hostname,
                failed=True,
                msg=msg,
            ).model_dump(),
        )

    try:
        nb_device: NetboxDevice = await get_netbox_device(hostname)
    except DeviceWalkerError as exc:
        return return_error(str(exc))
    except Exception as exc:
        msg = f"Неизвестное исключение {exc.__class__.__name__} {str(exc)}"
        return return_error(msg)

    # TODO перейти на фабрику
    scrapli_device = CiscoXE(hostname=hostname, ip=nb_device.ip)

    # 3 сходить в scrapli
    output = await get_scrapli_output(scrapli_device, output_type)

    return JSONResponse(
        status_code=200,
        content=DeviceWalkerResponse(
            hostname=hostname,
            failed=output.failed,
            output=output.result,
        ).model_dump(),
    )
