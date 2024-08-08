import asyncio
from time import perf_counter

import aiohttp


async def make_get_request(item: int) -> str:
    url = f"http://127.0.0.1:8000/items/{item}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            j = await response.json()

    return f"{j.get('item'):>5}: {j.get('delay')}"


async def main() -> None:
    results = await asyncio.gather(
        *[asyncio.create_task(make_get_request(item)) for item in range(1, 1001)],
        return_exceptions=True,
    )
    for result in results:
        print(result)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print(f"время: {perf_counter() - t0:.4f} сек.")
