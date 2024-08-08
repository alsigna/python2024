import asyncio
import logging
from contextlib import asynccontextmanager

import settings
from exceptions import CLIError, NetboxError
from factory import DeviceFactory
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import ABCDevice, AppResponse, Commands, NetboxDevice
from scrapli.response import Response
from utils import NetboxWalker, get_netbox_device, get_scrapli_output

log = logging.getLogger("uvicorn")
log.setLevel(logging.DEBUG)
sem = asyncio.Semaphore(settings.CLI_MAX_CONNECTIONS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    nb_api = NetboxWalker()
    yield
    await nb_api.close()


app = FastAPI(lifespan=lifespan)


@app.get("/{hostname}/{output_type}/")
async def get_device_command(hostname: str, output_type: str) -> JSONResponse:
    def return_error(msg: str) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=AppResponse(
                failed=True,
                hostname=hostname,
                output_type=output_type,
                msg=msg,
            ).model_dump(),
        )

    if output_type not in Commands.model_fields:
        return return_error("неизвестный тип вывода")
    log_id = f"{hostname}/{output_type}:"
    log.debug(f"{log_id} тип вывода {output_type} существует")

    try:
        nb_device: NetboxDevice = await get_netbox_device(hostname)
    except NetboxError as exc:
        msg = f"{exc.__class__.__name__}: {str(exc)}"
        log.error(f"{log_id} {msg}")
        return return_error(msg)
    except Exception as exc:
        msg = f"Неизвестное исключение при работе с Netbox: {exc.__class__.__name__}: {str(exc)}"
        log.error(f"{log_id} {msg}")
        return return_error(msg)

    log.debug(f"{log_id} данные из netbox корректно получены")

    device: ABCDevice = DeviceFactory(
        platform=nb_device.platform,
        hostname=nb_device.name,
        ip=nb_device.ip,
    )
    log.debug(f"{log_id} для устройства выбран драйвер {device.__class__.__name__}")
    try:
        output: Response = await get_scrapli_output(device, output_type)
    except CLIError as exc:
        msg = f"{exc.__class__.__name__}: {str(exc)}"
        log.error(f"{log_id} {msg}")
        return return_error(msg)
    except Exception as exc:
        msg = f"Неизвестное исключение при работе с Netbox: {exc.__class__.__name__}: {str(exc)}"
        log.error(f"{log_id} {msg}")
        return return_error(msg)

    if output.failed:
        msg = "ошибка сбора команды"
        log.error(f"{log_id} {msg}, {output.result}")
        return JSONResponse(
            status_code=400,
            content=AppResponse(
                failed=True,
                hostname=hostname,
                output_type=output_type,
                output=f"{output.channel_input}\n{output.result}",
                msg=msg,
            ).model_dump(),
        )
    else:
        log.info(f"{log_id} вывод успешно собран")
        return JSONResponse(
            status_code=200,
            content=AppResponse(
                failed=False,
                hostname=hostname,
                output_type=output_type,
                output=output.result,
            ).model_dump(),
        )
