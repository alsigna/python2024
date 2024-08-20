from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from pathlib import Path
from time import sleep
from typing import Any

import typer
from logger import log
from rich.live import Live
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
from scrapli.response import Response


def get_output(device: dict[str, Any], command: str) -> Response:
    with Scrapli(**device) as cli:
        result = cli.send_command(command)

    return result


def save_to_file(response: Response) -> None:
    folder = Path(Path.cwd(), "outputs", response.host)
    Path.mkdir(folder, parents=True, exist_ok=True)
    filename = response.channel_input.replace(" ", "_") + ".txt"
    with open(Path(folder, filename), "w") as f:
        f.write(response.result)


def execute_tasks(devices: list[dict[str, Any]], command: str, max_workers) -> None:
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    )
    progress_bar = progress.add_task("[red]Прогресс...", total=len(devices))

    statistics = Progress(
        TextColumn("[progress.description]{task.description}"),
        TextColumn("{task.completed}"),
    )
    statistics_ok = statistics.add_task("[green]Успешно", total=len(devices))
    statistics_skip = statistics.add_task("[yellow]Пропущено", total=len(devices))
    statistics_fail = statistics.add_task("[red]Ошибка", total=len(devices))

    footer = Table.grid()
    footer.add_row(
        Panel.fit(progress, title="Прогресс", border_style="green", padding=(1, 2)),
        Panel.fit(statistics, title="[b]Статистика", border_style="red", padding=(0, 2)),
    )
    with Live(footer, refresh_per_second=10):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            log.info(f"начало опроса {max_workers=}...")
            # tasks: dict[Future:str] = {
            #     executor.submit(get_output, device, command): device.get("host") for device in devices
            # }
            tasks: dict[Future:str] = {}
            for device in devices:
                ip = device.get("host")
                f = executor.submit(get_output, device, command)
                tasks[f] = ip

            for task in as_completed(tasks):
                progress.update(progress_bar, advance=1)
                ip = tasks.get(task)
                exc = task.exception()
                if exc is not None:
                    if isinstance(exc, OSError):
                        statistics.update(statistics_skip, advance=1)
                        log.warning(f"{ip}: устройство недоступно")
                    else:
                        statistics.update(statistics_fail, advance=1)
                        log.error(f"{ip}: ошибка сбора команды: {exc.__class__.__name__} - {exc}")
                else:
                    statistics.update(statistics_ok, advance=1)
                    result: Response = task.result()
                    log.info(f"{ip}: сбор завершился успешно")
                    log.debug(f"{ip}: результат сбора {result.result}")
                    save_to_file(result)
            log.info(f"опрос завершен")
