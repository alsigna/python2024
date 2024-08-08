import asyncio
from time import perf_counter

import aiohttp


async def make_get_request(session: aiohttp.ClientSession, item: int) -> str:

    async with session.get(f"/items/{item}") as response:
        j = await response.json()

    item = j.get("item")
    delay = j.get("delay")
    return f"{item:>5} - {delay}"


async def main() -> None:
    connector = aiohttp.TCPConnector(limit=2000)
    async with aiohttp.ClientSession(
        connector=connector,
        base_url="http://127.0.0.1:8000",
        raise_for_status=True,
    ) as session:
        results = await asyncio.gather(
            *[asyncio.create_task(make_get_request(session, item)) for item in range(1, 10001)],
            return_exceptions=True,
        )

    for indx, result in enumerate(results):
        print(f"{indx:>5} - {result}")

    errors = len(list(filter(lambda r: isinstance(r, Exception), results)))
    success = len(list(filter(lambda r: isinstance(r, str), results)))

    print(f"{errors=}, {success=}")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print(f"время: {perf_counter() - t0:.4f} сек.")
