import asyncio
from typing import AsyncGenerator


async def acounter(delay: int) -> AsyncGenerator[int, int]:
    c = 0
    while True:
        c += 1
        await asyncio.sleep(delay)
        yield c


async def main() -> None:
    async for i in acounter(1):
        print(i)


if __name__ == "__main__":
    asyncio.run(main())
