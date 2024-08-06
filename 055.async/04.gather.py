import asyncio
from time import perf_counter


async def fast() -> None:
    print("fast старт")
    await asyncio.sleep(2)
    print("fast стоп")


async def middle() -> None:
    print("middle старт")
    await asyncio.sleep(4)
    print("middle стоп")


async def slow() -> None:
    print("slow старт")
    await asyncio.sleep(6)
    print("slow стоп")


async def main() -> None:
    await asyncio.gather(fast(), middle(), slow())


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print("асинхронный код закончен")
    print(f"{perf_counter() - t0:.4f} сек")
