from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import Any

from scrapli import Scrapli
from scrapli.response import Response


def get_output(device: dict[str, Any], command: str) -> Response:
    with Scrapli(**device) as conn:
        output = conn.send_command(command)
    return output


def execute_tasks(devices: list[dict[str, Any]], command: str, max_workers: int = 5) -> None:
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures: dict[Future, str] = {
            pool.submit(get_output, scrapli, command): host for host, scrapli in devices.items()
        }

        for f in as_completed(futures):
            host = futures.get(f)
            exc = f.exception()

            if exc is not None:
                print(f"{host}: результат: 'ошибка выполнения, {exc.__class__.__name__}: {str(exc)}'")
            else:
                print(f"{host}: результат: '{f.result().result}'")
