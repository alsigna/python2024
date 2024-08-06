import asyncio
from time import perf_counter


async def slow() -> None:
    print("slow старт")
    await asyncio.sleep(6)
    print("slow стоп")


async def main() -> None:
    slow()


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print("асинхронный код закончен")
    print(f"{perf_counter() - t0:.4f} сек")
