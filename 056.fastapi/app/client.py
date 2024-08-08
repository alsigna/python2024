import asyncio

import aiohttp

sem = asyncio.Semaphore(5000)


async def make_get_request(session: aiohttp.ClientSession, item: int) -> str:
    url = f"http://127.0.0.1:8000/items/{item}?q=test"

    async with session.get(url) as response:
        response.raise_for_status()
        j = await response.json()

    return f"{j.get('item'):>5}: {j.get('delay')}"


async def main() -> None:
    connector = aiohttp.TCPConnector(limit=5000)
    async with aiohttp.ClientSession(connector=connector) as session:
        results = await asyncio.gather(
            *[asyncio.create_task(make_get_request(session, item)) for item in range(1, 50001)],
            return_exceptions=True,
        )
    for indx, result in enumerate(results):
        print(f"{indx:>5} - {result}")
    errors = len(list(filter(lambda result: isinstance(result, Exception), results)))
    success = len(list(filter(lambda result: not isinstance(result, Exception), results)))
    print(f"{errors=}, {success=}")


if __name__ == "__main__":
    asyncio.run(main())
