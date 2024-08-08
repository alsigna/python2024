import asyncio
from itertools import product
from time import perf_counter

import aiohttp

sem = asyncio.Semaphore(5000)


hostnames = [f"r{device_id}" for device_id in range(9, 19)]
hostnames.extend(["r1", "r2", "r6", "r7"])
commands = ["version", "running", "inventory"]
device_command_pairs = list(product(commands, hostnames))
device_command_pairs *= 2


async def make_get_request(session: aiohttp.ClientSession, hostname: str, command: str) -> str:
    url = f"http://127.0.0.1:8000/{hostname}/{command}/"

    async with session.get(url) as response:
        # response.raise_for_status()
        j = await response.json()

    return f"{j.get('hostname'):>10}: {not j.get('failed'):>5}: {j.get('output')[:10]} {j.get('msg')}"


async def main() -> None:
    connector = aiohttp.TCPConnector(limit=5000)
    async with aiohttp.ClientSession(connector=connector) as session:
        results = await asyncio.gather(
            *[asyncio.create_task(make_get_request(session, elem[1], elem[0])) for elem in device_command_pairs],
            return_exceptions=True,
        )
    for indx, result in enumerate(results):
        print(f"{indx:>5} - {result}")
    errors = len(list(filter(lambda result: isinstance(result, Exception), results)))
    success = len(list(filter(lambda result: not isinstance(result, Exception), results)))
    print(f"{errors=}, {success=}")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print(f"затраченное время: {perf_counter() - t0:.4f} сек.")
