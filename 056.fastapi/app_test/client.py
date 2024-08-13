import asyncio
from time import perf_counter

import aiohttp


async def make_get_request(session: aiohttp.ClientSession, item: int) -> str:
    url = f"http://127.0.0.1:8000/items/{item}"

    async with session.get(url) as response:
        j = await response.json()

    return f"{j.get('item'):>5}: {j.get('delay')}"


async def main() -> None:
    connector = aiohttp.TCPConnector(limit=5000)
    session = aiohttp.ClientSession(connector=connector)
    results = await asyncio.gather(
        *[asyncio.create_task(make_get_request(session, item)) for item in range(1, 50001)],
        return_exceptions=True,
    )
    await session.close()
    for indx, result in enumerate(results):
        print(f"{indx:>5} - {result}")
    errors = len(list(filter(lambda result: isinstance(result, Exception), results)))
    success = len(list(filter(lambda result: not isinstance(result, Exception), results)))
    print(f"{errors=}, {success=}")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print(f"время: {perf_counter() - t0:.4f} сек.")
