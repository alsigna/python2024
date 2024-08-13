import logging
from contextlib import asynccontextmanager

from exceptions import DeviceWalkerError
from factory import Device
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import CommandType, DeviceWalkerResponse, NetboxDevice
from scrapli.response import Response
from utils import NetboxWalker, get_netbox_device, get_scrapli_output
from uvicorn.config import LOGGING_CONFIG

LOGGING_CONFIG["formatters"]["default"].update(
    {
        "fmt": "%(asctime)s %(levelprefix)s %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
)
LOGGING_CONFIG["formatters"]["access"].update(
    {
        "fmt": '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
)


log = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # до старта
    log.setLevel("DEBUG")

    nb_walker = NetboxWalker()
    yield
    # после старта
    await nb_walker.close()
    log.debug("сессия aiohttp закрыта")


app = FastAPI(lifespan=lifespan)


@app.get("/api/v1/{hostname}/{command_type}/")
async def get_output(hostname: str, command_type: CommandType, raw: bool = False):
    def return_error(msg) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=DeviceWalkerResponse(
                hostname=hostname,
                failed=True,
                msg=msg,
            ).model_dump(),
        )

    log.debug(f"запрос команды {command_type} для устройства {hostname}")
    # данные из Netbox
    try:
        nb_device: NetboxDevice = await get_netbox_device(hostname)
    except DeviceWalkerError as exc:
        log.exception(exc)
        return return_error(str(exc))
    except Exception as exc:
        msg = f"Неизвестная ошибка при обращении к Netbox {exc.__class__.__name__} {str(exc)}"
        return return_error(msg)

    # фабрика
    try:
        scrapli_device = Device(**nb_device.model_dump())
    except DeviceWalkerError as exc:
        return return_error(str(exc))
    except Exception as exc:
        msg = f"Неизвестная ошибка фабрики {exc.__class__.__name__} {str(exc)}"
        return return_error(msg)

    # scrapli
    try:
        output: Response = await get_scrapli_output(scrapli_device, command_type)
    except DeviceWalkerError as exc:
        log.exception(exc)
        return return_error(str(exc))
    except Exception as exc:
        log.exception(exc)
        msg = f"Неизвестная ошибка при подключении к устройству {hostname} {exc.__class__.__name__} {str(exc)}"
        return return_error(msg)

    if command_type == CommandType.VERSION and not raw:
        output_str = scrapli_device.parse_version(output)
    else:
        output_str = output.result

    return JSONResponse(
        status_code=200,
        content=DeviceWalkerResponse(
            hostname=hostname,
            failed=output.failed,
            output=output_str,
        ).model_dump(),
    )
