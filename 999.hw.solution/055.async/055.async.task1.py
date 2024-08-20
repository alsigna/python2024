import asyncio
import math
from itertools import groupby
from random import randint
from time import perf_counter
from typing import Any

import aiohttp
import yaml

MAX_CONNECTIONS = 20
LIMIT = 30
# url можно через urllib формировать, но для простоты так сделаем:
URL_TEMPLATE = f"https://dummyjson.com/quotes?limit={LIMIT}&skip={{offset}}&delay={{delay}}"


async def make_get_request(session: aiohttp.ClientSession, url: str) -> dict[str, Any]:
    async with session.get(url) as response:
        response.raise_for_status()
        j = await response.json()

    return j


async def main() -> None:
    quotes = []
    connector = aiohttp.TCPConnector(limit=MAX_CONNECTIONS, ssl=False)
    session = aiohttp.ClientSession(connector=connector)

    urls = []
    result = await make_get_request(session, URL_TEMPLATE.format(offset=0, delay=randint(300, 3000)))
    total = result.get("total")
    quotes.extend(result.get("quotes"))
    pages = total // LIMIT + 1
    for page in range(1, pages):
        urls.append(URL_TEMPLATE.format(offset=page * LIMIT, delay=randint(300, 3000)))

    results = await asyncio.gather(
        *[asyncio.create_task(make_get_request(session, url)) for url in urls],
        return_exceptions=True,
    )
    await session.close()
    for result in results:
        quotes.extend(result.get("quotes"))

    quotes.sort(key=lambda q: q.get("author"))
    yaml_data = {}
    for author_name, author_quotes in groupby(quotes, key=lambda x: x.get("author")):
        yaml_data[author_name] = [q.get("quote") for q in author_quotes]

    with open("quotes.yaml", "w") as f:
        yaml.safe_dump(yaml_data, f, width=math.inf)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print(f"затраченное время: {perf_counter() - t0:.4f} сек.")
