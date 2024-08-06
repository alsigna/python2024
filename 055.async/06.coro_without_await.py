import asyncio
from time import perf_counter


async def fast() -> None:
    print("fast старт")
    await asyncio.sleep(2)
    print("fast стоп")


async def very_slow() -> None:
    print("very_slow старт")
    for num in range(500_000_000):
        _ = num * num
    print("very_slow стоп")


async def main() -> None:
    await asyncio.gather(fast(), very_slow(), fast())


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print("асинхронный код закончен")
    print(f"{perf_counter() - t0:.4f} сек")
