from factory import DeviceFactory
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import ABCDevice, AppResponse, Commands, NetboxDevice
from scrapli.response import Response
from utils import get_netbox_device, get_scrapli_output

app = FastAPI()


@app.get("/{hostname}/{output_type}/")
async def get_device_command(hostname: str, output_type: str) -> JSONResponse:
    if output_type not in Commands.model_fields:
        return JSONResponse(
            status_code=400,
            content=AppResponse(
                failed=True,
                hostname=hostname,
                output_type=output_type,
                msg=f"unknown output type",
            ).model_dump(),
        )

    nb_device: NetboxDevice = await get_netbox_device(hostname)
    device: ABCDevice = DeviceFactory(
        platform=nb_device.platform,
        hostname=nb_device.name,
        ip=nb_device.ip,
    )
    output: Response = await get_scrapli_output(device, output_type)

    if output.failed:
        return JSONResponse(
            status_code=400,
            content=AppResponse(
                failed=True,
                hostname=hostname,
                output_type=output_type,
                output=output.result,
                msg="error while collecting",
            ).model_dump(),
        )
    else:
        return JSONResponse(
            status_code=200,
            content=AppResponse(
                failed=False,
                hostname=hostname,
                output_type=output_type,
                output=output.result,
            ).model_dump(),
        )
