import asyncio
from time import perf_counter

import requests


async def get_netbox_version() -> None:
    url = "https://demo.netbox.dev/api/status/"
    response = requests.get(url)
    response.raise_for_status()
    print(f"NB version {response.json().get('netbox-version', "unknown")}")


async def main() -> None:
    await asyncio.gather(*(get_netbox_version() for _ in range(10)))


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print("асинхронный код закончен")
    print(f"{perf_counter() - t0:.4f} сек")
