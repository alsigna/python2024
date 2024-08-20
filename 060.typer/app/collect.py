from enum import auto
from pathlib import Path
from typing import Annotated

import typer
import yaml
from executor import execute_tasks
from logger import log
from strenum import UppercaseStrEnum


class LogLevel(UppercaseStrEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()


app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    name="collect",
)

TFilename = Annotated[
    str,
    typer.Option(
        "--filename",
        "-f",
        help="Файл с устройствами",
        show_default=False,
    ),
]

TTag = Annotated[
    str,
    typer.Option(
        "--tag",
        "-t",
        help="Netbox Tag для выгрузки устройств",
        show_default=False,
    ),
]


TCommand = Annotated[
    str,
    typer.Option(
        "--command",
        "-c",
        help="Команда для сбора",
        show_default=False,
    ),
]

TWorkers = Annotated[
    int,
    typer.Option(
        "--workers",
        "-w",
        help="Количество потоков",
    ),
]


def set_log_level(level: LogLevel) -> None:
    log.setLevel(level)


TLogLevel = Annotated[
    LogLevel,
    typer.Option(
        "--log-level",
        help="Уровень логирования",
        callback=set_log_level,
    ),
]

scrapli_template = {
    "transport": "telnet",
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


@app.command(
    no_args_is_help=True,
    name="file",
    help="Данные устройств из файла",
)
def get_devices_from_file(
    filename: TFilename,
    command: TCommand,
    workers: TWorkers = 5,
    loglevel: TLogLevel = LogLevel.DEBUG,
):
    _file = Path(Path.cwd(), filename)
    if not _file.is_file():
        raise typer.BadParameter(f"файла {filename} не существует")
    with open(_file, "r") as f:
        data_from_file = yaml.safe_load(f)

    devices = [scrapli_template | device for device in data_from_file]

    execute_tasks(devices, command, workers)


@app.command(
    no_args_is_help=True,
    name="netbox",
    help="Данные устройств из Netbox",
)
def get_devices_from_netbox(
    tag: TTag,
    command: TCommand,
    loglevel: TLogLevel = LogLevel.DEBUG,
):
    log.warning(f"{log.level=}")
    # print(f"{tag=}, {command=}")


if __name__ == "__main__":
    app()
