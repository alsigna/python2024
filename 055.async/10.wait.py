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


async def cancel_task(task: asyncio.Task) -> None:
    print(f"task {task.get_coro().__name__}")
    print(f"\t{task.done()=}")
    print(f"\t{task.cancelling()=}")
    print(f"\t{task.cancelled()=}")
    task.cancel()
    print(f"\t{task.cancelling()=} после cancel()")
    print(f"\t{task.cancelled()=} после cancel()")
    try:
        await task
    except asyncio.exceptions.CancelledError:
        print(f"\t{task.cancelled()=} после await")
        print(f"{task.get_coro().__name__} отменена")
    else:
        raise RuntimeError("Отмена задачи пошла не по плану")


async def main() -> None:
    done, pending = await asyncio.wait(
        fs=[
            asyncio.create_task(fast()),
            asyncio.create_task(middle()),
            asyncio.create_task(slow()),
        ],
        timeout=5,
        return_when=asyncio.FIRST_COMPLETED,
    )
    print("\nвыполненные таски")
    print(done)
    print("\nтаски, которые не уложились в стратегию")
    print(pending)
    await asyncio.gather(*[cancel_task(task) for task in pending])
    print("\nтаски, после отмены")
    print(pending)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    print("асинхронный код закончен")
    print(f"{perf_counter() - t0:.4f} сек")
