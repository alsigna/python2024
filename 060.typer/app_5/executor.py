import logging
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import Any

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from scrapli import Scrapli
from scrapli.response import Response

log = logging.getLogger("collector")
log.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.NOTSET)
sh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
log.addHandler(sh)


def get_output(device: dict[str, Any], command: str) -> Response:
    with Scrapli(**device) as conn:
        output = conn.send_command(command)
    return output


progress = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
)


def execute_tasks(devices: list[dict[str, Any]], command: str, max_workers: int = 5) -> None:
    log.info("старт сбора вывода....")
    with progress:
        task1 = progress.add_task("[red]collecting...", total=len(devices))
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures: dict[Future, str] = {
                pool.submit(get_output, scrapli, command): host for host, scrapli in devices.items()
            }

            for f in as_completed(futures):
                progress.update(task1, advance=1)
                host = futures.get(f)
                log.debug(f"вывод для {host} собраны")
                exc = f.exception()

                if exc is not None:
                    log.warning(f"{host}: результат: 'ошибка выполнения, {exc.__class__.__name__}: {str(exc)}'")
                else:
                    log.info(f"{host}: результат: '{f.result().result}'")
