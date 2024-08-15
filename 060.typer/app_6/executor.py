import logging
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from pathlib import Path
from random import randint
from typing import Any

from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from scrapli import Scrapli
from scrapli.exceptions import ScrapliConnectionError
from scrapli.response import Response

log = logging.getLogger("collector")
log.setLevel(logging.DEBUG)


rh = RichHandler(show_time=False)
rh.setLevel(logging.NOTSET)
rh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
log.addHandler(rh)


def get_output(device: dict[str, Any], command: str) -> Response:
    with Scrapli(**device) as conn:
        output = conn.send_command(command)
    delay = randint(100, 1000) / 100
    time.sleep(delay)
    return output


def save_to_file(output: Response) -> None:
    hostname = output.host
    command = output.channel_input.replace(" ", "-")
    Path.mkdir(Path(Path.cwd(), "outputs", hostname), exist_ok=True, parents=True)
    with open(Path(Path.cwd(), "outputs", hostname, f"{command}.txt"), "w") as f:
        f.write(output.result)


PROGRESS_COLUMNS = [
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
]


def execute_tasks(devices: list[dict[str, Any]], command: str, max_workers: int = 5) -> None:
    progress = Progress(*PROGRESS_COLUMNS)
    progress_bar = progress.add_task("[b]Прогресс сбора...", total=len(devices))

    stats = Progress("{task.description}", TextColumn("{task.completed}"))
    stats_succeeded_bar = stats.add_task("[green]Завершено успешно")
    stats_skipped_bar = stats.add_task("[yellow]Устройств пропущено")
    stats_failed_bar = stats.add_task("[red]Завершено с ошибкой")

    footer = Table.grid()
    footer.add_row(
        Panel.fit(progress, title="Прогресс", border_style="green", padding=(1, 2)),
        Panel.fit(stats, title="Статистика", border_style="red", padding=(0, 2)),
    )

    with Live(footer, refresh_per_second=10):
        log.info(f"старт сбора вывода, {max_workers=}....")
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures: dict[Future, str] = {
                pool.submit(get_output, scrapli, command): host for host, scrapli in devices.items()
            }

            for f in as_completed(futures):
                progress.update(progress_bar, advance=1)
                host = futures.get(f)
                log.debug(f"вывод для {host} собраны")
                exc = f.exception()

                if exc is not None:
                    if isinstance(exc, ScrapliConnectionError):
                        log.warning(f"{host}: устройство недоступно")
                        stats.update(stats_skipped_bar, advance=1)
                    else:
                        log.error(f"{host}: результат: 'ошибка выполнения, {exc.__class__.__name__}: {str(exc)}'")
                        stats.update(stats_failed_bar, advance=1)
                else:
                    result = f.result()
                    save_to_file(result)
                    stats.update(stats_succeeded_bar, advance=1)
                    log.info(f"{host}: результат: '{result.result}'")

        log.info("сбор вывода закончен")
