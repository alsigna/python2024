import logging
from enum import auto
from pathlib import Path
from typing import Annotated

import typer
import yaml
from executor import execute_tasks
from strenum import UppercaseStrEnum

log = logging.getLogger("collector")

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
)


TFileName = Annotated[
    str,
    typer.Option(
        "--filename",
        "-f",
        help="Файл с исходными данными",
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
        show_default=True,
    ),
]


class LogLevel(UppercaseStrEnum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()
    DEBUG = auto()


def set_log_level(level: LogLevel) -> None:
    log.setLevel(level)


TLogLevel = Annotated[
    LogLevel,
    typer.Option(
        "--log-level",
        help="Уровень логирования",
        callback=set_log_level,
        show_default=True,
    ),
]

scrapli_template = {
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
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
    help="Входные параметры из файла",
)
def collect_from_file(
    filename: TFileName,
    command: TCommand,
    workers: TWorkers = 5,
    loglevel: TLogLevel = LogLevel.INFO,
):
    if not Path(filename).is_file():
        raise typer.BadParameter(f"Файл {filename} не найден")
    with open(filename, "r") as f:
        input_data = yaml.safe_load(f)

    devices = {device_from_file.get("host"): scrapli_template | device_from_file for device_from_file in input_data}
    execute_tasks(devices, command, workers)


@app.command(
    # no_args_is_help=True,
    name="netbox",
    help="Входные параметры из NetBox",
)
def collect_from_netbox():
    raise NotImplementedError("В процессе реализации")


if __name__ == "__main__":
    app()
